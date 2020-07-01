# -*- coding: utf-8 -*-
# @Time    : 2019/10/18 10:58
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : geetest.py
# @Software: PyCharm

import json
import time
import requests
from city58.chaojiying import image_to_text
from city58.img_locate import get_distance, process_img
from city58.c58_crypt import aes_encrypt
from city58.get_trace import *

session = requests.session()
session.headers = {
    'referer': 'https://passport.58.com/forgetpassword',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
}


def get_session():
    """
    获取 session_id, 58同城密码修改页面滑块
    :return:
    """
    url = 'https://passport.58.com/58/forget/pc/init'
    params = {
        'source': 'passport',
        'path': 'http%3A%2F%2Fmy.58.com%2F%3Fpts%3D1571366746990',
        'psdk-d': 'jsdk',
        'psdk-v': '1.0.2',
        'callback': ''
    }
    resp = session.get(url, params=params)
    result = json.loads(resp.text.replace('(', '').replace(')', ''))
    if result['code'] == 2578:
        return result['data']['scid']
    return None


def get_token():
    """
    获取页面 token
    :return:
    """
    url = 'https://cdata.58.com/fpToken?callback='
    resp = session.get(url)
    result = json.loads(resp.text.replace('(', '').replace(')', ''))
    if result['status'] == 'success':
        return result['token']
    return None


def init_captcha(session_id):
    """
    初始化验证码
    :param session_id:
    :return:
    """
    url = 'https://verifycode.58.com/captcha/getV3'
    params = {
        'callback': '',
        'showType': 'embed',
        'sessionId': session_id,
        '_': int(time.time() * 1000)
    }
    resp = session.get(url, params=params)
    result = json.loads(resp.text.replace('(', '').replace(')', ''))
    if result['message'] == '成功':
        if result['data']['level'] == 310:
            print('触发滑块验证! ')
            return {
                'type': 'slide',
                'captcha_url': result['data']['bgImgUrl'],
                'slider_url': result['data']['puzzleImgUrl'],
                'response_id': result['data']['responseId']
            }
        elif result['data']['level'] == 320:
            print('触发点选验证! ')
            return {
                'type': 'click',
                'captcha_url': result['data']['bgImgUrl'],
                'response_id': result['data']['responseId']
            }
        elif result['data']['level'] == 330:
            print('触发手势验证! ')
            return {
                'type': 'gesture',
                'captcha_url': result['data']['bgImgUrl'],
                'response_id': result['data']['responseId']
            }
    return None


def format_slide_text(token, distance, trace):
    """
    构造滑动验证加密字符串
    :param token:
    :param distance:
    :param trace
    :return:
    """
    return json.dumps({
        'x': str(distance),
        'track': trace,
        'p': '0,0',
        'finger': token
    }).replace(' ', '')


def format_click_text(position):
    """
    构造点选验证加密字符串
    :param position:
    :return:
    """
    return json.dumps({
        'r': "25",
        'p': position,
        'track': '|'.join([p + f',{random.randint(600, 700)}' for p in position.split('|')])
    }).replace(' ', '')


def _captcha_verify(response_id, session_id, text):
    """
    最终验证
    :param response_id:
    :param session_id:
    :param text:
    :return:
    """
    url = 'https://verifycode.58.com/captcha/checkV3'
    params = {
        'callback': '',
        'responseId': response_id,
        'sessionId': session_id,
        'data': aes_encrypt(response_id[0: 16], response_id[0: 16], text)
    }
    resp = session.get(url, params=params)
    result = json.loads(resp.text.replace('(', '').replace(')', ''))
    print(result)
    if result['message'] == '校验成功':
        return result['data']['successToken']
    return None


def main():
    # 获取 session_id
    session_id = get_session()
    # 获取 token 签名
    token = get_token()
    # 初始化验证码
    init_data = init_captcha(session_id)
    if init_data['type'] == 'slide':
        # 获取缺口距离
        distance = get_distance(init_data['slider_url'], init_data['captcha_url'])
        # 屏幕图片尺寸比
        distance = round(distance * (280 / 480))
        # 伪造轨迹
        trace = generate_slide_trace(distance)
        new_trace = process_trace(trace)
        # 构造加密字符串
        text = format_slide_text(token, distance, new_trace)
    elif init_data['type'] == 'click':
        # 下载验证码并重置尺寸
        captcha_url = 'https://verifycode.58.com' + init_data['captcha_url']
        img_data = process_img(captcha_url, init_data['type'])
        # 超级鹰识别点选位置
        ok, position = image_to_text(img_data)
        if ok:
            # 构造加密字符串
            text = format_click_text(position)
        else:
            return {
                'success': 0,
                'message': '点选验证位置识别失败! ',
                'data': None
            }
    elif init_data['type'] == 'gesture':
        # 下载验证码并重置尺寸
        captcha_url = 'https://verifycode.58.com' + init_data['captcha_url']
        img_data = process_img(captcha_url, init_data['type'])
        # 超级鹰识别点选位置
        ok, position = image_to_text(img_data, img_kind=9004)
        if ok:
            position = [i for i in position.split('|')]
            # 伪造轨迹
            distance, trace = generate_gesture_trace(position)
            # 构造加密字符串
            text = format_slide_text(token, distance, trace)
        else:
            return {
                'success': 0,
                'message': '手势验证轮廓识别失败! ',
                'data': None
            }
    else:
        return {
            'success': 0,
            'message': '未知验证类型! ',
            'data': None
        }
    # 最终验证
    result = _captcha_verify(init_data['response_id'], session_id, text)
    if result:
        return {
            'success': 1,
            'message': '校验通过! ',
            'data': {
                'successToken': result
            }
        }
    return {
        'success': 0,
        'message': '校验失败! ',
        'data': None
    }


if __name__ == '__main__':
    x = main()
    print(x)
