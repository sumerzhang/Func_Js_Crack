# -*- coding: utf-8 -*-
# @Time    : 2019/10/12 18:16
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : geetest.py
# @Software: PyCharm


import execjs
from PIL import Image
import requests
import random
import json
import time


headers = {
    'Content-Type': 'application/x-www-form-urlencoded;',
    'Origin': 'https://portal.mogu.com',
    'Referer': 'https://portal.mogu.com/user/newlogin?redirect_url=https%3A%2F%2Fwww.mogu.com%2F&ptp=31.v5mL0b.0.0.sjRcapVp',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
}


def _fake_trace(click_list):
    """
    根据点击次数伪造轨迹
    :param click_list: 每张图片点击次数列表
    :return: 在验证码上移动的轨迹
    """
    # 轨迹构造已删除, 请自行编写, 提示: [-1, -1, -1, 0] 开头, 点击位置处停留时间稍长
    # 轨迹样式:
    trace = [[-1, -1, -1, 0], [110, 33, 1571136448228, 1], [115, 33, 696, 2], [129, 33, 17, 2], [137, 33, 16, 2], [145, 33, 17, 2]]
    return trace


def encrypt(data, cap_key):
    """
    加密
    :param data: 待加密数据
    :param cap_key: 验证码 ID
    :return:
    """
    with open('mgj_encrypt.js', 'rb') as f:
        js = f.read().decode()
    ctx = execjs.compile(js)
    return ctx.call('encrypt', data, cap_key)


def get_auth(data):
    """
    签名验证
    :param data:
    :return:
    """
    with open('get_auth.js', 'rb') as f:
        js = f.read().decode()
    ctx = execjs.compile(js)
    return ctx.call('get_auth', data)


def get_cap_key():
    """
    获取验证码初始化 ID
    :return:
    """
    url = 'https://shieldcaptain.mogu.com/gettoken'

    params = {
        'auth': get_auth({}),
        '_': int(time.time() * 1000),
        'callback': ''
    }

    resp = requests.get(url, params=params, headers=headers)
    try:
        result = json.loads(resp.text.replace('(', '').replace(')', ''))
        cap_key = result['capkey']
        return cap_key
    except:
        return None


def _download_captcha(cap_key):
    """
    下载验证码图片
    :param cap_key: 验证码 ID
    :return:
    """
    url = 'https://shieldcaptain.mogu.com/getimage'

    params = {
        'code': cap_key,
        'auth': get_auth({'code': cap_key})
    }
    imgdata = requests.get(url, params=params, headers=headers).content

    with open('captcha.jpg', 'wb') as f:
        f.write(imgdata)

    img = Image.open('captcha.jpg')
    img.show()


def _input_click():
    """
    输入点击次数
    :return:
    """
    click_times = []
    x1 = input('请输入第一张图片需要点击几次 >> \n')
    click_times.append(int(x1))
    x2 = input('请输入第二张图片需要点击几次 >> \n')
    click_times.append(int(x2))
    x3 = input('请输入第三张图片需要点击几次 >> \n')
    click_times.append(int(x3))
    x4 = input('请输入第四张图片需要点击几次 >> \n')
    click_times.append(int(x4))

    return click_times


def _click_verify(cap_key, click_times):
    """
    最终验证
    :param cap_key: 验证码 ID
    :param click_times: 点击次数
    :return:
    """
    url = 'https://shieldcaptain.mogu.com/validate'

    trace = _fake_trace(click_times)

    data = {
        'probc': cap_key,
        # 最后需要反转一下, 加密的是翻转的列表
        'probd': encrypt(click_times[::-1], cap_key),
        'probe': encrypt(trace, cap_key),
        'probf': encrypt([[-1, -1, -1, 0]], cap_key),
        'probg': encrypt([[-1, -1, -1, 0]], cap_key),
    }
    auth = get_auth(data)
    data['auth'] = auth

    resp = requests.post(url, data=data, headers=headers).json()
    print(resp)
    if resp['ret'] == 'SUCCESS':
        return resp['data']['captkey']
    return None


def click():
    # 获取验证码 ID
    cap_key = get_cap_key()
    # 下载验证码并显示
    _download_captcha(cap_key)
    # 手动输入点击次数
    click_times = _input_click()
    # 最终验证
    result = _click_verify(cap_key, click_times)
    if result:
        return {
            'success': 1,
            'message': '校验通过! ',
            'data': {
                'captkey': result
            }
        }
    return {
        'success': 0,
        'message': '校验失败! ',
        'data': None
    }


if __name__ == '__main__':
    x = click()
    print(x)
