# -*- coding: utf-8 -*-
# @Time    : 2019/10/22 20:41
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : geetest.py
# @Software: PyCharm


import os
import requests
import base64
import time
import re
from PIL import Image
import cv2
import numpy as np

session = requests.session()
session.headers = {
    'Referer': 'https://my.ztgame.com/plugin/pwd',
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


def get_distance(slider_url, captcha_url):
    """
    获取缺口距离
    :param slider_url:
    :param captcha_url:
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
    w, h = target.shape[::-1]

    temp = save_path + '\\' + 'temp.jpg'
    targ = save_path + '\\' + 'targ.jpg'
    cv2.imwrite(temp, template)
    cv2.imwrite(targ, target)
    target = cv2.imread(targ)
    target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    target = abs(255 - target)
    cv2.imwrite(targ, target)
    template = cv2.imread(temp)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    template = abs(255 - template)
    cv2.imwrite(temp, template)
    target = cv2.imread(targ)
    template = cv2.imread(temp)
    result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
    x, y = np.unravel_index(result.argmax(), result.shape)

    # 调用PIL Image 做测试
    image = Image.open(captcha_path)

    xy = (y, x, y + w, x + h)
    # 切割
    imagecrop = image.crop(xy)
    # 保存切割的缺口
    imagecrop.save(save_path + '\\' + "new_image.png")
    # imagecrop.show()
    return y


def _init_slider():
    """
    初始化滑块
    :return:
    """
    url = 'https://nocaptcha.ztgame.com/nocaptcha/init'

    params = {
        'version': '0.0.1',
        'callback': '',
        'appid': 'my',
        'element': '.captcha',
        'type': 'verifydrag',
        'width': '292px',
        'height': '240px',
        'mode': 'embed',
        '_': int(time.time() * 1000)
    }

    resp = session.get(url, params=params).json()

    if resp['code'] == 0:
        html = resp['html']
        imgs = re.findall(r'url\((.*?)\);', html)

        return {
            'nonce': resp['nonce'],
            'captcha_url': 'https:' + imgs[0],
            'slider_url': 'https:' + imgs[1]
        }
    return None


def _slider_verify(nonce, distance):
    """
    滑块验在
    :param nonce: 验证码 ID
    :param distance: 缺口距离
    :return:
    """
    url = 'https://nocaptcha.ztgame.com/nocaptcha/verify'

    params = {
        'version': '0.0.1',
        'appid': 'my',
        'input': base64.b64encode(str(distance).encode()).decode(),
        'nonce': nonce,
        'callback': '',
        '_': int(time.time() * 1000)
    }

    resp = session.get(url, params=params).json()
    print(resp)
    if resp['code'] == 0:
        return resp['token']
    return None


def crack():
    # 初始化滑块
    init_data = _init_slider()
    # 获取缺口距离
    distance = get_distance(init_data['slider_url'], init_data['captcha_url'])
    # 最终验证
    result = _slider_verify(init_data['nonce'], distance)
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
