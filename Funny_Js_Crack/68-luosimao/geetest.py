# -*- coding: utf-8 -*-
# @Time    : 2019/10/11 0:03
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : geetest.py
# @Software: PyCharm

import re
import json
import random
import requests
import execjs
from bs4 import BeautifulSoup
from luosimao import img_locate
import time
from luosimao.lsm_crypt import aes_encrypt, md5_encrypt
from luosimao.chaojiying import image_to_text


session = requests.session()
session.headers = {
    'Content-type': 'application/x-www-form-urlencoded',
    'Origin': 'https://captcha.luosimao.com',
    'Referer': 'https://my.luosimao.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


def _req_widiget():
    """
    初始化环境
    :return:
    """
    url = 'https://captcha.luosimao.com/api/widget?k=e7b4d20489b69bab25771f9236e2c4be&l=zh-cn&s=normal&i=_2ymuhhcry'
    resp = session.get(url)
    bsobj = BeautifulSoup(resp.text, 'lxml')
    data_token = bsobj.select('#l_captcha_widget')[0]['data-token']
    return data_token


def _init_slider(data_token):
    """
    初始化验证码
    :param data_token:
    :return:
    """
    url = 'https://captcha.luosimao.com/api/request?k=e7b4d20489b69bab25771f9236e2c4be&l=zh-cn'
    env_param = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36||{}||1366:768||win32||webkit".format(data_token)
    begin_time = int(time.time() * 1000)
    click_param = f"{random.randint(100, 150)},{random.randint(0, 30)}:{begin_time}||{random.randint(100, 150)},{random.randint(0, 30)}:{begin_time + random.randint(1, 10)}"
    data = {
        'bg': aes_encrypt("c28725d494c78ad782a6199c341630ee", "2801003954373300", env_param),
        'b': aes_encrypt("c28725d494c78ad782a6199c341630ee", "2801003954373300", click_param)
    }
    # print(data)
    resp = session.post(url, data=data)
    print(resp.json())
    cookies = resp.cookies.get_dict()
    return resp.json(), cookies


def get_captcha(s, cookies):
    """
    获取乱序验证码图片和还原数组
    :param s:
    :param cookies:
    :return:
    """
    url = 'https://captcha.luosimao.com/api/frame'
    params = {
        's': s,
        'i': '_2ymuhhcry',
        'l': 'zh-cn'
    }
    resp = session.get(url, params=params, cookies=cookies)
    captcha_data = re.search('var captchaImage = ({.*?})', resp.text, re.S).group(1)
    captcha_url = re.search(r"p:\['(.*?)',", captcha_data, re.S).group(1)
    merge_array = json.loads(re.search(r'l:(.*?)}', captcha_data).group(1))
    return captcha_url, merge_array


def encrypt_data(init_data, position):
    """
    js 加密
    :param init_data:
    :param position:
    :return:
    """
    with open('lsm_encrypt.js', 'rb') as f:
        js = f.read().decode()
    ctx = execjs.compile(js)
    return ctx.call('encrypt', init_data, position)


def _slider_verify(init_data, position, cookies):
    """
    最终验证
    :param init_data: 初始化数据
    :param position: 点选位置
    :param cookies:
    :return:
    """
    url = 'https://captcha.luosimao.com/api/user_verify'

    # 参数说明: h: 哈希签名, 给服务器确定使用的验证码图片和密钥;
    #          v: 点选位置加密, 固定偏移量
    #          s: 哈希验签
    # python 复写版
    data = {
        'h': init_data['h'],
        'v': aes_encrypt(init_data['i'], "2801003954373300", position).replace('=', '').replace('+', '-').replace('/', '_'),
        's': md5_encrypt(position)
    }
    print(data)
    # execjs 执行版
    data1 = encrypt_data(init_data, position)
    print(data1)
    result = session.post(url, data=data, cookies=cookies).json()
    print(result)
    if result['res'] == 'success':
        return result['resp']
    else:
        if 'reload' in set(result.keys()):
            init_data = result['request']
            return init_data
        return None


def click(init_data, cookies):
    # 获取乱序验证码图片和还原位置数组
    captcha_url, merge_array = get_captcha(init_data['s'], cookies)
    # 还原验证码图片
    captcha_path = img_locate.reduce_image(merge_array, captcha_url)
    # 制作描述图片
    word_path = img_locate.make_word(init_data['w'])
    # 合并
    img_path = img_locate.merge_word(captcha_path, word_path)
    # 提交给打码平台识别
    with open(img_path, 'rb') as f:
        img_data = f.read()
    ok, position = image_to_text(img_data, img_kind=9004)
    if ok:
        # 最终验证
        position = position.replace('|', '#')
        print(position)
        # 停顿3到5秒, 模拟人为
        time.sleep(random.randint(3, 5))
        result = _slider_verify(init_data, position, cookies)
        if isinstance(result, str):
            return {
                'success': 1,
                'message': '校验成功! ',
                'data': {
                    'resp': result
                }
            }
        elif isinstance(result, dict):
            print('重新加载验证! ')
            click(result, cookies)
        return {
            'success': 0,
            'message': '校验失败! ',
            'data': None
        }
    else:
        return {
            'success': 0,
            'message': '验证码识别失败! ',
            'data': None
        }


if __name__ == '__main__':
    x = _req_widiget()
    y, cookies = _init_slider(x)
    z = click(y, cookies)
    print(z)
