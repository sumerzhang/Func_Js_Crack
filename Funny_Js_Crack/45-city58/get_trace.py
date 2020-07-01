# -*- coding: utf-8 -*-
# @Time    : 2019/10/18 12:24
# @Author  : Esbiya
# @Email   : 18829040039@163.com
# @File    : get_trace.py
# @Software: PyCharm


import random
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


def generate_gesture_trace(position):
    """
    生成手势验证码轨迹
    :param position:
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
    plot_line(trace_x, trace_y, [0, 280], [0, 158])
    xx = 0
    while xx < len(trace_x) - 1:
        last_trace_x.append(trace_x[xx])
        last_trace_y.append(trace_y[xx])
        xx += random.randint(1, 4)
    last_trace_x.append(trace_x[-1])
    last_trace_y.append(trace_y[-1])

    timestamp_list = []
    timestamp = random.randint(180, 220)
    for i in range(len(last_trace_x)):
        t = random.randint(5, 10)
        timestamp += t
        timestamp_list.append(timestamp)
        i += 1
    trace = [{
        'p': ','.join([str(last_trace_x[0]), str(last_trace_y[0])]),
        't': 1
    }]
    for i in range(len(last_trace_x)):
        trace.append({
            'p': ','.join([str(last_trace_x[i]), str(last_trace_y[i])]),
            't': timestamp_list[i]
        })
    trace.append({
        'p': ','.join([str(last_trace_x[-1]), str(last_trace_y[-1])]),
        't': timestamp_list[-1] + random.randint(50, 100)
    })
    return x[3] - x[0], trace


def generate_slide_trace(distance):
    """
    生成滑块验证码轨迹
    :param distance: 缺口距离
    :return:
    """
    # 轨迹删除
    for index, x in enumerate(tracks_list):
        trace.append({
            'p': ','.join([str(x + start_x), str(y_list[index] + start_y)]),
            't': timestamp_list[index]
        })
    trace.append({
        'p': f'{tracks_list[-1] + start_x},{y_list[-1] + start_y}',
        't': timestamp_list[-1] + random.randint(100, 300)
    })
    return trace


def process_trace(trace):
    """
    处理轨迹
    :param trace: 轨迹
    :return:
    """
    merge = lambda s: ','.join([str(s['p']), str(s['t'])])
    new_trace = '|'.join([merge(i) for i in trace]) + '|'
    return new_trace


if __name__ == '__main__':
    pass
