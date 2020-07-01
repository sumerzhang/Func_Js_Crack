# -*- coding: utf-8 -*-
# @Time    : 2019/10/17 8:33
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : td_crypt.py
# @Software: PyCharm

import math
import execjs
from Crypto.Cipher import AES
import base64


def generate_key(token):
    """
    根据设备指纹生成自定义加密密钥
    :return:
    """
    return "rsp67ou9" + '-'.join(token.split('-')[1:])[2:18]


def generate_aes_key(token):
    """
    根据设备指纹生成 AES 密钥
    :return:
    """
    return "rsp67ou9" + '-'.join(token.split('-')[1:])[10:18]


def replace_str(text, x, y):
    """
    对指定字符串实现x、y互换
    :param text:
    :param x:
    :param y:
    :return:
    """
    chs = list(text)
    for i, ch in enumerate(chs):
        if ch == x:
            chs[i] = y
        elif ch == y:
            chs[i] = x
    return ''.join(chs)


def aes_encrypt(key, text, iv="Mnz14C2tXod8AUJ5"):
    """
    AES CBC Pkcs7Padding
    :param key: 密钥
    :param text: 明文
    :param iv: 偏移量固定
    :return:
    """
    bs = AES.block_size
    # Pkcs7 填充
    pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
    cipher = AES.new(key.encode(), AES.MODE_CBC, iv.encode())
    cipher_text = cipher.encrypt(pad(text).encode())
    encrypt_str = base64.b64encode(cipher_text).decode()
    # 大小写转换
    tansfer = lambda x: x.upper() if x.islower() else x.lower()
    # 字符替换, p/q 互换, I/J互换
    result = ''.join([tansfer(i) for i in [j for j in encrypt_str]]).replace('+', '~')
    result = replace_str(result, 'p', 'q')
    result = replace_str(result, 'I', 'J')
    return result


def et(ctx, text):
    return ctx.call('et', text)


def Pt(ctx, text):
    return ctx.call('Pt', text)


def ft(ctx, text, aes_key):
    return ctx.call('ft', text, aes_key)


def int2str(num, b):
    """
    将一个整数转化为指定进制字符
    :param num:
    :param b:
    :return:
    """
    num = math.ceil(num)
    return ((num == 0) and "0") or (int2str(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])


def encrypt_trace(slide_y, trace, start_time):
    """
    加密轨迹: 按照特定顺序对轨迹数值转成 36 进制字符串拼接
    :param slide_y: 缺口 y 值
    :param trace: 轨迹
    :param start_time: 验证码刷新时间
    :return:
    """
    # 优化: python 复写整数转 36 进制
    # js = """
    # function encrypt(x) {
    #     return Math.round(x).toString(36)
    # }
    # """
    # ctx = execjs.compile(js)
    # encrypt = lambda j: ctx.call('encrypt', j) if j != '' else j
    # enc_slide = ','.join([encrypt(slide[m]) for m in ["left", "top"]]) + ',' + \
    #             ','.join([encrypt(n) for n in [slide['left'] + slide['width'], slide['top'] + slide['height']]]) + \
    #             ',' + encrypt(trace[-1]['op_x']) + ',' + encrypt(trace[-1]['op_y']) + ',0,0,' + encrypt(start_time)
    encrypt = lambda j: int2str(j, 36) if j != '' else j
    slide = {'height': 35, 'left': 506.5, 'top': 636.5, 'width': 230}
    enc_slide = ','.join([encrypt(slide[m]) for m in ["left", "top"]]) + ',' + \
                ','.join([encrypt(n) for n in [slide['left'] + 42, slide['top'] + 40]]) + \
                ',' + encrypt(trace[-1]['op_x']) + ',' + encrypt(trace[-1]['op_y']) + \
                ',' + encrypt(slide['left']) + \
                ',' + encrypt(440.5 + slide_y) + ",1,0," + encrypt(start_time)

    enc_trace = []
    for i in trace:
        enc_trace.append((encrypt(i['time'] - start_time) + ',' + ','.join(
            [encrypt(i[k]) for k in ['type', 'op_x', 'op_y', 'Action']])).strip(','))
    enc_trace.append('')
    return enc_slide + '%' + '|'.join(enc_trace)


if __name__ == '__main__':
    encrypt = lambda j: int2str(j, 36) if j != '' else j
    slide = {'height': 35, 'left': 506.5, 'top': 636.5, 'width': 230}
    enc_slide = ','.join([encrypt(slide[m]) for m in ["left", "top"]]) + ',' + \
                ','.join([encrypt(n) for n in [slide['left'] + 42, slide['top'] + 40]]) + \
                ',' + encrypt(523) + ',' + encrypt(669) + \
                ',' + encrypt(slide['left']) + \
                ',' + encrypt(440.5 + 25) + ",1,0," + encrypt(1571228630478)
    print(enc_slide)
    print("e3,hp,f9,it,ej,il,e3,cy,1,0,k1t8yifi")
