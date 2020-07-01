# -*- coding: utf-8 -*-
# @Time    : 2019/10/22 21:42
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : geetest.py
# @Software: PyCharm

import os
import random
import requests
import time
import json
from PIL import Image
import cv2
import numpy as np


session = requests.session()
session.headers = {
    'Content-Type': 'application/json',
    'Origin': 'https://passport.ximalaya.com',
    'Referer': 'https://passport.ximalaya.com/page/web/forget',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
}


def _pic_download(url, type):
    """
    图片下载
    :param url:
    :param type:
    :return:
    """
    save_path = os.path.abspath('...') + '\\' + 'images'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    img_path = save_path + '\\' + '{}.jpg'.format(type)
    img_data = session.get(url).content
    with open(img_path, 'wb') as f:
        f.write(img_data)
    return img_path


def _cut_slider(path):
    """
    滑块切割
    :return:
    """
    image = Image.open(path)
    x = []
    y = []
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            pix = image.load()[i, j]
            if pix != 255:
                x.append(i)
                y.append(j)
    z = (np.min(x), np.min(y), np.max(x), np.max(y))
    result = image.crop(z)
    result.convert('RGB').save(path)
    # result.show()
    return result.size[0], result.size[1]


def _get_distance(slider_url, captcha_url):
    """
    获取缺口距离
    :param slider_url: 滑块图片 url
    :param captcha_url: 验证码图片 url
    :return:
    """
    save_path = os.path.abspath('...') + '\\' + 'images'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # 引用上面的图片下载
    slider_path = _pic_download(slider_url, 'slider')

    # 引用上面的图片下载
    captcha_path = _pic_download(captcha_url, 'captcha')

    # # 计算拼图还原距离
    target = cv2.imread(slider_path, 0)
    template = cv2.imread(captcha_path, 0)
    temp = save_path + '\\' + 'temp.jpg'
    targ = save_path + '\\' + 'targ.jpg'
    cv2.imwrite(targ, target)
    w, h = _cut_slider(slider_path)
    cv2.imwrite(temp, template)
    target = cv2.imread(targ)
    target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    target = abs(255 - target)
    cv2.imwrite(targ, target)
    target = cv2.imread(targ)
    template = cv2.imread(temp)
    result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
    x, y = np.unravel_index(result.argmax(), result.shape)

    # 调用PIL Image 做测试
    image = Image.open(captcha_path)

    xy = (y + 15, x, y + w, x + h)
    # 切割
    imagecrop = image.crop(xy)
    # 保存切割的缺口
    imagecrop.save(save_path + '\\' + "new_image.jpg")
    imagecrop.show()
    return int(y + 15)


def process_distance(distance):
    """
    处理缺口距离
    :param distance:
    :return:
    """
    x = -12 * 0.808 + (distance + 10) * (384 - 85.64800000000001 + 24 * 0.808) / (384 - 40)
    return int(round(x / 0.808 + 44))


def _init_slider():
    """
    初始化滑块
    :return:
    """
    url = 'https://mobile.ximalaya.com/captcha-web/check/slide/get?bpId=139&sessionId=xm_k21uo8e150s7pt'

    resp = session.get(url).json()
    if resp['result'] == 'true':
        return {
            'captcha_url': resp['data']['bgUrl'],
            'slider_url': resp['data']['fgUrl']
        }
    return None


def _slider_verify(distance):
    """
    滑块验证
    :param distance:
    :return:
    """
    url_ = 'https://mobile.ximalaya.com/captcha-web/valid/slider'

    start_x = random.randint(795, 810)
    start_y = random.randint(325, 340)
    start_time = int(time.time() * 1000)
    time.sleep(random.randint(1, 2))
    payload = json.dumps({
        'bpId': 139,
        'sessionId': "xm_k21uo8e150s7pt",
        'type': "slider",
        'captchaText': f"{process_distance(distance)},{random.randint(-5, 5)}",
        'startX': start_x,
        'startY': start_y,
        'startTime': start_time
    }).replace(' ', '')

    resp = session.post(url_, data=payload).json()
    print(resp)
    if 'token' in set(resp.keys()):
        return resp['token']
    return None


def crack():
    # 初始化滑块
    init_data = _init_slider()
    # 获取缺口距离
    distance = _get_distance(init_data['slider_url'], init_data['captcha_url'])
    # 屏幕验证码尺寸比
    distance = int(round(distance * (404 / 500)))
    # 最终验证
    result = _slider_verify(distance)
    if result:
        return {
            'success': 1,
            'message': '校验通过! ',
            'data': {
                'token': result
            }
        }
    return {
        'success': 0,
        'message': '校验失败! ',
        'data': None
    }


if __name__ == '__main__':
    x = crack()
    print(x)
