# -*- coding: utf-8 -*-
# @Time    : 2019/10/24 20:12
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : img_locate.py
# @Software: PyCharm

import os
import cv2
import numpy as np
import requests
from PIL import Image
from eastmoney.chaojiying import image_to_text


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


def merge_img(url, type):
    """
    还原图片
    :param url: 乱序验证码 url
    :param type: 类型
    :return:
    """
    merge_array = [{"left": 157, "top": 0}, {"left": 145, "top": 0}, {"left": 265, "top": 0}, {"left": 277, "top": 0},
                   {"left": 181, "top": 0}, {"left": 169, "top": 0}, {"left": 241, "top": 0}, {"left": 253, "top": 0},
                   {"left": 109, "top": 0}, {"left": 97, "top": 0}, {"left": 289, "top": 0}, {"left": 301, "top": 0},
                   {"left": 85, "top": 0}, {"left": 73, "top": 0}, {"left": 25, "top": 0}, {"left": 37, "top": 0},
                   {"left": 13, "top": 0}, {"left": 1, "top": 0}, {"left": 121, "top": 0}, {"left": 133, "top": 0},
                   {"left": 61, "top": 0}, {"left": 49, "top": 0}, {"left": 217, "top": 0}, {"left": 229, "top": 0},
                   {"left": 205, "top": 0}, {"left": 193, "top": 0}, {"left": 145, "top": 80}, {"left": 157, "top": 80},
                   {"left": 277, "top": 80}, {"left": 265, "top": 80}, {"left": 169, "top": 80},
                   {"left": 181, "top": 80}, {"left": 253, "top": 80}, {"left": 241, "top": 80},
                   {"left": 97, "top": 80}, {"left": 109, "top": 80}, {"left": 301, "top": 80},
                   {"left": 289, "top": 80}, {"left": 73, "top": 80}, {"left": 85, "top": 80}, {"left": 37, "top": 80},
                   {"left": 25, "top": 80}, {"left": 1, "top": 80}, {"left": 13, "top": 80}, {"left": 133, "top": 80},
                   {"left": 121, "top": 80}, {"left": 49, "top": 80}, {"left": 61, "top": 80}, {"left": 229, "top": 80},
                   {"left": 217, "top": 80}, {"left": 193, "top": 80}, {"left": 205, "top": 80}]

    captcha_path = _pic_download(url, type)
    captcha = Image.open(captcha_path)
    new_captcha = Image.new('RGB', (260, 160))

    upper_list = merge_array[:26]
    lower_list = merge_array[26:]

    for index, location in enumerate(upper_list):
        imgcrop = captcha.crop((location['left'], location['top'], location['left'] + 10, location['top'] + 80))
        new_captcha.paste(imgcrop, (index * 10, 0))

    for index, location in enumerate(lower_list):
        imgcrop = captcha.crop((location['left'], location['top'], location['left'] + 10, location['top'] + 80))
        new_captcha.paste(imgcrop, (index * 10, 80))

    new_captcha.save(captcha_path)
    return captcha_path


def _cut_slider(path):
    """
    滑块切割
    :return:
    """
    save_path = os.path.abspath('...') + '\\' + 'images'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

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
    result.convert('RGB').save(save_path + '\\' + 'temp.jpg')
    # result.show()
    return result.size[0], result.size[1]


def get_distance(captcha_url, slider_url):
    """
    获取滑块缺口距离
    :param captcha_url:
    :param slider_url:
    :return:
    """
    save_path = os.path.abspath('...') + '\\' + 'images'
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # 完整图片还原
    captcha_path = merge_img(captcha_url, 'slide_full')
    # 缺口图片还原
    slider_path = _pic_download(slider_url, 'slide_gap')
    # 滑块切割
    w, h = _cut_slider(slider_path)

    # # 计算拼图还原距离
    target = cv2.imread(slider_path, 0)
    template = cv2.imread(captcha_path, 0)
    temp = save_path + '\\' + 'temp.jpg'
    targ = save_path + '\\' + 'targ.jpg'
    cv2.imwrite(targ, target)
    cv2.imwrite(temp, template)

    target = cv2.imread(targ)
    template = cv2.imread(temp)
    result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
    x, y = np.unravel_index(result.argmax(), result.shape)

    # 调用PIL Image 做测试
    image = Image.open(captcha_path)

    xy = (y + 5, x, y + w, x + h)
    # 切割
    imagecrop = image.crop(xy)
    # 保存切割的缺口
    imagecrop.convert('RGB').save(save_path + '\\' + "new_image.jpg")
    imagecrop.show()
    return int(round(y)) + 2


def get_position(full, words):
    """
    获取点选验证位置
    :param full:
    :param words:
    :return:
    """
    # 还原点选原图
    merge_img(full, 'click_full')
    full_path = os.path.abspath('...') + '\\' + 'images' + '\\' + 'click_full.jpg'
    full_bg = Image.open(full_path)

    # 下载点选文字图片
    words_path = _pic_download(words, 'click_words')
    text_bg = Image.open(words_path)

    # 合并
    click_img = Image.new('RGB', (260, 190))
    click_img.paste(full_bg, (0, 0))
    click_img.paste(text_bg, (0, 160))

    click_img.show()
    click_path = os.path.abspath('...') + '\\' + 'images' + '\\' + 'click_merge.jpg'
    click_img.save(click_path)

    with open(click_path, 'rb') as f:
        img_data = f.read()
    # 超级鹰识别
    ok, position = image_to_text(img_data, img_kind=9004)
    if ok:
        return position
    return None


if __name__ == '__main__':
    # position = get_position('https://captcha2.eastmoney.com/14/resources/a8af_160/3/83/83565224e1e1b9e992d0feee4d0dea43.jpg',
    #                         'https://captcha2.eastmoney.com/14/resources/a8af_160/3/83/83565224e1e1b9e992d0feee4d0dea43_words.jpg')
    # print(position)

    distance = get_distance('https://captcha2.eastmoney.com/13/resources/e02b_160/3/73/73bc88b9cb453cb71713c4694137c5f2/bg/473a0b2e.jpg',
                            'https://captcha2.eastmoney.com/13/resources/e02b_160/3/73/73bc88b9cb453cb71713c4694137c5f2/slice/473a0b2e.png')
    print(distance)
    # _cut_slider(os.path.abspath('...') + '\\' + 'images' + '\\' + 'slide_gap.jpg')
