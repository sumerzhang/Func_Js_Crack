# -*- coding: utf-8 -*-
# @Time    : 2019/10/9 19:54
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : geetest.py
# @Software: PyCharm

import random
import time
import json
import requests
from wanmei.img_locate import _get_distance, process_location
from wanmei import wm_crypt
from wanmei.trace import _generate_trace


session = requests.session()
session.headers = {
    'Referer': 'https://passport.wanmei.com/sso/login?service=passport&isiframe=1&location=2f736166652f',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
}


def get_cap_ticket():
    """
    获取验证码标识
    :return:
    """
    url = 'https://passport.wanmei.com/sso/servlet/ajax?op=mCaptchaInit&isAICap=1'
    resp = session.get(url).json()
    if resp['code'] == 0:
        cap_ticket = resp['data']['capTicket']
        return cap_ticket
    return None


def fist_test(cap_ticket):
    """
    智能验证, 判断用户可疑程度, 使用点选验证还是滑块验证
    :param cap_ticket:
    :return:
    """
    url = 'https://captchas.wanmei.com/aicaptcha/firstTest'
    r = "[[149,163,3,772],[146,191,6,859],[146,191,5,859],[146,192,6,873],[146,192,5,873],[146,206,3,978],[146,209,6,1004],[146,209,5,1005],[146,211,6,1012],[146,211,5,1013],[145,232,3,1122],[145,233,1,1283],[145,233,2,1497]]"
    op = wm_crypt.encrypt(cap_ticket, r)
    params = {
        'callback': '',
        'appId': '10003',
        'capTicket': cap_ticket,
        'mobile': '0',
        'op': op,
        'fp': '4170524067',
        'isInIframe': 'true',
        '_': int(time.time() * 1000)
    }
    resp = session.get(url, params=params)
    result = json.loads(resp.text.replace('(', '').replace(')', ''))
    if result['type'] == 'move_captcha':
        return True
    return False


def init_slider(cap_ticket):
    """
    初始化验证码
    :return:
    """
    params = {
        'callback': '',
        'appId': '10003',
        'capTicket': cap_ticket,
        '_': int(time.time() * 1000)
    }
    url = 'https://captchas.wanmei.com/aicaptcha/getCaptcha?'
    resp = session.get(url, params=params)
    result = json.loads(resp.text.replace('(', '').replace(')', ''))
    if result['code'] == 0:
        print('滑块初始化成功! ')
        return {
            'cap_key': result['capKey'],
            'img_url': result['imgUrl'],
            'data': result['data']
        }
    return None


def _slider_verify(cap_ticket, cap_key, validate, op):
    """
    最终验证
    :return:
    """
    url = 'https://captchas.wanmei.com/aicaptcha/secondTest/move_captcha'
    params = {
        'callback': '',
        'appId': '10003',
        'capTicket': cap_ticket,
        'capKey': cap_key,
        'validData': validate,
        'op': op,
        'fp': '4170524067',
        'label': 1,
        '_': int(time.time() * 1000)
    }
    resp = session.get(url, params=params)
    result = json.loads(resp.text.replace('(', '').replace(')', ''))
    print(result)
    if result['code'] == 0:
        return {
            'success': 1,
            'message': '校验通过! ',
            'data': {
                'result': result['result']
            }
        }
    return {
        'success': 0,
        'message': '校验失败! ',
        'data': None
    }


def crack():
    capt_ticket = get_cap_ticket()
    # 触发验证, 最开始可能是点选, 直到出现滑块验证为止
    while True:
        check = fist_test(capt_ticket)
        if check:
            break
    # 初始化滑块
    init_data = init_slider(capt_ticket)
    # 处理图片还原数组
    location_list = process_location(json.loads(init_data['data']))
    # 获取缺口距离
    distance = _get_distance(location_list, init_data['img_url'])
    # 构造轨迹
    start_time = int(time.time() * 1000)
    time.sleep(random.uniform(0.1, 0.3))
    trace = _generate_trace(distance + random.randint(5, 10), start_time)
    # 加密轨迹数据
    # op
    op = wm_crypt.encrypt(capt_ticket, json.dumps(trace))
    time.sleep(random.uniform(1.5, 2.5))
    # validate
    validate = {
        'length': distance,
        'validateTimeMilSec': int(time.time() * 1000) - start_time
    }
    validate_data = wm_crypt.encrypt(capt_ticket, json.dumps(validate))
    result = _slider_verify(capt_ticket, init_data['cap_key'], validate_data, op)
    return result


if __name__ == '__main__':
    x = crack()
    print(x)