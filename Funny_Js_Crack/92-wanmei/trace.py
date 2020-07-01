# -*- coding: utf-8 -*-
# @Time    : 2019/10/10 17:29
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : trace.py
# @Software: PyCharm

import time
import random


def _generate_trace(distance, start_time):
    """
    生成轨迹
    :param distance:
    :return:
    """
    # 轨迹删除
    trace = [[base_x, base_y, 1, 0]]
    for index, x in enumerate(tracks_list):
        trace.append([base_x + x, base_y + y_list[index], 3, timestamp_list[index] - start_time])
    return trace[:-1]

