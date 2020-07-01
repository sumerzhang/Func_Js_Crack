# -*- coding: utf-8 -*-
# @Time    : 2019/10/17 8:21
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : img_locate.py
# @Software: PyCharm

import os
import numpy as np
import execjs
from PIL import Image
import cv2
import requests


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
    img_data = requests.get('https://static.tongdun.net' + url).content
    with open(img_path, 'wb') as f:
        f.write(img_data)
    return img_path


def get_merge_str(imageGeneral, bgImageSplitSequence):
    """
    获取图片还原数组
    :param imageGeneral:
    :param bgImageSplitSequence:
    :return:
    """
    with open('merge_img.js', 'rb') as f:
        js = f.read().decode()
    ctx = execjs.compile(js)
    return ctx.call('merge', imageGeneral, bgImageSplitSequence)


def parse_int(text):
    js = """
    function parse_int(text) {
        return parseInt(text, 16)
    }
    """
    ctx = execjs.compile(js)
    return ctx.call('parse_int', text)


def merge_img(init_data):
    """
    还原验证码
    :return:
    """
    img_path = _pic_download(init_data['validateCodeObj']['slideBgi'], 'captcha')
    img = Image.open(img_path)
    upper_list = []
    lower_list = []
    for i in range(8):
        upper_crop = img.crop((round(320 / 8) * i, 0, round(320 / 8) * i + 40, 90))
        upper_list.append(upper_crop)
        lower_crop = img.crop((round(320 / 8) * i, 90, round(320 / 8) * i + 40, 180))
        lower_list.append(lower_crop)

    new_image = Image.new('RGB', img.size)
    merge_str = get_merge_str(init_data['validateCodeObj']['imageGeneral'],
                              init_data['validateCodeObj']['bgImageSplitSequence'])
    for m in range(16):
        n = parse_int(merge_str[m])
        if n < 8:
            if m >= 8:
                new_image.paste(lower_list[m - 8], (round(320 / 8) * n, 0))
            else:
                new_image.paste(upper_list[m], (round(320 / 8) * n, 0))
        else:
            if m >= 8:
                new_image.paste(lower_list[m - 8], (round(320 / 8) * (n - 8), 90))
            else:
                new_image.paste(upper_list[m], (round(320 / 8) * (n - 8), 90))

    new_image.show()

    save_path = os.path.abspath('...') + '\\' + 'images'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    img_path = save_path + '\\' + 'new_captcha.jpg'
    new_image.save(img_path)
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


def get_distance(init_data):
    """
    获取缺口距离
    :param init_data: 验证码初始化数据
    :return:
    """
    save_path = os.path.abspath('...') + '\\' + 'images'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # 引用上面的图片下载
    slider_path = _pic_download(init_data['validateCodeObj']['slideImage'], 'slider')

    # 图片还原
    captcha_path = merge_img(init_data)

    # # 计算拼图还原距离
    target = cv2.imread(slider_path, 0)
    template = cv2.imread(captcha_path, 0)
    temp = save_path + '\\' + 'temp.jpg'
    targ = save_path + '\\' + 'targ.jpg'
    cv2.imwrite(targ, target)
    w, h = _cut_slider(slider_path)
    cv2.imwrite(temp, template)
    target = cv2.imread(targ)
    target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    target = abs(255 - target)
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
    imagecrop.convert('RGB').save(save_path + '\\' + "new_image.jpg")
    imagecrop.show()
    return int(round(y))


if __name__ == '__main__':
    pass
