from fractions import Fraction
import copy
import numpy as np
from scipy.optimize import linprog

def format_date(target, matrix):
    '''
    从前端获得数据的直接传入进行格式化
    传出二维数组
    v | E |b
    target | 0
    '''
    equ_number = len(matrix)
    E = np.zeros([equ_number, equ_number])
    for i in range(equ_number):
        E[i][i] = 1
    matrix = np.array(list(map(lambda e: list(map(int, e)), matrix)))
    datar = np.hstack((matrix[..., :-1], E, matrix[..., -1].reshape(equ_number, 1)))
    target = list(map(int, target))
    target += [0] * (equ_number + 1)
    return (np.vstack((datar, target)))

def deformat_data(d_set):
    return [[['inf' if x == 100001 else str(x) for x in line] for line in d] for d in d_set]

def format_data(data):
    '''
    data: 原始数据未标准化

    '''
    max_number = int(data['max_number'])
    equation_number = int(data['equation_number'])
    datar = []
    for i in range(1, equation_number + 1):  # 系数矩阵生成
        list = []
        for j in range(1, max_number + 1):
            number = int(data['number' + str(i) + '_' + str(j)])
            list.append(number)
        base = [0] * equation_number
        base[i - 1] = 1
        list += base  # 合并初矩阵
        list.append(int(data['value' + str(i)]))
        datar.append(list)
    list = []
    for j in range(1, max_number + 1):
        number = int(data['number' + str(0) + '_' + str(j)])
        list.append(number)
    list += [0] * (equation_number + 1)
    datar.append(list)
    return datar, max_number, equation_number


def fast_calculate(d):
    '''
    使用scipy直接运算 先行判断是否有解
    传入格式 format之后的numpy
    '''
    # print("fast calculate")
    c = d[-1, :-1]
    A_eq = d[0:-1, 0:-1]
    b_eq = d[0:-1, -1]
    # print(c, A_eq, b_eq)

    # 求解，最小化c  最大化-c
    r = linprog(-c, None, None, A_eq, b_eq, method='simplex')
    # print(r)
    return r

def check(data):
    max_number = max(data['check'])
    if max_number <= 0:
        return True  # 找到最优解
    else:
        return False

def solve(d):
    '''
    输出dset格式为
    v| 松弛变量 | b | out(theta) | s
    target
    '''
    (bn, cn) = d.shape
    s = list(range(cn - bn, cn - 1))  # 基变量列表
    # format = np.hstack((np.array(s + [0.]).reshape(len(s) + 1, 1), d[..., -1].reshape(len(d), 1), d[..., :-1]))

    dset = []
    oiset = []
    sset = []
    while max(d[-1][:-1]) > 0:
        # print(d)
        jnum = np.argmax(d[-1][:-1])  # 转入下标
        out = d[:-1, -1] * 1.0 / np.maximum(0, d[:-1, jnum])
        np.place(out, np.isinf(out), 100001)  # np.nan替换为np.inf
        inum = np.argmin(out)  # 转出下标
        out_tmp = np.append(out, 0.)
        s_tmp = s + [0.]
        table = np.hstack((np.array(s_tmp).reshape(len(s_tmp), 1), d[..., -1].reshape(len(d), 1), d[..., :-1],
                           np.array(out_tmp).reshape(len(out_tmp), 1)))
        s[inum] = jnum  # 更新基变量
        d[inum] /= d[inum][jnum] * 1.0
        for i in range(bn):
            if i != inum:
                d[i] -= d[i][jnum] * d[inum]
        # print("转出" + inum.__str__() + " 转入" + jnum.__str__())

        # table = np.hstack((np.array(s_tmp).reshape(len(s_tmp), 1), d[..., -1].reshape(len(d), 1), d[..., :-1],
        #                    np.array(out_tmp).reshape(len(out_tmp), 1)))
        dset.append(np.round(table, 2).tolist())
        oiset.append([inum.__str__(), jnum.__str__()])
        # print(table)

    format = np.round(
        np.hstack((np.array(s + [0.]).reshape(len(s) + 1, 1), d[..., -1].reshape(len(d), 1), d[..., :-1])), 2).tolist()
    return dset, oiset, format