from fractions import Fraction
import copy


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


def calculate_ds(d):
    '''
    迭代计算解
    '''
    d, s = solve(d)
    printSol(d, s)


def fast_calculate(d):
    '''
    使用scipy直接运算 先行判断是否有解
    传入格式 format之后的numpy
    '''
    # print("fast calculate")
    c = d[-1, :-1]
    A_eq = d[0:-1, 0:-1]
    b_eq = d[0:-1, -1]
    print(c, A_eq, b_eq)

    # 求解，最小化c  最大化-c
    r = optimize.linprog(-c, None, None, A_eq, b_eq, method='simplex')
    print(r)
    return r


def Find_Identity_Matrix(data):  # 找到单位矩阵，提取目标函数的价值系数
    Cb = []
    Xb = []
    for i in range(1, equation_number + 1):
        for j in range(max_number):
            flag = 0
            if data['list' + str(i)][j] == 1:  # 系数为1,其他系数在列里面全为0
                for m in range(1, i):
                    if data['list' + str(m)][j] != 0:
                        flag = 1
                for n in range(i + 1, equation_number + 1):
                    if data['list' + str(n)][j] != 0:
                        flag = 1
                if flag == 0:
                    Cb.append(data['list' + str(0)][j])
                    Xb.append(j + 1)
                    data['Cb'] = Cb
                    data['Xb'] = Xb
    return data  # Tip:带有Cb和Xb的，下次可以直接迭代


def check_number(data):  # 检验数生成
    check_list = []
    for j in range(max_number):
        check_number = int(data['list0'][j])
        for i in range(1, equation_number + 1):
            # print('check_number'+str(check_number)+'\n')
            # print(str(data['list'+str(i)][j])+'*'+str(data['Cb'][i-1]))
            check_number = check_number - data['list' + str(i)][j] * data['Cb'][i - 1]
        check_list.append(check_number)
    data['check'] = check_list
    return data


def check(data):
    max_number = max(data['check'])
    if max_number <= 0:
        return True  # 找到最优解
    else:
        return False


def circulate(data):
    max_number_x = max(data['check'])
    pos_x = data['check'].index(max_number_x)  # 求出检验数最小非零项的下标
    Theta = []
    for i in range(1, equation_number + 1):  # 求Theta
        if data['list' + str(i)][pos_x] == 0 or data['b'][i - 1] == 0:  # Theta为0，设为最大,也保证了找到的下标值即除数不为0
            Theta.append(10000000)
        else:
            Theta_tmp = data['b'][i - 1] / data['list' + str(i)][pos_x]
            if Theta_tmp > 0:  # Theta为负数，设为最大
                Theta.append(Theta_tmp)
            else:
                Theta.append(10000000)
    data['Theta'] = Theta
    pos_y = Theta.index(min(Theta))
    Divisor = data['list' + str(pos_y + 1)][pos_x]  # 找到的数即除数
    for i in range(max_number):
        v = data['list' + str(pos_y + 1)][i]
        data['list' + str(pos_y + 1)][i] = v / Divisor  # 整行除以除数
    data['b'][pos_y] = data['b'][pos_y] / Divisor  # b变化
    b = data['b'][pos_y]  # 保存下现在的b，后面用于变化其他的b
    for i in range(1, equation_number + 1):
        pos_x_move = data['list' + str(i)][pos_x]  # 先保存下基变量那一列对应的数，用于算出倍数，然后其他相减
        if i != pos_y + 1:  # 换出的这一行不用变了
            for j in range(max_number):  # 这一行系数变化
                data['list' + str(i)][j] = data['list' + str(i)][j] - pos_x_move * (data['list' + str(pos_y + 1)][j])
            # 价值系数也要变一下
            data['b'][i - 1] = data['b'][i - 1] - b * pos_x_move
    data['Xb'][pos_y] = pos_x + 1  # Xb变化
    data['Cb'][pos_y] = data['list0'][pos_x]


# def unsolved(data) #无解

def iteration(rst, i):  # 检验数判断
    data = copy.deepcopy(rst['flag' + str(i)])  # 深度copy
    if check(data) == False:  # 判断检验数   && unsolved(data)
        circulate(data)  # 算Theta和换的值 xb Cb
        # ---------------------------------------------------------------
        # 这样很不幸的是上一张表的Theta值和替换掉的xb,Cb传入下一个中去了，后面要写个函数变一下
        # ===============================================================
        # data = Find_Identity_Matrix(data) #找单位矩阵的
        # 因为在circulate函数中已经变换的xb Cb,对应的就是单位矩阵,所以就没必要Find_Identity_Matrix()了
        data = check_number(data)
        i = i + 1
        rst['flag' + str(i)] = data
        iteration(rst, i)


