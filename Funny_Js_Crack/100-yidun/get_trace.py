# -*- coding: utf-8 -*-
# @Time    : 2019/11/1 21:59
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : get_trace.py
# @Software: PyCharm

import time
import random


def _generate_trace(distance, start_time):
    """
    生成轨迹
    :param distance:
    :param start_time:
    :return:
    """
    trace = []
    for index, x in enumerate(tracks_list):
        trace.append([x, y_list[index], timestamp_list[index] - start_time])
    return trace
