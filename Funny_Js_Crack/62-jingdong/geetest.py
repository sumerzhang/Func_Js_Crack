# -*- coding: utf-8 -*-
# @Time    : 2019/9/28 10:56
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : geetest.py
# @Software: PyCharm


import requests
import json
import execjs
import re
from jingdong.img_locate import get_distance
from jingdong.get_trace import *


session = requests.Session()
session.headers = {
    'Connection': 'keep-alive',
    'Referer': 'https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fh5.m.jd.com%2Fpc%2Fdev%2F3mr2iWXgiWcZvyGYrQAoYp3KXAaq%2Findex.html%3Futm_source%3Dkong%26utm_medium%3Dzssc%26utm_campaign%3Dt_1000023384_100757%26utm_term%3D36f20e86-5b4d-4b6e-8fba-d79e6c2654a9-p_1999-pr_1646-at_100757%26jd_pop%3D36f20e86-5b4d-4b6e-8fba-d79e6c2654a9%26abt%3D0',
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
}


def get_session_id():
    """
    获取设备指纹 _jdtdmap_sessionId
    :return:
    """
    response = session.get("https://seq.jd.com/jseqf.html?bizId=passport_jd_com_login_pc&platform=js&version=1")
    session_id = re.findall(r'_jdtdmap_sessionId="(.*?)"', response.text)[0]
    return session_id


def _init_slider():
    """
    初始化滑块
    :return:
    """
    url = 'https://iv.jd.com/slide/g.html'
    params = {
        'appId': '1604ebb2287',
        'scene': 'login',
        'product': 'click-bind-suspend',
        'e': 'Q2NDKJBVGRE5UMX3OJJRO6BV6UVQBMIFTJ3D2UJKVYHJMWPOMZYIUY43WWNWPEKLNC6UL62ABWCUBISUNMCQBEQUUQ',
        'lang': 'zh_CN',
        'callback': ''
    }
    resp = session.get(url, params=params)
    init_data = json.loads(resp.text.replace("(", "").replace(")", ""))
    return init_data


def _encrypt_trace(trace):
    """
    加密轨迹, 生成参数 d
    :return:
    """
    with open('jd_slider.js', 'r') as f:
        js = f.read()

    ctx = execjs.compile(js)
    return ctx.call('encrypt_trace', trace)


def _slider_verify(d, challenge, session_id):
    """
    滑块验证
    :param d: 加密轨迹
    :param challenge: 验证码签名
    :param session_id: 设备指纹
    :return:
    """
    url = "https://iv.jd.com/slide/s.html?"
    params = {
        "d": d,
        "c": challenge,
        "w": 278,
        "appId": "1604ebb2287",
        "scene": "login",
        "product": "click-bind-suspend",
        "e": 'Q2NDKJBVGRE5UMX3OJJRO6BV6UVQBMIFTJ3D2UJKVYHJMWPOMZYIUY43WWNWPEKLNC6UL62ABWCUBISUNMCQBEQUUQ',
        "s": session_id,
        "o": 'xxx',  # 账号
        "lang": 'zh_CN',
        "callback": ''
    }
    response = session.get(url, params=params)
    result = json.loads(response.text.replace("(", "").replace(")", ""))
    print(result)
    return result


def crack():
    # 获取设备指纹
    session_id = get_session_id()
    # 初始化滑块
    init_data = _init_slider()
    # 获取缺口距离
    distance = get_distance(init_data['patch'], init_data['bg'])
    # 屏幕图片尺寸比
    distance = round(distance * (278 / 360))
    # print(distance)
    # 伪造轨迹
    trace = get_trace(distance)
    # trace = generate_trace(distance)
    # print(trace)
    d = _encrypt_trace(trace)
    time.sleep(2)
    result = _slider_verify(d, init_data['challenge'], session_id)
    if "validate" not in result.keys():
        return {
            'success': 0,
            'message': '校验失败: {}'.format(result["message"]),
            'data': None
        }
    return {
        'success': 1,
        'message': '校验成功! ',
        'data': {
            "validate": result["validate"],
            "challenge": init_data["challenge"],
        }
    }


if __name__ == '__main__':
    x = crack()
    print(x)
