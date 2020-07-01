# -*- coding: utf-8 -*-
# @Time    : 2019/11/1 21:56
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : img_locate.py
# @Software: PyCharm

import os
import numpy as np
import requests
from PIL import Image
import cv2
from PIL import ImageFont
from PIL import ImageDraw


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


def _get_distance(slider_url, captcha_url):
    """
    获取缺口距离
    :param slider_url: 滑块图片 url
    :param captcha_url: 验证码图片 url
    :return:
    """
    save_path = os.path.abspath('...') + '\\' + 'images'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # 引用上面的图片下载
    slider_path = _pic_download(slider_url, 'slider')

    # 引用上面的图片下载
    captcha_path = _pic_download(captcha_url, 'captcha')

    # 计算拼图还原距离
    target = cv2.imread(slider_path, 0)
    template = cv2.imread(captcha_path, 0)
    temp = save_path + '\\' + 'temp.jpg'
    targ = save_path + '\\' + 'targ.jpg'
    cv2.imwrite(targ, target)
    w, h = _cut_slider(slider_path)
    cv2.imwrite(temp, template)
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
    imagecrop.save(save_path + '\\' + "new_image.jpg")
    # imagecrop.show()
    return int(y + 3)


def make_word(text):
    """
    制作描述图片
    :return:
    """
    save_path = os.path.abspath('...') + '\\' + 'images'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    text = text.replace('<i>', '').replace('</i>', '')
    # 初始化图片对象, (300, 30)为图片大小, (255, 255, 255) 为白色背景
    img = Image.new('RGB', (300, 30), (255, 255, 255))
    # 设置字体
    font = ImageFont.truetype('simsun.ttc', 15)
    # 初始化写入对象
    draw = ImageDraw.Draw(img)
    # 添加文字, (0, 0): 文字起始坐标, (0, 0, 0): 颜色(黑色), font: 字体
    draw.text((0, 0), text, (0, 0, 0), font=font)
    # img.show()
    img_path = save_path + '\\' + 'word.jpg'
    img.save(img_path)
    return img_path


def merge_word(img1, img2, width):
    """
    将描述性文字合并到验证码图片上, 以便交给打码平台识别
    :return:
    """
    save_path = os.path.abspath('...') + '\\' + 'images'
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    new_image = Image.new('RGB', (width, 190))
    img1 = Image.open(img1)
    new_image.paste(img1, (0, 0))

    img2 = Image.open(img2)
    new_image.paste(img2, (0, 160))

    # new_image.show()
    img_path = save_path + '\\' + 'new_captcha.jpg'
    new_image.save(img_path)
    return img_path
