# -*- coding: utf-8 -*-
# @Time    : 2019/10/3 21:13
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : geetest.py
# @Software: PyCharm

import requests
import json
import time
import base64
import random
from shumei.img_locate import _get_distance
from shumei.get_trace import generate_trace
from shumei.des import encrypt, decrypt

headers = {
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
        'organization': 'TKWQ4vmgC3PJLGDTMIoJ',
        'appId': 'default',
        'channel': 'DEFAULT',
        'lang': 'zh-cn',
        'model': 'slide',
        'rversion': '1.0.1',
        'sdkver': '1.1.2',
        'data': {},
        'callback': 'sm_{}'.format(int(time.time() * 1000))
    }
    resp = requests.get(url, params=params, headers=headers)
    result = json.loads(resp.text.replace('{}('.format(params['callback']), '').replace(')', ''))
    print('初始化结果: ', result)
    if result['riskLevel'] == 'PASS':
        return {
            'k': result['detail']['k'],
            'captcha_url': 'https://castatic.fengkongcloud.com{}'.format(result['detail']['bg']),
            'rid': result['detail']['rid']
        }
    return None


def _encrypt_trace(k, trace, distance):
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
    # 构造待加密数据
    data = {
        # 滑动距离 / 300
        "d": distance / 300,
        # 轨迹
        "m": trace,
        # 滑动所用时间
        "c": trace[-1][-1],
        # 验证码图片尺寸, 宽
        "w": 300,
        # 验证码图片尺寸, 高
        'h': 150,
        # 设备
        'os': 'web_pc',
        # 是否 webdriver
        "cs": 0,
        "wd": 0,
        'sm': -1
    }
    # 最后加密 DES
    return encrypt(new_key, json.dumps(data).replace(' ', ''))


def _slider_verify(act, rid):
    """
    验证
    :param act:
    :param rid:
    :return:
    """
    url = 'https://captcha.fengkongcloud.com/ca/v1/fverify'
    params = {
        "organization": "TKWQ4vmgC3PJLGDTMIoJ",
        "appId": "default",
        "channel": "DEFAULT",
        "act": act,
        "rid": rid,
        "lang": "zh-cn",
        "ostype": "web",
        "rversion": "1.0.1",
        "sdkver": "1.1.2",
        "callback": "sm_{}".format(int(time.time() * 1000)),
    }
    resp = requests.get(url, params=params, headers=headers)
    result = json.loads(resp.text.replace('{}('.format(params['callback']), '').replace(')', ''))
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
    distance = _get_distance(_init_data['captcha_url'])
    if not distance:
        return {
            'success': 0,
            'message': '缺口距离获取失败! ',
            'data': None
        }
    # time.sleep(random.uniform(0.01, 0.05))
    trace = generate_trace(distance)
    act = _encrypt_trace(_init_data['k'], trace, distance)
    rid = _init_data['rid']
    result = _slider_verify(act, rid)
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
