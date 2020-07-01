# -*- coding: utf-8 -*-
# @Time    : 2019/10/9 19:14
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : aes_encrypt.py
# @Software: PyCharm

import os
import cv2
import numpy as np
import requests
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


def process_location(location_array):
    """
    处理滑块验证码接口返回的图片还原数组
    :param location_array:
    :return: 图片顺序
    """
    new_loaction_list = []
    for t in location_array:
        if t < 20:
            new_loaction_list.append({
                'x': -int(260 / 20 * t),
                'y': 0
            })
        else:
            new_loaction_list.append({
                'x': -int(260 / 20 * (t % 20)),
                'y': -60
            })
    return new_loaction_list


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


def get_merge_image(location_list, url):
    """
    根据图片位置合并还原
    :param location_list: 图片位置数组
    :param url: 图片 url
    :return:
    """
    save_path = os.path.abspath('...') + '\\' + 'images'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    filename = _pic_download(url, 'all')
    im = Image.open(filename)
    width, height = im.size
    # print(width, height)
    big = im.crop((0, 0, 260, height))
    captcha_path = save_path + '\\' + 'captcha.jpg'
    slider_path = save_path + '\\' + 'slider.jpg'
    big.convert('RGB').save(captcha_path)

    small = im.crop((260, 0, width, height))
    small.convert('RGB').save(slider_path)

    new_im = Image.new('RGB', (260, height))

    upper_list = location_list[:20]
    lower_list = location_list[20:]

    x_offset = 0
    for location in upper_list:
        imgcrop = big.crop((abs(location['x']), abs(location['y']), abs(location['x']) + 13, abs(location['y']) + 60))
        new_im.paste(imgcrop, (x_offset, 0))
        x_offset += 13

    x_offset = 0
    for location in lower_list:
        imgcrop = big.crop((abs(location['x']), abs(location['y']), abs(location['x']) + 13, abs(location['y']) + 60))
        new_im.paste(imgcrop, (x_offset, 60))
        x_offset += 13

    new_im.show()
    new_im.save(captcha_path)
    return captcha_path, slider_path


def process_img(img1, img2):
    """
    图片处理
    :param img1: 处理后图片
    :param img2: 待处理图片
    :return:
    """
    cv2.imwrite(img1, img2)
    target = cv2.imread(img1)
    target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
    target = abs(255 - target)
    cv2.imwrite(img1, target)


def _get_distance(location_list, url):
    """
    获取缺口距离
    :param url: 验证码图片合集
    :return:
    """
    save_path = os.path.abspath('...') + '\\' + 'images'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    captcha_path, slider_path = get_merge_image(location_list, url)
    # 计算拼图还原距离
    target = cv2.imread(slider_path, 0)
    template = cv2.imread(captcha_path, 0)
    temp = save_path + '\\' + 'temp.jpg'
    targ = save_path + '\\' + 'targ.jpg'
    process_img(temp, template)
    process_img(targ, target)
    w, h = _cut_slider(targ)
    cv2.imwrite(temp, template)
    target = cv2.imread(targ)
    template = cv2.imread(temp)
    result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
    x, y = np.unravel_index(result.argmax(), result.shape)
    # 缺口位置
    # print((y, x, y + w, x + h))

    # 调用PIL Image 做测试
    image = Image.open(captcha_path)

    xy = (y + 3, x, y + w, x + h)
    # 切割
    imagecrop = image.crop(xy)
    # 保存切割的缺口
    imagecrop.save(save_path + '\\' + "new_image.jpg")
    imagecrop.show()
    return int(y + 3)
