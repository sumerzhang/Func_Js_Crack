# -*- coding: utf-8 -*-
# @Time    : 2019/10/18 16:03
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : get_trace.py
# @Software: PyCharm

import time
import math
import random


def get_trace(distance):
    """
    生成轨迹
    :param distance:
    :return:
    """
    back = random.randint(2, 6)
    distance += back

    base_x = 851
    base_y = 342
    # 初速度
    v = 0
    # 位移/轨迹列表，列表内的一个元素代表0.02s的位移
    tracks_list = []
    # 当前的位移
    current = 0
    while current < distance - 13:
        # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
        a = random.randint(10000, 12000)  # 加速运动
        # 初速度
        v0 = v
        t = random.randint(9, 18)
        s = v0 * t / 1000 + 0.5 * a * ((t / 1000) ** 2)
        # 当前的位置
        current += s
        # 速度已经达到v,该速度作为下次的初速度
        v = v0 + a * t / 1000
        # 添加到轨迹列表
        if current < distance:
            tracks_list.append(round(current))
    # 减速慢慢滑
    if round(current) < distance:
        for i in range(round(current) + 1, distance + 1):
            tracks_list.append(i)
    else:
        for i in range(tracks_list[-1] + 1, distance + 1):
            tracks_list.append(i)
    # 回退
    for _ in range(back):
        current -= 1
        tracks_list.append(round(current))
    if tracks_list[-1] != distance - back:
        if tracks_list[-1] - distance + back > 0:
            for j in range(tracks_list[-1] - distance + back):
                current -= 1
                tracks_list.append(round(current))
        else:
            for j in range(distance - back - tracks_list[-1]):
                current += 1
                tracks_list.append(round(current))
    # 生成时间戳列表
    timestamp = int(time.time() * 1000)
    timestamp_list = [timestamp]
    time.sleep(random.uniform(0.5, 1.5))
    for i in range(1, len(tracks_list)):
        t = random.randint(11, 18)
        timestamp += t
        timestamp_list.append(timestamp)
        i += 1
    y_list = []
    for j in range(len(tracks_list)):
        y = random.choice(
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0])
        y_list.append(y)
        j += 1
    trace = [[str(base_x), str(base_y), timestamp_list[0]]]
    x_offset = random.randint(20, 40)
    y_offset = random.randint(20, 40)
    for index, x in enumerate(tracks_list):
        trace.append([str(base_x + x_offset + x), str(base_y + y_offset + y_list[index]), timestamp_list[index]])
    return trace


def generate_trace(distance):
    """
    生成轨迹
    :param distance:
    :return:
    """
    start_x = random.randint(860, 880)
    start_y = random.randint(355, 375)

    stage1 = 0.4
    stage2 = 0.7

    tracks_list = [0]
    current = 0
    while current <= distance:
        if current <= distance * stage1:
            x_move = random.randint(3, 6)
        elif distance * stage1 < current <= distance * stage2:
            x_move = random.randint(1, 3)
        else:
            x_move = random.choice([0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0])
        current += x_move
        tracks_list.append(current)
    # tracks_list.append(distance)
    # 生成时间戳列表
    timestamp = int(time.time() * 1000)
    timestamp_list = [timestamp]
    for i in range(1, len(tracks_list)):
        if i == 1:
            t = random.randint(150, 250)
        elif len(tracks_list) - 10 <= i < len(tracks_list) - 4:
            t = random.randint(20, 40)
        elif i >= len(tracks_list) - 4:
            t = random.randint(50, 150)
        else:
            t = random.randint(6, 9)
        timestamp += t
        timestamp_list.append(timestamp)
        i += 1
    y_list = []
    for j in range(len(tracks_list)):
        y = random.choice(
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0])
        y_list.append(y)
        j += 1
    trace = [["851", "342", timestamp_list[0]]]
    for index, x in enumerate(tracks_list):
        trace.append([str(start_x + x), str(start_y + y_list[index]), timestamp_list[index]])
    return trace[:-2]


def generate_trace2(distance):
    base_x = 851
    base_y = 342

    # 移动轨迹
    tracks = []
    # 当前位移
    current = 0
    # 减速阈值
    mid = distance * 4 / 5
    # 时间间隔
    t = 0.2
    # 初始速度
    v = 0

    while current < distance:
        if current < mid:
            a = random.uniform(2, 5)
        else:
            a = -(random.uniform(12.5, 13.5))
        v0 = v
        v = v0 + a * t
        x = v0 * t + 1 / 2 * a * t * t
        current += math.ceil(round(x))

        if 0.6 < current - distance < 1:
            x = x - 0.53
            tracks.append(math.ceil(math.ceil(round(x, 2))))

        elif 1 < current - distance < 1.5:
            x = x - 1.4
            tracks.append(math.ceil(round(x, 2)))
        elif 1.5 < current - distance < 3:
            x = x - 1.8
            tracks.append(math.ceil(round(x, 2)))

        else:
            tracks.append(math.ceil(round(x, 2)))

    print(tracks, sum(tracks))
    return tracks


