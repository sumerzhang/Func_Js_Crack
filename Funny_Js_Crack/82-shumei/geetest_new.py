# -*- coding: utf-8 -*-
# @Time    : 2019/11/1 18:52
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : geetest_new.py
# @Software: PyCharm

import requests
import json
import time
import base64
import random
from shumei.des import encrypt, decrypt
from shumei.img_locate import get_distance
from shumei.get_trace import _generate_trace

session = requests.session()
session.headers = {
    "Referer": "https://www.fengkongcloud.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
}


def _init_slider():
    """
    初始化验证码
    :return:
    """
    url = 'https://captcha.fengkongcloud.com/ca/v1/register'
    params = {
        'organization': 'RlokQwRlVjUrTUlkIqOg',
        'appId': 'default',
        'channel': 'DEFAULT',
        'lang': 'zh-cn',
        'model': 'slide',
        'rversion': '1.0.1',
        'sdkver': '1.1.2',
        'data': {},
        'callback': 'sm_{}'.format(int(time.time() * 1000))
    }
    resp = session.get(url, params=params)
    result = json.loads(resp.text.replace('{}('.format(params['callback']), '').replace(')', ''))
    print('初始化结果: ', result)
    if result['riskLevel'] == 'PASS':
        return {
            'k': result['detail']['k'],
            'captcha_url': 'https://castatic.fengkongcloud.com{}'.format(result['detail']['bg']),
            'slider_url': 'https://castatic.fengkongcloud.com{}'.format(result['detail']['fg']),
            'rid': result['detail']['rid']
        }
    return None


def _encrypt_data(k, trace, distance):
    """
    加密轨迹
    :param k: 初始密钥
    :param trace: 轨迹
    :param distance: 距离
    :return:
    """
    # 对 k 值进行 base64 解码
    text = base64.b64decode(k)
    # 对解码后的 k 值进行 DES 解密（密钥: sshummei）, 取前8位作为下一次加密的密钥
    new_key = decrypt('sshummei', text)[:8]
    # 构造加密数据
    return {
        # 滑动距离 / 300
        "hz": encrypt(new_key, str(distance / 300)),
        # 轨迹
        "wa": encrypt(new_key, json.dumps(trace).replace(' ', '')),
        # 滑动所用时间
        "co": encrypt(new_key, str(trace[-1][-1] + random.randint(30, 70))),
        # 验证码图片尺寸, 宽
        "mn": encrypt(new_key, "300"),
        # 验证码图片尺寸, 高
        "us": encrypt(new_key, "150"),
        # 是否 webdriver
        "oq": encrypt(new_key, '0'),
        "et": encrypt(new_key, '0'),
        "bm": encrypt(new_key, '-1'),
        "ml": encrypt(new_key, '"default"'),
        "fd": encrypt(new_key, '"DEFAULT"'),
        "ep": encrypt(new_key, '"zh-cn"')
    }


def _slider_verify(encrypt_data, rid):
    """
    验证
    :param encrypt_data:
    :param rid:
    :return:
    """
    url = 'https://captcha.fengkongcloud.com/ca/v2/fverify'
    encrypt_data.update({
        'organization': 'RlokQwRlVjUrTUlkIqOg',
        'callback': 'sm_{}'.format(int(time.time() * 1000)),
        'ostype': 'web',
        'rid': rid,
        'sdkver': '1.1.2',
        'rversion': '1.0.1',
        'protocol': 1,
        'act.os': 'web_pc'
    })
    resp = session.get(url, params=encrypt_data)
    result = json.loads(resp.text.replace('{}('.format(encrypt_data['callback']), '').replace(')', ''))
    return result


def crack():
    """
    滑块验证
    :return:
    """
    while True:
        _init_data = _init_slider()
        if _init_data:
            break
        time.sleep(random.random())
    distance = get_distance(_init_data['captcha_url'])
    distance = int(round(distance * (300 / 600)))
    print('缺口距离: ', distance)
    if not distance:
        return {
            'success': 0,
            'message': '缺口距离获取失败! ',
            'data': None
        }
    trace = _generate_trace(distance)
    rid = _init_data['rid']
    encrypt_data = _encrypt_data(_init_data['k'], trace, distance)
    result = _slider_verify(encrypt_data, rid)
    print('校验结果: ', result)
    if result['riskLevel'] == 'PASS':
        return {
            'success': 1,
            'message': '校验成功! ',
            'data': rid
        }
    return {
        'success': 0,
        'message': '校验失败! ',
        'data': None
    }


if __name__ == '__main__':
    x = crack()
    print(x)
