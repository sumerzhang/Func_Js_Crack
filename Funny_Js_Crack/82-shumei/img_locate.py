# -*- coding: utf-8 -*-
# @Time    : 2019/11/1 18:47
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : img_locate.py
# @Software: PyCharm

import os
import cv2
import requests
import numpy as np
from PIL import Image


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
    img_data = requests.get(url).content
    with open(img_path, 'wb') as f:
        f.write(img_data)
    return img_path


def get_distance(captcha_url):
    """
    获取缺口距离
    :param captcha_url:
    :return:
    """
    save_path = os.path.abspath('...') + '\\' + 'images'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # 引用上面的图片下载
    slider_path = save_path + '\\' + 'slider.jpg'
    w, h = Image.open(slider_path).size

    # 引用上面的图片下载
    captcha_path = _pic_download(captcha_url, 'captcha')

    # 计算拼图还原距离
    target = cv2.imread(slider_path, 0)
    template = cv2.imread(captcha_path, 0)

    temp = save_path + '\\' + 'temp.jpg'
    targ = save_path + '\\' + 'targ.jpg'
    cv2.imwrite(temp, template)
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
    imagecrop.save(save_path + '\\' + "new_image.png")
    imagecrop.show()
    return int(y)


def _get_distance(captcha_url):
    """
    获取缺口距离
    :param captcha_url: 验证码 url
    :return:
    """
    save_path = os.path.abspath('...') + '\\' + 'images'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    img_path = _pic_download(captcha_url, 'captcha')
    img1 = cv2.imread(img_path, 0)
    img2 = cv2.imread(save_path + '\\' + "slider.jpg", 0)
    res = cv2.matchTemplate(img1, img2, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= 0.6)
    for pt in zip(*loc[::-1]):
        p = pt
    try:
        cv2.imshow('Detected', img1[p[1]:, p[0]:])
        cv2.waitKey(3000)
    except Exception as e:
        print(e.args)
        return None
    res = cv2.resize(img1, (255, int(300 * (255 / 600))), interpolation=cv2.INTER_CUBIC)
    cv2.imshow("res", res[:, int(p[0] * (255 / 600) + 15):])
    # cv2.waitKey(3000)
    return int(p[0] * (290 / 600))
