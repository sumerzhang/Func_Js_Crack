# -*- coding: utf-8 -*-
# @Time    : 2019/10/11 8:48
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : img_locate.py
# @Software: PyCharm

import os
import requests
from PIL import Image
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


def reduce_image(location_list, url):
    """
    根据还原数组还原验证码图片
    :param location_list: 图片位置数组
    :param url: 图片 url
    :return:
    """
    img_path = _pic_download(url, 'captcha')
    im = Image.open(img_path)

    new_im = Image.new('RGB', im.size)

    upper_list = location_list[:15]
    lower_list = location_list[15:]

    x_offset = 0
    for location in upper_list:
        imgcrop = im.crop((int(location[0]), int(location[1]), int(location[0]) + 20, int(location[1]) + 80))
        new_im.paste(imgcrop, (x_offset, 0))
        x_offset += 20

    x_offset = 0
    for location in lower_list:
        imgcrop = im.crop((int(location[0]), int(location[1]), int(location[0]) + 20, int(location[1]) + 80))
        new_im.paste(imgcrop, (x_offset, 80))
        x_offset += 20

    # new_im.show()
    new_im.save(img_path)
    return img_path


def merge_word(img1, img2):
    """
    将描述性文字合并到验证码图片上, 以便交给打码平台识别
    :return:
    """
    save_path = os.path.abspath('...') + '\\' + 'images'
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    new_image = Image.new('RGB', (300, 190))
    img1 = Image.open(img1)
    new_image.paste(img1, (0, 0))

    img2 = Image.open(img2)
    new_image.paste(img2, (0, 160))

    new_image.show()
    img_path = save_path + '\\' + 'new_captcha.jpg'
    new_image.save(img_path)
    return img_path

