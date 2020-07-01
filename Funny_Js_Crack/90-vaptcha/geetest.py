# -*- coding: utf-8 -*-
# @Time    : 2019/10/19 11:19
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : geetest.py
# @Software: PyCharm

import requests
import json
import os
import execjs
import random
from PIL import Image
from vaptcha.get_trace import generate_trace
from vaptcha.chaojiying import image_to_text


headers = {
    'Referer': 'https://www.vaptcha.com/demo/popup',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
}


def get_challenge():
    """
    获取验证码签名参数
    :return:
    """
    url = 'https://api.vaptcha.com/v2/config'

    params = {
        'id': '5b4d9dfea485e5041019253f',
        'type': 'popup',
        'scene': '',
        'callback': ''
    }

    resp = requests.get(url, headers=headers, params=params)
    result = json.loads(resp.text.replace('(', '').replace(')', ''))
    return result['challenge']


def init_vaptcha(challenge):
    """
    初始化验证码
    :param challenge:
    :return:
    """
    url = 'https://api.vaptcha.com/v2/click'

    params = {
        'id': '5b4d9dfea485e5041019253f',
        'challenge': challenge,
        'callback': ''
    }
    resp = requests.get(url, params=params, headers=headers)
    result = json.loads(resp.text.replace('(', '').replace(')', ''))
    return result


def _pic_download(url, type):
    """
    图片下载
    :param url:
    :param type:
    :return:
    """
    img_path = os.path.abspath('...') + '\\' + '{}.jpg'.format(type)
    img_data = requests.get(url).content
    with open(img_path, 'wb') as f:
        f.write(img_data)
    return img_path


def _slider_verify(challenge, trace):
    """
    手势验证
    :param challenge:
    :param trace:
    :return:
    """
    url = 'https://api.vaptcha.com/v2/verify'
    with open('v_slider.js', 'rb') as f:
        js = f.read().decode()
    ctx = execjs.compile(js)
    params = {
        'v': ctx.call('assemblyCoordData', trace),
        'id': '5b4d9dfea485e5041019253f',
        'challenge': challenge,
        'drawtime': random.randint(1300, 2000),
        'callback': ''
    }
    resp = requests.get(url, headers=headers, params=params)
    result = json.loads(resp.text.replace('(', '').replace(')', ''))
    print(result)
    if result['code'] == '0103':
        return result['token']
    return None


def crack():
    # 获取验证码 ID 签名
    challenge = get_challenge()
    # 初始化验证码
    init_data = init_vaptcha(challenge)
    # 下载验证码
    img_path = _pic_download('https://cdn.vaptcha.com/' + init_data['img'], 'vaptcha')
    img = Image.open(img_path)
    # img.show()

    # 使用超级鹰识别
    img_data = open(img_path, 'rb').read()
    ok, result = image_to_text(img_data, img_kind=9004)
    position = [x for x in result.split('|')]
    print('超级鹰识别结果: ', result)
    if ok and len(position) == 4:
        trace = generate_trace(position, img.size)
        # print(trace)
        result = _slider_verify(challenge, trace)
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
            'data': {
                'token': None
            }
        }
    return {
        'success': 0,
        'message': '验证码识别失败! ',
        'data': None
    }


if __name__ == '__main__':
    x = crack()
    print(x)
