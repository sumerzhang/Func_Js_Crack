# -*- coding: utf-8 -*-
# @Time    : 2019/11/1 21:58
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : encrypt.py
# @Software: PyCharm

import execjs


def _reload_js():
    """
    加载 js
    :return:
    """
    with open('yd_slider.js', 'rb') as f:
        slider_js = f.read().decode()
    with open('generate_fp.js', 'rb') as f:
        fp_js = f.read().decode()
    return slider_js, fp_js


def _get_cb(js):
    """
    生成 cp 参数
    :param js:
    :return:
    """
    ctx = execjs.compile(js)
    return ctx.call('get_cb')[:64]


def _get_fp(js):
    """
    生成指纹 fp
    :param js:
    :return:
    """
    ctx_ = execjs.compile(js)
    return ctx_.call('generateFingerprint')


def _encrypt_slider(js, token, trace, width):
    """
    滑块验证加密
    加密轨迹
    :param token:
    :param trace:
    :param width
    :return:
    """
    ctx = execjs.compile(js)
    return ctx.call('slider_encrypt', token, trace, width)


def _encrypt_click(js, token, trace, position):
    """
    点选验证加密
    加密轨迹与点选位置
    :param js:
    :param token:
    :param trace:
    :param position:
    :return:
    """
    ctx = execjs.compile(js)
    return ctx.call('click_encrypt', token, trace, position)


def _encrypt_sense(js, token, trace, position):
    """
    无感验证加密
    加密轨迹与点击位置
    :param js:
    :param token:
    :param trace:
    :param position:
    :return:
    """
    ctx = execjs.compile(js)
    return ctx.call('sense_encrypt', token, trace, position)


def _encrypt_validate(js, validate, fp):
    """
    加密 validate
    :param js:
    :param validate: 验证码通过签名
    :param fp: 指纹
    :return:
    """
    ctx = execjs.compile(js)
    return ctx.call('encrypt_validate', validate, fp)
