# -*- coding: utf-8 -*-
# @Time    : 2019/10/23 21:44
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : geetest.py
# @Software: PyCharm


import execjs
import json
import time
import random
import os
import requests
from PIL import Image
import cv2
import numpy as np


session = requests.session()
session.headers = {
    'Cookie': 'uc_l_token=3f608886-4f78-42aa-a74d-bb73076a16b7; BIGipServerP_ucapache=!RPhhdg/fig5hTHVObK2MiI46Ur2DR+ceaDaWLhRQEqFf/oBqmwYqulUtF37NTZMy1GRcZqBCTeYStA==; newInjectAttr=01lsMCfkOii8UUfmKmd+aVnmxLnqnO0SQIN0eprHPOYdI5YLBgTkloRZOB1myRcJr312; _dest_ver=unknown; dfp_t_c=1571833231955; dvs_v_t=1571833231944; dfpSessionId=110001D006rRHXOrnFtgsX39Pl7m11571833233239',
    'Referer': 'https://user.95516.com/pages/login/?sysIdStr=K1vjtj1xNKvaLzh&service=https%3A%2F%2Fwww.95516.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
}


def _init_session():
    """
    初始化请求 session
    :return:
    """
    url = 'https://user.95516.com/ucsso/initcap/'

    resp = session.post(url).json()
    return resp['sesId']


def _init_slider(session_id):
    """
    初始化滑块
    :param session_id:
    :return:
    """
    url = 'https://captcha.95516.com/session/initcap'

    params = {
        'callback': '',
        'v': int(time.time() * 1000),
        'cType': 0,
        'cVersion': '1.0.0',
        'sesId': session_id
    }

    resp = session.get(url, params=params)
    result = json.loads(resp.text.replace('(', '').replace(')', ''))
    if result['resCode'] == '0000':
        return result['resData']['capId']
    return None


def _pic_download(cap_id, type):
    """
    图片下载
    :param cap_id: 验证码 ID
    :param type:
    :return:
    """
    save_path = os.path.abspath('...') + '\\' + 'images'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    img_path = save_path + '\\' + '{}.jpg'.format(type)
    img_data = requests.get(f'https://captcha.95516.com/media?mediaId={"m" if type == "captcha" else "s"}{cap_id}.png').content
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


def get_distance(cap_id):
    """
    获取缺口距离
    :param cap_id:
    :return:
    """
    save_path = os.path.abspath('...') + '\\' + 'images'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # 引用上面的图片下载
    slider_path = _pic_download(cap_id, 'slider')

    # 引用上面的图片下载
    captcha_path = _pic_download(cap_id, 'captcha')

    # 计算拼图还原距离
    target = cv2.imread(slider_path, 0)
    template = cv2.imread(captcha_path, 0)
    temp = save_path + '\\' + 'temp.jpg'
    targ = save_path + '\\' + 'targ.jpg'
    cv2.imwrite(targ, target)
    w, h = _cut_slider(slider_path)
    cv2.imwrite(temp, template)
    target = cv2.imread(targ)
    target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    # target = abs(255 - target)
    cv2.imwrite(targ, target)
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
    imagecrop.save(save_path + '\\' + "new_image.jpg")
    imagecrop.show()
    return int(round(y))


def _generate_trace(distance):
    """
    生成轨迹
    :param distance:
    :return:
    """
    # 初速度
    v = 0
    # 位移/轨迹列表，列表内的一个元素代表0.02s的位移
    tracks_list = []
    # 当前的位移
    current = 0
    while current < distance - 13:
        # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
        a = random.randint(10000, 12000)  # 加速运动
        # 初速度
        v0 = v
        t = random.randint(9, 18)
        s = v0 * t / 1000 + 0.5 * a * ((t / 1000) ** 2)
        # 当前的位置
        current += s
        # 速度已经达到v,该速度作为下次的初速度
        v = v0 + a * t / 1000
        # 添加到轨迹列表
        if current < distance:
            tracks_list.append(round(current))
    # 减速慢慢滑
    if round(current) < distance:
        for i in range(round(current) + 1, distance + 1):
            tracks_list.append(i)
    else:
        for i in range(tracks_list[-1] + 1, distance + 1):
            tracks_list.append(i)
    # 生成时间戳列表
    timestamp_list = []
    timestamp = 0
    for i in range(len(tracks_list)):
        t = random.choice([7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 8, 8, 8])
        timestamp += t
        timestamp_list.append(timestamp)
        i += 1
    y_list = []
    zy = 0
    for j in range(len(tracks_list)):
        y = random.choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0])
        zy += y
        y_list.append(zy)
        j += 1
    trace = [[-random.randint(0, 20), -random.randint(70, 85), 0], [0, 0, 0], [0, 0, 0]]
    for index, x in enumerate(tracks_list[:-1]):
        trace.append([x, y_list[index], timestamp_list[index]])
    trace.append([distance, y_list[-1], timestamp_list[-2] + random.randint(10, 20)])
    return trace


def _encrypt_bhv(trace):
    """
    加密轨迹
    :param trace:
    :return:
    """
    with open('ysf_slider.js', 'rb') as f:
        js = f.read().decode()
    ctx = execjs.compile(js)
    return ctx.call('getCompress', trace)


def _slider_verify(session_id, distance):
    """
    滑块验证
    :param session_id:
    :param distance:
    :return:
    """
    url = 'https://captcha.95516.com/session/vfy'

    trace = _generate_trace(distance)
    params = {
        'callback': '',
        'v': int(time.time() * 1000),
        'sesId': session_id,
        'passTime': random.randint(1500, 2000),
        'value': distance,
        'bhv': _encrypt_bhv(trace)
    }
    resp = session.get(url, params=params)
    result = json.loads(resp.text.replace('(', '').replace(')', ''))
    print(result)
    if result['resCode'] == '0000':
        return result['resData']
    return None


def crack():
    # 初始化页面
    session_id = _init_session()
    # 初始化滑块
    cap_id = _init_slider(session_id)
    # 获取缺口
    distance = get_distance(cap_id)
    # 最终验证
    result = _slider_verify(session_id, distance)

    if result:
        return {
            'success': 1,
            'message': '校验通过! ',
            'data': result
        }
    return {
        'success': 0,
        'message': '校验失败! ',
        'data': None
    }


if __name__ == '__main__':
    x = crack()
    print(x)
