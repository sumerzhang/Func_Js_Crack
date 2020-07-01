# -*- coding: utf-8 -*-
# @Time    : 2019/11/1 18:48
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : get_trace.py
# @Software: PyCharm

import math
import numpy as np
import random


def _generate_trace(distance):
    """
    生成轨迹
    :param distance:
    :return:
    """
    sy = [0, 1, -1, 0, 0, 0, 0, -1, 0, 0, 0, -1, -1, 0, 0, 1]
    # 位移/轨迹列表
    tracks_list = []
    # 当前的位移
    current = 0
    while current <= distance - 35:
        move = random.randint(12, 30)
        current += move
        tracks_list.append(current)
    # 减速慢慢滑
    if current < distance - 12:
        move = random.randint(9, 12)
        current += move
        tracks_list.append(current)
    for i in range(round(current) + 1, distance + 1, 3):
        if current < distance - 3:
            current += 3
            tracks_list.append(current)
        else:
            tracks_list.append(distance)
    # 生成时间戳列表
    timestamp_list = []
    start = random.randint(100, 110)
    timestamp = start
    for i in range(len(tracks_list)):
        t = random.randint(99, 101)
        timestamp += t
        timestamp_list.append(timestamp)
        i += 1
    yy = random.randint(5, 8)
    trace = [[0, yy, random.choice([0, 1])], [0, yy, start]]
    for index, x in enumerate(tracks_list):
        trace.append([x, random.choice(sy), timestamp_list[index]])
    trace.append([distance, random.choice(sy), timestamp_list[-1] + random.randint(99, 101)])
    return trace


def generate_trace(space):
    x = [0, 0]
    y = [0, 0, 0]
    z = [0]
    # x
    count = np.linspace(-math.pi / 2, math.pi / 2, random.randrange(20, 30))
    # print(count)
    func = list(map(math.sin, count))
    nx = [i + 1 for i in func]
    add = random.randrange(10, 15)
    sadd = space + add
    x.extend(list(map(lambda x: x * (sadd / 2), nx)))
    # x.extend(np.linspace(sadd, space, 4 if add > 12 else 3))
    x.extend(np.linspace(sadd, space, 3 if add > 12 else 2))
    x = [math.floor(i) for i in x]
    # y
    for i in range(len(x) - 2):
        if y[-1] < 30:
            y.append(y[-1] + random.choice([0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0]))
        else:
            y.append(y[-1] + random.choice([0, 0, -1, -1, 0, 0, -1, 0, 0, 0, 0, 0]))
    # z
    for i in range(len(x) - 1):
        z.append((z[-1] // 100 * 100) + 100 + random.choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2]))
    return list(map(list, zip(x, y, z)))
