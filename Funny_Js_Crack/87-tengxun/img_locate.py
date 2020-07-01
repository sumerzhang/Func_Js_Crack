# -*- coding: utf-8 -*-
# @Time    : 2019/11/10 10:26
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : pic_locate.py
# @Software: PyCharm

import cv2
import numpy as np
from PIL import Image
import os


def _pic_download(session, url, type):
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
    # 请求多次保证图片下载成功, 有时第一次图片下载失败
    for _ in range(10):
        session.get(url)
    img_data = session.get(url).content
    with open(img_path, 'wb') as f:
        f.write(img_data)
    return img_path


def get_distance(session, slider_url, captcha_url):
    """
    获取缺口距离
    :param session:
    :param slider_url:
    :param captcha_url:
    :return:
    """
    save_path = os.path.abspath('...') + '\\' + 'images'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # 引用上面的图片下载
    slider_path = _pic_download(session, slider_url, 'slider')
    w, h = Image.open(slider_path).size

    # 图片还原
    captcha_path = _pic_download(session, captcha_url, 'captcha')

    # # 计算拼图还原距离
    target = cv2.imread(slider_path, 0)
    template = cv2.imread(captcha_path, 0)
    temp = save_path + '\\' + 'temp.jpg'
    targ = save_path + '\\' + 'targ.jpg'
    cv2.imwrite(targ, target)
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
    xy = (y + 23, x, y + w, x + h)
    # 切割
    imagecrop = image.crop(xy)
    # 保存切割的缺口
    imagecrop.convert('RGB').save(save_path + '\\' + "new_captcha.jpg")
    # imagecrop.show()
    return int(y + 23)
