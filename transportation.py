# Vogel法寻找初始基可行解+位势法判断解的最优性
import numpy as np
import copy
import pandas as pd


def TP_split_matrix(mat):
    # print(mat)
    mat = np.array(list(map(lambda e: list(map(int, e)), mat)))
    c = mat[:-1, :-1]
    a = mat[:-1, -1]
    b = mat[-1, :-1]
    # print(mat)
    return c, a, b


def TP_vogel(var):  # Vogel法代码，变量var可以是以numpy.ndarray保存的运输表，或以tuple或list保存的(成本矩阵,供给向量,需求向量)
    import numpy
    total_cost = 0
    typevar1 = type(var) == numpy.ndarray
    typevar2 = type(var) == tuple
    typevar3 = type(var) == list
    c_set = []
    message_set = []
    x_set = []
    if typevar1 == False and typevar2 == False and typevar3 == False:
        # print('>>>非法变量<<<')
        (cost, x) = (None, None)
    else:
        if typevar1 == True:
            [c, a, b] = TP_split_matrix(var)
        elif typevar2 == True or typevar3 == True:
            [c, a, b] = var
        cost = copy.deepcopy(c)
        x = np.zeros(c.shape)
        M = pow(10, 9)
        for factor in c.reshape(1, -1)[0]:
            while int(factor) != M:
                if np.all(c == M):
                    break
                else:
                    message = ""
                    # print('c:\n', c)
                    # 获取行/列最小值数组
                    row_mini1 = []
                    row_mini2 = []
                    for row in range(c.shape[0]):
                        Row = list(c[row, :])
                        row_min = min(Row)
                        row_mini1.append(row_min)
                        Row.remove(row_min)
                        row_2nd_min = min(Row)
                        row_mini2.append(row_2nd_min)
                    # print(row_mini1,'\n',row_mini2)
                    r_pun = [row_mini2[i] - row_mini1[i] for i in range(len(row_mini1))]
                    # print('行罚数：', r_pun)
                    # 计算列罚数
                    col_mini1 = []
                    col_mini2 = []
                    for col in range(c.shape[1]):
                        Col = list(c[:, col])
                        col_min = min(Col)
                        col_mini1.append(col_min)
                        Col.remove(col_min)
                        col_2nd_min = min(Col)
                        col_mini2.append(col_2nd_min)
                    c_pun = [col_mini2[i] - col_mini1[i] for i in range(len(col_mini1))]
                    # print('列罚数：', c_pun)
                    message += '行罚数：' + str([i if i < M - 10000 else np.absolute(i - M) for i in r_pun])
                    message += ',列罚数：' + str([i if i < M - 10000 else np.absolute(i - M)  for i in c_pun])
                    pun = copy.deepcopy(r_pun)
                    pun.extend(c_pun)
                    # print('罚数向量：', pun)
                    max_pun = max(pun)
                    max_pun_index = pun.index(max(pun))
                    max_pun_num = max_pun_index + 1
                    # print('最大罚数：', max_pun, '元素序号：', max_pun_num)
                    message += ',最大罚数：' + (max_pun if max_pun < M - 10000 else np.absolute(max_pun - M) ).__str__()
                    if max_pun_num <= len(r_pun):
                        row_num = max_pun_num
                        # print('对第', row_num, '行进行操作：')
                        row_index = row_num - 1
                        catch_row = c[row_index, :]
                        # print(',对第', row_num, '行进行操作：', str([i if i < M - 10000 else np.absolute(i - M)  for i in r_pun]))
                        message += ',对第' + row_num.__str__() + '行进行操作：' + str(
                            [i if i < M - 10000 else np.absolute(i - M)  for i in catch_row])
                        # print(catch_row)
                        min_cost_colindex = int(np.argwhere(catch_row == min(catch_row)))
                        # print('最小成本所在列索引：', min_cost_colindex)
                        message += ',最小成本所在列索引：' + min_cost_colindex.__str__()
                        message += ',填入' + min(a[row_index], b[min_cost_colindex]).__str__()
                        if a[row_index] <= b[min_cost_colindex]:
                            x[row_index, min_cost_colindex] = a[row_index]
                            c1 = copy.deepcopy(c)
                            c1[row_index, :] = [M] * c1.shape[1]
                            b[min_cost_colindex] -= a[row_index]
                            a[row_index] -= a[row_index]
                        else:
                            x[row_index, min_cost_colindex] = b[min_cost_colindex]
                            c1 = copy.deepcopy(c)
                            c1[:, min_cost_colindex] = [M] * c1.shape[0]
                            a[row_index] -= b[min_cost_colindex]
                            b[min_cost_colindex] -= b[min_cost_colindex]
                    else:
                        col_num = max_pun_num - len(r_pun)
                        col_index = col_num - 1
                        # print('对第', col_num, '列进行操作：')
                        catch_col = c[:, col_index]
                        # print('对第', col_num, '列进行操作：', catch_col)
                        message += ',对第' + col_num.__str__() + '列进行操作：' + str(
                            [i if i < M - 10000 else np.absolute(i - M)  for i in catch_col])
                        # print(catch_col)
                        # 寻找最大罚数所在行/列的最小成本系数
                        min_cost_rowindex = int(np.argwhere(catch_col == min(catch_col)))
                        # print('最小成本所在行索引：', min_cost_rowindex)
                        message += ',最小成本所在行索引：' + min_cost_rowindex.__str__()
                        message += ',填入' + min(a[min_cost_rowindex], b[col_index]).__str__()
                        # 计算将该位置应填入x矩阵的数值（a,b中较小值）
                        if a[min_cost_rowindex] <= b[col_index]:
                            x[min_cost_rowindex, col_index] = a[min_cost_rowindex]
                            c1 = copy.deepcopy(c)
                            c1[min_cost_rowindex, :] = [M] * c1.shape[1]
                            b[col_index] -= a[min_cost_rowindex]
                            a[min_cost_rowindex] -= a[min_cost_rowindex]
                        else:
                            x[min_cost_rowindex, col_index] = b[col_index]
                            # 填入后删除已满足/耗尽资源系数的行/列，得到剩余的成本矩阵，并改写资源系数
                            c1 = copy.deepcopy(c)
                            c1[:, col_index] = [M] * c1.shape[0]
                            a[min_cost_rowindex] -= b[col_index]
                            b[col_index] -= b[col_index]
                    c = c1
                    # print('本次迭代后的x矩阵：\n', x)
                    # print('a:', a)
                    # print('b:', b)
                    # print('c:\n', c)
                    c_set.append(np.vstack((np.hstack((c, a.reshape(len(a), 1))), np.array(b.tolist() + [0]))).tolist())
                    x_set.append(x.tolist())
                    message_set.append(message)
        total_cost = np.sum(np.multiply(x, cost))
        if np.all(a == 0):
            if np.all(b == 0):
                print('>>>供求平衡<<<')
            else:
                print('>>>供不应求，需求方有余量<<<')
        elif np.all(b == 0):
            print('>>>供大于求，供给方有余量<<<')
        else:
            print('>>>无法找到初始基可行解<<<')
        print('>>>初始基本可行解x*：\n', x)
        print('>>>当前总成本：', total_cost)
        [m, n] = x.shape
        varnum = np.array(np.nonzero(x)).shape[1]
        if varnum != m + n - 1:
            print('【注意：问题含有退化解】')
    return cost, x, total_cost, x_set, message_set, c_set


