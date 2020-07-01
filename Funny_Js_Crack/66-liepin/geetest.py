# -*- coding: utf-8 -*-
# @Time    : 2019/10/11 18:27
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : geetest.py
# @Software: PyCharm

import os
import execjs
from PIL import Image
import requests
import random
import json
import time
from Crypto.Cipher import AES
import base64
from liepin.chaojiying import image_to_text


headers = {
    'Referer': 'https://passport.liepin.cn/account/v1/elogin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}


def aes_encrypt(key, text):
    """
    AES CBC Pkcs7Padding
    :param key: 密钥, iv 与密钥相同
    :param text: 明文
    :return:
    """
    bs = AES.block_size
    # Pkcs7 填充
    pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
    cipher = AES.new(key.encode(), AES.MODE_CBC, key.encode())
    data = cipher.encrypt(pad(text).encode())
    return base64.b64encode(data).decode()


def _init_click():
    """
    初始化点选验证码
    :return:
    """
    url = 'https://passport.liepin.cn/verificationcode/v1/clicaptcha.json'
    data = {
        'scenario': '4'
    }
    resp = requests.post(url, headers=headers, data=data).json()
    if resp['flag']:
        return {
            'captcha_url': resp['data']['image'],
            'challenge': resp['data']['challenge']
        }
    return None


def _pic_download(url, type):
    """
    图片下载
    :param url:
    :param type:
    :return:
    """
    save_path = os.path.abspath('...') + '\\' + 'images'
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    img_path = save_path + '\\' + '{}.jpg'.format(type)
    img_data = base64.b64decode(url)
    with open(img_path, 'wb') as f:
        f.write(img_data)
    return img_path


def merge_img(img_url):
    """
    图片还原
    :param img_url:
    :return:
    """
    js = """
    function get_merge_array() {
        for (var t = [6, 1, 5, 3, 0, 7, 2, 4], a = [], i = void 0, s = void 0, o = void 0, r = void 0, n = 0, l = t.length; n < l;)
            i = t[n],
                s = i + l,
                o = i + (l << 1),
                r = s + (l << 1),
                a[n++] = i,
                a[2 * l - n] = s,
                a[3 * l - n] = o,
                a[4 * l - n] = r;
        for (var c = [], u = 0, d = a.length; u < d; u++) {
            var h = u >= 16 ? 1 : 0;
            c.push([[a[u] % 16 * 16, 100 * h], [u % 16 * 16, 100 * h]])
        }
        return c
    }
    """
    ctx = execjs.compile(js)
    merge_array = ctx.call('get_merge_array')

    save_path = os.path.abspath('...') + '\\' + 'images'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    img_path = _pic_download(img_url, 'captcha')
    img = Image.open(img_path)
    new_image = Image.new('RGB', img.size)

    for i in merge_array:
        imgcrop = img.crop((i[0][0], i[0][1], i[0][0] + 16, i[0][1] + 100))
        new_image.paste(imgcrop, (i[1][0], i[1][1]))
    # new_image.show()
    img_path = save_path + '\\' + 'new_captcha.jpg'
    new_image.save(img_path)
    return img_path


def fake_click_data(position):
    """
    根据识别结果伪造点击数据
    :return:
    """
    # 轨迹删除
    left_click_data.append({
        't': timestamp,
        'x': position['x'],
        'y': position['y']
    })
    collect_data = {
        'startTime': start_time,
        'mousemoveData': move_data,
        'mouseLeftClickData': left_click_data,
        'mouseLeftDownData': left_click_data[1:],
        'mouseLeftUpData': left_click_data[1:],
        'mouseRightClickData': [],
        'mouseRightDownData': [],
        'mouseRightUpData': [],
        'valuableClickData': click_data,
        'keydownData': [],
        'mouseClickMaxCount': 20,
    }
    return collect_data


def _click_verify(challenge, aes_key, collect_data):
    """
    最终验证
    :param challenge:
    :param aes_key:
    :param collect_data:
    :return:
    """
    url = 'https://passport.liepin.cn/verificationcode/v1/verifyclicaptcha.json'
    data = {
        'scenario': '4',
        'challenge': challenge,
        'collectibles': aes_encrypt(aes_key, json.dumps(collect_data))
    }
    resp = requests.post(url, headers=headers, data=data).json()
    print(resp)
    if resp['flag']:
        return resp['data']['ticket']
    return None


def click():
    # 初始化验证码
    init_data = _init_click()
    captcha_url = init_data['captcha_url']
    aes_key = captcha_url[830: 846]
    challenge = init_data['challenge']
    # 乱序验证码图片还原
    img_path = merge_img(captcha_url)
    # 超级鹰识别
    with open(img_path, 'rb') as f:
        img_data = f.read()
    ok, position = image_to_text(img_data, img_kind=9004)
    if ok:
        # 伪造点击数据, 已删除, 自行处理, 如有需要, 正当需求, 可邮件联系我
        collect_data = fake_click_data(position)
        # 最终验证
        result = _click_verify(challenge, aes_key, collect_data)
        if result:
            return {
                'success': 1,
                'message': '校验通过! ',
                'data': {
                    'ticket': result
                }
            }
        return {
            'success': 0,
            'message': '校验失败! ',
            'data': None
        }
    return {
        'success': 0,
        'message': '验证码识别失败! ',
        'data': None
    }


if __name__ == '__main__':
    x = click()
    print(x)
