# -*- coding: utf-8 -*-
# @Time    : 2019/10/16 16:13
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : geetest.py
# @Software: PyCharm

import requests
import re
import json
from selenium import webdriver
import time
import random
from tongdun import img_locate
from tongdun.td_crypt import *

"""
同盾的加密代码是动态生成的, 每天都不一样
但是核心加密目前我只发现两套, 第一套是自定义的一套加密方式, 第二套是AES加密外加字符替换
"""


headers = {
    'Referer': 'https://x.tongdun.cn/onlineExperience/slidingPuzzle',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
}


# 初始化 data
data = {
    'blackBox': "eyJ2IjoiVTBnVjMvdlhucEZJUERZYUcxMlVVUjNzaXovYXRxVlNVdG5IU0FYaEI2Sy9qL3FLT1l2VWxzZDVKbWpYSnVzLyIsIm9zIjoid2ViIiwiaXQiOjkzOTY4LCJ0IjoiR2ZrWERvQzVCVWFRUTk2bGFoeUxtVFZxcERNSjRsdERIeTBZRUloSzIyNi9SeG5EN2t5OGg4eDRIc25kemxVOTl4RW9kUUh6VTNoYS9iYjRSZDBJVEE9PSJ9",
    'mouseInfo': '',
    'requestType': 1,
    'usedTime': None,
    'validateCodeObj': '^^',
    'userAnswer': None,
    "sensorInfo": None,
    'validateToken': None
}


def _reload_js():
    with open('td_slider.js', 'rb') as f:
        js = f.read().decode()
    ctx = execjs.compile(js)
    return ctx


def get_token_id():
    """
    利用 selenium 获取同盾设备指纹
    :return:
    """
    options = webdriver.ChromeOptions()
    options.add_argument('lang=zh_CN.UTF-8')
    options.add_argument('--headless')
    options.add_argument(
        'user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"'
    )
    driver = webdriver.Chrome(options=options)
    driver.get('https://x.tongdun.cn/onlineExperience/slidingPuzzle')
    time.sleep(1)
    html = driver.page_source
    # print(html)
    token_id = re.search('token_id=(.*?)&', html).group(1)
    return token_id


def format_data(enc_type, p2, token, data):
    """
    构造表单
    :param enc_type: 加密类型
    :param token: 设备指纹
    :return:
    """
    ctx = _reload_js()
    # 自定义加密
    if enc_type == 1:
        p1 = "{}^^{}^^tongdun^^x_tongdun2_web".format(
            "n13r6ttkNB9Anh67QYkg4Ixs9SU6Sv6dhAHuuaeK41DwtJSN0NmQx8DvWWk/TKeZ", token)
        key = generate_key(token)
        d = "103159^^|^^|^^" + str(int(time.time() * 1000))
        s = et(ctx, p1 + "^^" + p2) + f"^^{data['validateCodeObj'] if data['validateCodeObj'] else '|'}^^{data['userAnswer'] if data['userAnswer'] else '|'}^^{data['validateToken'] if data['validateToken'] else '|'}^^" + et(ctx, d)
        p3 = ft(ctx, s, key)
        p4 = ft(ctx, f"{data['sensorInfo'] if data['sensorInfo'] else '|'}^^{data['mouseInfo']}^^{data['usedTime'] if data['usedTime'] else '|'}", key)
        u = Pt(ctx, 8)
        p6 = ft(ctx, u + "https://x.tongdun.cn/onlineExperience/slidingPuzzle", key)
        p7 = et(ctx, p6) + et(ctx, d) + Pt(ctx, 32)
        p9 = ft(ctx, d, key)
    # AES 加密
    elif enc_type == 2:
        p1 = "{}^^{}^^tongdun^^x_tongdun2_web".format(
            "b37uCyfyme4S7TF/MVDRqSRxP4CB2BjsnDxr4bSxz0vSL/~hXNGID9Tr7vzaBm~F", token)
        aes_key = generate_aes_key(token)
        d = "151694^^|^^|^^" + str(int(time.time() * 1000))
        s = et(ctx, p1 + "^^" + p2) + f"^^{data['validateCodeObj'] if data['validateCodeObj'] else '|'}^^{data['userAnswer'] if data['userAnswer'] else '|'}^^{data['validateToken'] if data['validateToken'] else '|'}^^" + et(ctx, d)
        u = Pt(ctx, 8)
        p3 = aes_encrypt(aes_key, s)
        p4 = aes_encrypt(aes_key, f"{data['sensorInfo'] if data['sensorInfo'] else '|'}^^{data['mouseInfo']}^^{data['usedTime'] if data['usedTime'] else '|'}")
        p6 = aes_encrypt(aes_key, u + "https://x.tongdun.cn/onlineExperience/slidingPuzzle")
        p7 = et(ctx, p6) + et(ctx, d) + Pt(ctx, 32)
        p9 = aes_encrypt(aes_key, d)
    else:
        print('未实现的加密方式! ')
        return
    return p1, {
        'p3': p3,
        'p4': p4,
        'p5': 'web',
        'p6': p6,
        'p7': p7,
        'p8': u,
        'p9': p9
    }


