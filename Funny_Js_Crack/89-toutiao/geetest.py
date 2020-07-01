# -*- coding: utf-8 -*-
# @Time    : 2019/10/19 22:32
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : geetest.py
# @Software: PyCharm

import os
import requests
import json
import time
import cv2
from PIL import Image
import random
import numpy as np

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://sso.toutiao.com',
    'Connection': 'keep-alive',
    'Referer': 'https://sso.toutiao.com/'
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
    img_data = requests.get(url).content
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


def generate_trace(distance, tip_y, start_time):
    """
    伪造轨迹
    :param distance:
    :param tip_y:
    :param start_time:
    :return:
    """
    # 轨迹删除
    trace = []
    for index, x in enumerate(tracks_list):
        trace.append({
            'relative_time': timestamp_list[index] - start_time,
            'x': int(x),
            'y': tip_y
        })
    trace.append({
        'relative_time': timestamp_list[-1] - start_time + random.randint(80, 140),
        'x': tracks_list[-1],
        'y': tip_y
    })
    return trace


def _init_slider():
    """
    初始化滑块
    :return:
    """
    url = 'https://verify.snssdk.com/get'

    params = {
        'external': '',
        'fp': 'c8076ff7da5bd4d49e6a5031fa98b9b9',
        'aid': 1768,
        'lang': 'zh',
        'app_name': 'sso',
        'iid': 0,
        'vc': '1.0',
        'did': 0,
        'uid': 0,
        'ch': 'pc_slide',
        'os': 2,
        'challenge_code': 1105,
        '_': int(time.time() * 1000)
    }

    resp = requests.get(url, params=params, headers=headers).json()
    if resp['ret'] == 200:
        return {
            'cid': resp['data']['id'],
            'captcha_url': resp['data']['question']['url1'],
            'slider_url': resp['data']['question']['url2'],
            'tip_y': resp['data']['question']['tip_y']
        }
    return None


def _slider_verify(cid, trace):
    """
    滑块验证
    :param cid: 验证码 id
    :param trace: 轨迹
    :return:
    """
    url = 'https://verify.snssdk.com/verify'

    params = {
        'external': '',
        'fp': 'c8076ff7da5bd4d49e6a5031fa98b9b9',
        'aid': 1768,
        'lang': 'zh',
        'app_name': 'sso',
        'iid': 0,
        'vc': '1.0',
        'did': 0,
        'uid': 0,
        'ch': 'pc_slide',
        'os': 2,
        'challenge_code': 1105,
    }
    data = json.dumps({
        "modified_img_width": 268,
        "id": cid,
        "mode": "slide",
        "reply": trace
    }).replace(' ', '')
    resp = requests.post(url, params=params, headers=headers, data=data).json()
    print(resp)
    if resp['msg'] == '验证通过':
        return cid
    return None


def crack():
    # 初始化滑块
    init_data = _init_slider()
    # 获取缺口距离
    distance = get_distance(init_data['slider_url'], init_data['captcha_url'])
    # 模拟人为延时
    start_time = int(time.time() * 1000)
    time.sleep(random.uniform(0.02, 0.05))
    # 伪造轨迹
    trace = generate_trace(distance, init_data['tip_y'], start_time)
    # 模拟人为延时, 停顿 1 到 2 秒, 很重要
    time.sleep(random.randint(1, 2))
    result = _slider_verify(init_data['cid'], trace)
    if result:
        return {
            'success': 1,
            'message': '校验通过! ',
            'data': {
                'id': result
            }
        }
    return {
        'success': 0,
        'message': '校验失败! ',
        'data': None
    }


def main():
    print('开始测试...')
    print('=' * 100)
    num = 1
    success = 0
    while num <= 1000:
        x = crack()
        print(x)
        if x['success']:
            success += 1
        num += 1
        time.sleep(random.uniform(1.5, 3))
    print('最后测试结果 >> %.2f%%' % success)


if __name__ == '__main__':
    main()