def get_trace_2(distance):
    base_x = 851
    base_y = 342

    # 创建存放轨迹信息的列表
    tracks_list = []
    # 设置加速的距离
    faster_distance = distance * 3 / 5

    # 设置初始位置、初始速度、时间间隔
    start, v0, t = 0, 0.5, 0.2
    # 当尚未移动到终点时
    while start < distance:
        # 如果处于加速阶段
        if start < faster_distance:
            # 设置加速度为2
            a = round(random.uniform(0.5, 0.8), 2)
        # 如果处于减速阶段
        else:
            # 设置加速度为-3
            a = round(random.uniform(-0.7, -0.9), 2)
        # 移动的距离公式
        move = v0 * t + 1 / 2 * a * t * t
        move = int(move)
        # 此刻速度
        v = v0 + a * t
        # 重置初速度
        v0 = v
        # 重置起点
        start += move
        # 将移动的距离加入轨迹列表
        tracks_list.append(round(start))

    # 生成时间戳列表
    timestamp = int(time.time() * 1000)
    timestamp_list = [timestamp]
    time.sleep(random.uniform(0.5, 1.5))
    for i in range(1, len(tracks_list)):
        t = random.randint(11, 18)
        timestamp += t
        timestamp_list.append(timestamp)
        i += 1
    y_list = []
    for j in range(len(tracks_list)):
        y = random.choice(
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
             0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0])
        y_list.append(y)
        j += 1
    trace = [[str(base_x), str(base_y), timestamp_list[0]]]
    x_offset = random.randint(20, 40)
    y_offset = random.randint(20, 40)
    for index, x in enumerate(tracks_list):
        trace.append([str(base_x + x_offset + x), str(base_y + y_offset + y_list[index]), timestamp_list[index]])
    return trace




x = [["851", "342", 1571388235200], ["875", "358", 1571388235200], ["877", "358", 1571388235419],
     ["880", "358", 1571388235426], ["884", "358", 1571388235433], ["887", "358", 1571388235442],
     ["890", "358", 1571388235448], ["893", "359", 1571388235455], ["895", "359", 1571388235462],
     ["898", "360", 1571388235470], ["900", "360", 1571388235477], ["903", "360", 1571388235485],
     ["907", "361", 1571388235492], ["911", "362", 1571388235498], ["917", "362", 1571388235506],
     ["921", "362", 1571388235513], ["926", "362", 1571388235522], ["929", "362", 1571388235528],
     ["932", "362", 1571388235535], ["934", "362", 1571388235543], ["936", "362", 1571388235550],
     ["937", "362", 1571388235557], ["939", "362", 1571388235564], ["941", "362", 1571388235572],
     ["942", "362", 1571388235579], ["943", "362", 1571388235586], ["945", "362", 1571388235594],
     ["947", "362", 1571388235601], ["949", "362", 1571388235608], ["950", "362", 1571388235615],
     ["952", "362", 1571388235623], ["954", "362", 1571388235630], ["956", "362", 1571388235638],
     ["958", "362", 1571388235645], ["961", "362", 1571388235653], ["962", "362", 1571388235661],
     ["964", "362", 1571388235667], ["966", "362", 1571388235674], ["967", "362", 1571388235681],
     ["969", "362", 1571388235689], ["970", "362", 1571388235695], ["971", "362", 1571388235703],
     ["973", "362", 1571388235711], ["975", "362", 1571388235717], ["976", "362", 1571388235725],
     ["977", "362", 1571388235732], ["978", "362", 1571388235740], ["979", "362", 1571388235747],
     ["980", "362", 1571388235754], ["981", "362", 1571388235763], ["982", "362", 1571388235776],
     ["983", "362", 1571388235783], ["984", "362", 1571388235805], ["985", "362", 1571388235834],
     ["986", "362", 1571388235849], ["987", "362", 1571388235886], ["988", "362", 1571388235944],
     ["989", "362", 1571388236002], ["991", "362", 1571388236113], ["991", "363", 1571388236206],
     ["992", "363", 1571388236221], ["992", "364", 1571388236287], ["992", "364", 1571388236419]]

# timestamp = x[0][2]
# y = [i[2] - timestamp for i in x]
# print(y)
# generate_trace2(117)
