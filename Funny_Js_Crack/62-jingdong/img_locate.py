# -*- coding: utf-8 -*-
# @Time    : 2019/10/18 15:59
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : img_locate.py
# @Software: PyCharm

import io
import os
import cv2
import base64
import numpy as np
from PIL import Image


def pic_download(url, type):
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
    current_img = Image.open(io.BytesIO(img_data)).convert("RGB")
    current_img.save(img_path)
    return img_path


def get_distance(slider_url, captcha_url):
    """
    获取缺口距离
    :param slider_url:
    :param captcha_url:
    :return:
    """
    save_path = os.path.abspath('...') + '\\' + 'images'
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    # 引用上面的图片下载
    slider_path = pic_download(slider_url, 'slider')

    # 引用上面的图片下载
    captcha_path = pic_download(captcha_url, 'captcha')

    # # 计算拼图还原距离
    target = cv2.imread(slider_path, 0)
    template = cv2.imread(captcha_path, 0)
    w, h = target.shape[::-1]
    temp = save_path + '\\' + 'temp.jpg'
    targ = save_path + '\\' + 'targ.jpg'
    cv2.imwrite(temp, template)
    cv2.imwrite(targ, target)
    target = cv2.imread(targ)
    target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    target = abs(255 - target)
    cv2.imwrite(targ, target)
    target = cv2.imread(targ)
    template = cv2.imread(temp)
    result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
    x, y = np.unravel_index(result.argmax(), result.shape)
    # 缺口位置
    # print((y, x, y + w, x + h))

    # 调用PIL Image 做测试
    image = Image.open(captcha_path)

    xy = (y, x, y + w, x + h)
    # 切割
    imagecrop = image.crop(xy)
    # 保存切割的缺口
    imagecrop.save(save_path + '\\' + "new_captcha.jpg")
    # imagecrop.show()
    return int(round(y))