def create_c_nonzeros(c, x):
    import numpy as np
    import copy
    nonzeros = copy.deepcopy(x)
    for i in range(x.shape[0]):
        for j in range(x.shape[1]):
            if x[i, j] != 0:
                nonzeros[i, j] = 1
    # print(nonzeros)
    c_nonzeros = np.multiply(c, nonzeros)
    return c_nonzeros


def if_dsquare(a, b):
    # print('a:', a.shape, '\n', 'b:', b.shape)
    correct = '>>>位势方程组可解<<<'
    error = '>>>位势方程组不可解，请检查基变量个数是否等于(m+n-1)及位势未知量个数是否等于(m+n)<<<'
    if len(a.shape) == 2:
        if len(b.shape) == 2:
            if a.shape[0] == a.shape[1] and a.shape == b.shape:
                print(correct)
                if_dsquare = True
            else:
                print(error)
                if_dsquare = False
        elif len(b.shape) == 1 and b.shape[0] != 0:
            if a.shape[0] == a.shape[1] and a.shape[0] == b.shape[0]:
                print(correct)
                if_dsquare = True
            else:
                print(error)
                if_dsquare = False
        else:
            print(error)
            if_dsquare = False
    elif len(a.shape) == 1:
        if len(b.shape) == 2:
            if b.shape[0] == b.shape[1] and a.shape[0] == b.shape[0]:
                print('>>>位势方程组系数矩阵与方程组值向量位置错误<<<')
                if_dsquare = 'True but not solvable'
            else:
                print(error)
                if_dsquare = False
        elif len(b.shape) == 1:
            print(error)
            if_dsquare = False
        else:
            print(error)
            if_dsquare = False
    else:
        print(error)
        if_dsquare = False
    return if_dsquare


