# -*- coding: utf-8 -*-
# @Time    : 2019/10/28 16:24
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : test.py
# @Software: PyCharm

import time
import random
import requests
from geetest3.geetest import GeetestV3
from geetest3.geetest_v2 import GeetestV3New


def test1():
    """
    B站测试
    :return:
    """
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://passport.bilibili.com/login',
        'Connection': 'keep-alive',
    }
    params = {'plat': '11'}
    response = requests.get(
        'https://passport.bilibili.com/web/captcha/combine',
        headers=headers,
        params=params,
    )
    result = response.json()['data']['result']
    result = GeetestV3(result['gt'], result['challenge']).crack()

    if result:
        return {
            'success': 1,
            'message': '校验通过! ',
            'data': {
                'validate': result
            }
        }
    return {
        'success': 0,
        'message': '校验失败! ',
        'data': None
    }


def test2():
    """
    简书测试
    :return:
    """
    url = 'https://www.jianshu.com/captchas/new?t={}-vjp'.format(int(time.time() * 1000))
    headers = {
        'referer': 'https://www.jianshu.com/sign_in',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36'
    }
    resp = requests.get(url, headers=headers).json()
    gt = resp['gt']
    challenge = resp['challenge']
    result = GeetestV3(gt, challenge).crack()
    if result:
        return {
            'success': 1,
            'message': '校验通过! ',
            'data': {
                'validate': result
            }
        }
    return {
        'success': 0,
        'message': '校验失败! ',
        'data': None
    }


def test3():
    """
    最新版极验3滑块验证, 测试为 OKEX 注册： https://www.okex.me/account/register, 固定 gt
    :return:
    """
    result = GeetestV3New('5252e05bb861c2b62105353977e43f94').crack()
    if result:
        return {
            'success': 1,
            'message': '校验通过! ',
            'data': {
                'validate': result
            }
        }
    return {
        'success': 0,
        'message': '校验失败! ',
        'data': None
    }


def test4():
    """
    拉勾登录测试: https://passport.lagou.com/login/login.html?utm_source=m_cf_cpt_360_pc1
    gt 固定, 图片选择, 类似谷歌 recaptcha
    :return:
    """
    result = GeetestV3New('66442f2f720bfc86799932d8ad2eb6c7').crack()
    if result:
        return {
            'success': 1,
            'message': '校验通过! ',
            'data': {
                'validate': result
            }
        }
    return {
        'success': 0,
        'message': '校验失败! ',
        'data': None
    }


if __name__ == '__main__':
    print('开始测试...')
    print('=' * 100)
    num = 1
    success = 0
    while num <= 100:
        # x = test1()
        # x = test2()
        # x = test3()
        x = test4()
        print(x)
        print('=' * 100)
        if x['success']:
            success += 1
        time.sleep(random.randint(1, 3))
        num += 1
    print('最后测试结果 >> %.2f%%' % success)