def qianduan(rst):
    b = []
    Cb = []
    Xb = []
    check = []
    Theta = []
    list_all = []
    for i in range(len(rst)):
        list_one = []
        for j in range(equation_number):
            list_one.append((rst['flag' + str(i)]['list' + str(j + 1)]))
        # print(list_one)
        list_all.append(list_one)
        b.append(rst['flag' + str(i)]['b'])
        Cb.append(rst['flag' + str(i)]['Cb'])
        Xb.append(rst['flag' + str(i)]['Xb'])
        check.append(rst['flag' + str(i)]['check'])
        if ('Theta' in rst['flag' + str(i)]):
            Theta.append(rst['flag' + str(i)]['Theta'])
    tmp = {}
    tmp['cj'] = rst['flag0']['list0']
    tmp['b'] = b
    tmp['Cb'] = Cb
    tmp['Xb'] = Xb
    tmp['check'] = check
    tmp['Theta'] = Theta
    tmp['list'] = list_all

    return tmp


def main(data):
    global max_number, equation_number  # 全局一下，很多函数要用
    max_number = int(data['max_number'])
    equation_number = int(data['equation_number'])
    # data = create_data(data)  # 从前端生成数据
    data = format_data(data)
    print(data)
    data = Find_Identity_Matrix(data)  # 找单位矩阵
    data = check_number(data)  # 算检验数字
    rst = {}
    rst['flag0'] = data
    iteration(rst, 0)
    # Theta变化
    first = True
    for value in rst.values():
        if first:
            first = False
        else:
            temp["Theta"] = value["Theta"]
        temp = value
    del temp["Theta"]
    # 结束

    # 前端数据对接
    rst = qianduan(rst)
    return rst


import numpy as np
import numpy as np


def solve(d):
    '''
    输出dset格式为
    v| 松弛变量 | b | out(theta) | s
    target
    '''
    (bn, cn) = d.shape
    s = list(range(cn - bn, cn - 1))  # 基变量列表
    format = np.hstack((np.array(s + [0.]).reshape(len(s) + 1, 1), d[..., -1].reshape(len(d), 1), d[..., :-1]))

    dset = []
    oiset = []
    sset = []
    while max(d[-1][:-1]) > 0:
        # print(d)
        jnum = np.argmax(d[-1][:-1])  # 转入下标
        out = d[:-1, -1] * 1.0 / np.maximum(0, d[:-1, jnum])
        np.place(out, np.isinf(out), 100001)  # np.nan替换为np.inf
        # np.place(out, np.isinf(out), -10000)
        inum = np.argmin(out)  # 转出下标
        s[inum] = jnum  # 更新基变量
        d[inum] /= d[inum][jnum] * 1.0
        for i in range(bn):
            if i != inum:
                d[i] -= d[i][jnum] * d[inum]
        print("转出" + inum.__str__() + " 转入" + jnum.__str__())
        out_tmp = np.append(out, 0.)
        s_tmp = s + [0.]
        table = np.hstack((np.array(s_tmp).reshape(len(s_tmp), 1), d[..., -1].reshape(len(d), 1), d[..., :-1],
                           np.array(out_tmp).reshape(len(out_tmp), 1)))
        dset.append(table.tolist())
        oiset.append([inum.__str__(), jnum.__str__()])
    return dset, oiset, format


def printSol(d, s):
    for i in range(d.shape[1] - 1):
        print("x%d=%.2f" % (i, d[s.index(i)][-1] if i in s else 0))
    print("objective is %.2f" % (-d[-1][-1]))


if __name__ == '__main__':
    dstr = [[2, 2, 1, 0, 0, 0, 12],
            [1, 2, 0, 1, 0, 0, 8],
            [4, 0, 0, 0, 1, 0, 16],
            [0, 4, 0, 0, 0, 1, 12],
            [2, 3, 0, 0, 0, 0, 0]]
    d = np.array(dstr).astype(np.float)
    d, s = solve(d)
    printSol(d, s)

from scipy import optimize
import numpy as np
