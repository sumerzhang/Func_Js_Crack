# -*- coding: utf-8 -*-
# @Time    : 2019/10/19 13:52
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : get_trace.py
# @Software: PyCharm

import numpy as np
from numpy import *
import matplotlib.pyplot as plt


def plot_line(x, y, xrange=None, yrange=None):
    """
    :param x: x list
    :param y: y list
    :param xrange: x坐标范围
    :param yrange: y坐标范围
    :return: 画出折线图
    """
    fig = plt.figure()
    ax = fig.add_subplot(3, 2, 1)
    ax.plot(np.array(x), np.array(y))

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    if not xrange:
        ax.set_xlim(xrange)
    if not yrange:
        ax.set_ylim(yrange)

    ax.invert_yaxis()
    plt.show()


def get_func(x, y):
    """
    传入xlist, ylist
    list长度3
    生成一个一元二次方程
    :param x:
    :param y:
    :return:
    """
    if len(x) != len(y):
        raise Exception("Error: len(x) != len(y)")
    temp_mat = mat(zeros((3, 3)))
    for i in range(0, 3):
        temp_mat[0, i] = pow(x[i], 2)
        temp_mat[1, i] = x[i]
        temp_mat[2, i] = 1
    temp_mat_inv = np.linalg.inv(temp_mat)
    temp_y = mat(array(y))
    parameter_abc = temp_y * temp_mat_inv
    list_abc = []
    for i in range(0, 3):
        list_abc.append(parameter_abc[0, i])
    return list_abc


def generate_trace(position, size):
    """
    生成轨迹
    :param position: 手势的四个坐标
    :param size: 验证码图片尺寸
    :return:
    """
    x = []
    y = []
    for i in position:
        x.append(int(i.split(',')[0]))
        y.append(int(i.split(',')[1]))

    trace_x = []
    trace_y = []
    for _ in range(0, 2):
        tepx = [x[_], x[_ + 1], x[_ + 2]]
        tepy = [y[_], y[_ + 1], y[_ + 2]]
        [a, b, c] = get_func(tepx, tepy)
        if _ == 0:
            for i in range(x[0], x[1]):
                trace_x.append(i)
                trace_y.append(a * i * i + b * i + c)
            for i in range(x[1], x[2]):
                trace_x.append(i)
                if random.randint(1, 5) == 1:
                    trace_y.append((((float)(y[2] - y[1])) / (x[2] - x[1])) * (i - x[1]) + y[1] + random.randint(-1, 1))
                else:
                    trace_y.append((((float)(y[2] - y[1])) / (x[2] - x[1])) * (i - x[1]) + y[1])
        else:
            for i in range(x[2], x[3]):
                trace_x.append(i)
                trace_y.append(a * i * i + b * i + c)
    trace_x = [int(i) for i in trace_x]
    trace_y = [int(i) for i in trace_y]
    last_trace_x = []
    last_trace_y = []
    plot_line(trace_x, trace_y, [0, size[0]], [0, size[1]])
    xx = 0
    while xx < len(trace_x) - 1:
        last_trace_x.append(trace_x[xx])
        last_trace_y.append(trace_y[xx])
        xx += random.randint(1, 4)
    last_trace_x.append(trace_x[-1])
    last_trace_y.append(trace_y[-1])

    timestamp_list = [random.randint(5, 20)]
    timestamp = random.randint(100, 200)
    for i in range(len(last_trace_x) - 1):
        t = random.randint(6, 18)
        timestamp += t
        timestamp_list.append(timestamp)
        i += 1

    trace = []
    for i in range(0, len(last_trace_x)):
        trace.append({
            'x': last_trace_x[i],
            'y': last_trace_y[i],
            'time': timestamp_list[i] + int(''.join([random.choice(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']) for _ in range(14)])) * 0.00000000000001
        })

    return trace

