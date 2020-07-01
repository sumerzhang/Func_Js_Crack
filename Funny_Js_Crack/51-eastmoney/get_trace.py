# -*- coding: utf-8 -*-
# @Time    : 2019/10/24 21:28
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : get_trace.py
# @Software: PyCharm


import random


def generate_trace(distance):
    """
    生成轨迹
    :param distance:
    :return:
    """
    # 轨迹删除
    trace = [[0, 0, 0]]
    for index, x in enumerate(tracks_list[:-1]):
        trace.append([x, y_list[index], timestamp_list[index]])
    trace.append([tracks_list[-1], y_list[-1], timestamp_list[-2] + random.randint(100, 200)])
    trace.append([distance, y_list[-1], timestamp_list[-2] + random.randint(200, 300)])
    return trace