def TP_potential(cost, x):
    message = ""
    [m, n] = x.shape
    varnum = np.array(np.nonzero(x)).shape[1]
    if varnum != m + n - 1:
        sigma = None
        message = ('【问题含有退化解，暂时无法判断最优性】')
    else:
        # print(c_nonzeros.shape)
        c_nonzeros = create_c_nonzeros(cost, x)
        cc_nonzeros = np.array(np.nonzero(c_nonzeros))
        A = []
        B = []
        length = c_nonzeros.shape[0] + c_nonzeros.shape[1]
        zeros = np.zeros((1, length))[0]
        for i in range(cc_nonzeros.shape[1]):
            zeros = np.zeros((1, length))[0]
            zeros[cc_nonzeros[0, i]] = 1
            zeros[cc_nonzeros[1, i] + c_nonzeros.shape[0]] = 1
            A.append(zeros)
            B.append(c_nonzeros[cc_nonzeros[0, i], cc_nonzeros[1, i]])
        l = [1]
        for j in range(length - 1):
            l.append(0)  # 补充一个x1=0的方程以满足求解条件
        A.append(l)
        B.append(0)
        # print(A)
        # print(B)
        A = np.array(A)
        B = np.array(B)
        judge = if_dsquare(A, B)
        if judge == True:
            sol = np.linalg.solve(A, B)  # 求解条件：A的行数（方程个数)=A的列数(变量个数）=B的个数（方程结果个数）才能解
            # print(sol)
            var = []  # 创建位势名称数组
            for i in range(c_nonzeros.shape[0]):
                var.append('u' + str(i + 1))
            for j in range(c_nonzeros.shape[1]):
                var.append('v' + str(j + 1))
            # print(var)
            solset = dict(zip(var, sol))
            # print('>>>当前位势:\n', solset)
            u = []
            v = []
            [m, n] = c_nonzeros.shape
            zero_places = np.transpose(np.argwhere(c_nonzeros == 0))
            for i in range(m):
                u.append(sol[i])
            for j in range(n):
                v.append(sol[j + m])
            for k in range(zero_places.shape[1]):
                c_nonzeros[zero_places[0, k], zero_places[1, k]] = u[zero_places[0, k]] + v[zero_places[1, k]]
            # print(c_nonzeros)
            sigma = cost - c_nonzeros
            # print('>>>检验表σ：\n', sigma)
            if np.all(sigma >= 0):
                message = '>>>TP已达到最优解<<<'
            else:
                message = '>>>TP未达到最优解<<<'
        else:
            sigma = None
            message = '>>>位势方程组不可解<<<'
    return sigma, message

# c = [
#     [4, 12, 4, 11],
#     [2, 10, 3, 9],
#     [8, 5, 11, 6]
# ]
# a = [16, 10, 22]
# b = [8, 14, 12, 14]

# mat = [
#     [4, 12, 4, 11, 6],
#     [2, 10, 3, 9, 10],
#     [8, 5, 11, 6, 22],
#     [8, 14, 12, 14, 0]
# ]
# mat = pd.read_excel('表上作业法求解运输问题.xlsx', header=None).values
# mat = pd.read_csv('表上作业法求解运输问题.csv', header=None).values
# c = np.array([[4, 12, 4, 11], [2, 10, 3, 9], [8, 5, 11, 6]])
# a = np.array([16, 10, 22])
# b = np.array([8, 14, 12, 14])
# [c, x] = TP_vogel([c, a, b])
# # [c,x]=TP_vogel([c,a,b])
# sigma = TP_potential(c, x)
# print("---------")
# print(sigma)
# print(c)
