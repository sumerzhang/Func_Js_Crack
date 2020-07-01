# -*- coding: utf-8 -*-
# @Time    : 2019/10/24 21:29
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : geetest.py
# @Software: PyCharm

import execjs
import json
import time
import random
import re
import requests
from bs4 import BeautifulSoup
from eastmoney.get_trace import generate_trace
from eastmoney.img_locate import get_distance, get_position

session = requests.session()
session.headers = {
    # 这里的 Cookie 是我浏览器上的 Cookie, 其中有个 Cookie 值决定校验的风险等级, 即是无感验证还是点选验证还是滑块验证, 没有研究是哪个值起这样的作用, 用兴趣的可以研究一下
    # 第一次请求一般都是无感验证, 如果请求头不加 Cookie, 升级的验证方式为点选验证, 加了这个 Cookie 才变成滑块验证
    'Cookie': 'p_origin=https%3A%2F%2Fpassport2.eastmoney.com; qgqp_b_id=0472721faf4a54b1f31465c45065fe56; st_si=42421110325677; st_sn=13; st_psi=20191024215313968-111000300841-6727199613; st_asi=delete; st_pvi=34574527160225; st_sp=2019-10-24%2019%3A01%3A44; st_inirUrl=https%3A%2F%2Fhao.360.com%2Fredirect',
    'Referer': 'https://exaccount2.eastmoney.com/home/Login?rc=1609971765',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
}

# 手机号
username = '18982347887'

# 密码
password = '123456'


def _encrypt_request(data):
    """
    加密表单信息
    :param data: 表单
    :return:
    """
    with open('em_slider.js', 'rb') as f:
        js = f.read().decode()
    ctx = execjs.compile(js)
    return ctx.call('encrypt', data)


def get_ctxid():
    """
    请求登录 iframe 获取 ctx_id
    :return:
    """
    url = 'https://exaccount2.eastmoney.com/home/Login?rc=1609971765'
    resp = session.get(url)
    bsobj = BeautifulSoup(resp.text, 'lxml')
    ctx_id = bsobj.select('#hdAccountCaptContextId')[0]['value']
    return ctx_id


def _init_captcha(ctx_id, username, password):
    """
    初始化验证码
    :param ctx_id: 验证码 ID
    :param username: 用户名
    :param password: 密码
    :return:
    """
    url = 'https://captcha2.eastmoney.com/Titan/api/captcha/get'

    params = {
        'callback': 'cb',
        'ctxid': ctx_id,
        'request': _encrypt_request(f"appid=201802274651|ctxid={ctx_id}|a={username}|p={password}|r={random.random()}"),
        '_': int(time.time() * 1000)
    }

    resp = session.get(url, params=params)
    result = json.loads(re.search(r'\((.*?)\)', resp.text).group(1))

    if result['ReturnCode'] == '0':
        return json.loads(result['Data']['CaptchaInfo'])
    return None


def _captcha_verify(init_data):
    """
    验证
    :param init_data:
    :return:
    """
    url = 'https://captcha2.eastmoney.com/Titan/api/captcha/Validate'

    if init_data['type'] == 'init':
        print('触发无感验证! ')
        distance = None
        # 轨迹类似于这样, 自己构造
        trace = "121,3,0:122,13,12:122,19,28:122,21,42:121,23,57:121,25,131"
        # 通过时间为最后一条轨迹的时间
        pass_time = 131
    elif init_data['type'] == 'slide':
        # 用了自己浏览器的 Cookie 才会触发滑块验证, 不用 Cookie 一直是点选验证
        print('触发滑块验证! ')
        distance = get_distance('https://' + init_data['static_servers'][0] + init_data['bg'],
                                'https://' + init_data['static_servers'][0] + init_data['slice'])
        trace = generate_trace(distance)
        pass_time = trace[-1][-1]
        trace = ':'.join([','.join(list(map(str, x))) for x in trace])
    elif init_data['type'] == 'click':
        # 点选验证浏览器上一直触发不了... 所以不知道他加密的数据结构是怎么样的
        print('触发点选验证! ')
        # 这里的 distance 是点选的位置, 不知道是什么样的结构, 是 123,23|123,23 这样的还是 123,23;123,23 这样的...
        distance = get_position('https://' + init_data['static_servers'][0] + init_data['fullbg'],
                                'https://' + init_data['static_servers'][0] + init_data['slice'])
        # 轨迹应该是跟滑块那些一样
        trace = []
        # 通过时间
        pass_time = trace[-1][-1]
        trace = ':'.join([','.join(list(map(str, x))) for x in trace])
    else:
        print('未知验证类型! ')
        return None

    data = f"appid={init_data['appid']}|ctxid={init_data['captchaContextId']}|type={init_data['type']}|u={distance}|d={trace}|a={username}|p={password}|t={pass_time}|r={random.random()}"

    params = {
        'callback': 'cb',
        'ctxid': init_data['captchaContextId'],
        'request': _encrypt_request(data),
        '_': int(time.time() * 1000)
    }
    resp = session.get(url, params=params)
    result = json.loads(re.search(r'\((.*?)\)', resp.text).group(1))
    print('校验结果: ', result)
    if result['ReturnCode'] == '0':
        return {
            'validate': json.loads(result['Data']['Result'])['validate']
        }
    elif result['ReturnCode'] == '5':
        print('验证升级, 重新请求验证码初始化接口! ')
        return 'Retry'
    return None


def crack():
    # 获取页面验证码 ID
    ctx_id = get_ctxid()
    while True:
        # 初始化验证码
        init_data = _init_captcha(ctx_id, username, password)
        print('初始化数据: ', init_data)
        # 验证
        result = _captcha_verify(init_data)
        if isinstance(result, dict):
            return {
                'success': 1,
                'message': '校验通过! ',
                'data': result
            }
        elif isinstance(result, str):
            pass
        else:
            return {
                'success': 0,
                'message': '校验失败! ',
                'data': None
            }


if __name__ == '__main__':
    x = crack()
    print(x)