def _generate_trace(distance):
    """
    生成轨迹
    :param distance: 缺口距离
    :return:
    """
    # 轨迹伪造方法已删除
    # 提示: 轨迹形式如下所示, 滑动轨迹起点 Action 为 12, 终点 Action 为 13、type 为 3
    # 不仅需要滑动轨迹, 还需要验证码生成后鼠标在屏幕内移动至点击滑块的轨迹
    for index, x in enumerate(tracks_list[:-1]):
        if not index:
            trace.append({
                'type': 1,
                'time': timestamp_list[index],
                'Action': 12,
                'op_x': x + start_x,
                'op_y': y_list[index] + start_y,
            })
        elif index == len(tracks_list) - 1:
            trace.append({
                'type': 3,
                'time': timestamp_list[index],
                'Action': 13,
                'op_x': x + start_x,
                'op_y': y_list[index] + start_y,
            })
        trace.append({
            'type': 1,
            'time': timestamp_list[index],
            'Action': '',
            'op_x': x + start_x,
            'op_y': y_list[index] + start_y,
        })
    return trace


def _init_slider(enc_type, token):
    """
    初始化滑块
    :param enc_type: 使用加密的类型
    :return:
    """
    url = 'https://sphinx.tongdun.net/sphinx/validatecode/v1'
    p2 = data['blackBox'] + "^^1^^1^^1"  # 代表该页面首次生成验证码, 若第一次刷新验证码, 则为 "^^2^^1^^1", 依此类推

    p1, post_data = format_data(enc_type, p2, token, data)
    params = {
        'p1': p1,
        'p2': p2
    }
    resp = requests.post(url, params=params, data=post_data, headers=headers).json()
    if resp['success']:
        print('滑块初始化成功! ')
        return resp
    return None


def _slider_verify(enc_type, token, init_data, distance, start_time):
    """
    最终验证
    :param enc_type:
    :param token:
    :param init_data:
    :param start_time
    :return:
    """
    url = 'https://sphinx.tongdun.net/sphinx/validatecode/v1'
    p2 = data['blackBox'] + "^^3^^1^^1"  # 代表该页面首次生成验证码, 若第一次刷新验证码, 则为 "^^2^^1^^1", 依此类推

    # 伪造轨迹, 不仅是滑动轨迹, 还有鼠标在整个屏幕内的移动轨迹
    trace = _generate_trace(distance)
    data.update({
        'requestType': 3,
        'validateCodeObj': json.dumps(init_data['validateCodeObj']),
        'mouseInfo': encrypt_trace(init_data['validateCodeObj']['slideY'], trace, start_time),
        'userAnswer': f"{distance}|10|{int(time.time() * 1000)}",
        'usedTime': int(time.time()) * 1000 - start_time
    })
    # print(data)
    p1, post_data = format_data(enc_type, p2, token, data)
    params = {
        'p1': p1,
        'p2': p2
    }
    resp = requests.post(url, params=params, data=post_data, headers=headers).json()
    print(resp)
    if resp['success']:
        if not resp['needValidateCode']:
            return resp['validateToken']
        else:
            print('验证失败, 已刷新! ')
            return None
    return None


def crack():
    # 获取 token
    token = get_token_id()
    print('设备指纹: ', token)
    # 初始化数据
    init_data = _init_slider(2, token)
    print('初始化滑块数据: ', init_data)
    # 处理验证码获取缺口距离
    start_time = int(time.time() * 1000)
    distance = img_locate.get_distance(init_data)
    print('缺口距离: ', distance)
    result = _slider_verify(2, token, init_data, distance, start_time)
    if result:
        return {
            'success': 1,
            'message': '校验通过! ',
            'data': {
                'validateToken': result
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
