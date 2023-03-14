import numpy as np
from flask import jsonify


def transferStrToFloat(mat):
    return [[float(e) for e in mat[i]] for i in range(len(mat))]

def transferStrToInt(mat):
    return [[int(e) for e in mat[i]] for i in range(len(mat))]

def bestPure(mat):
    '''
    输入 对策绝阵matrix
    输出 [鞍点数值，（鞍点x,y）]
    '''
    mat = np.array(transferStrToFloat(mat))
    col_max = [(np.max(mat[:, j]).tolist(), (i, j)) for i in range(len(mat)) for j in range(len(mat[i])) if
               mat[i][j] == np.max(mat[:, j])]
    row_min = [(np.min(mat[i]).tolist(), (i, j)) for i in range(len(mat)) for j in range(len(mat[i])) if
               mat[i][j] == np.min(mat[i])]
    print(set(col_max) & set(row_min))
    result = []
    for s in set(col_max) & set(row_min):
        result.append([s[0], np.array(s[1]).tolist()])
    # print(type(result[0][0]))
    return result, col_max, row_min, "该对策没有单纯最优解" if len(result) == 0 else "解答成功"


def bestMixed(matrix):
    '''
    输入：策略矩阵
    输出：col [prob_,V]  row[prob_,V]
    '''
    row_mat = np.asarray(transferStrToFloat(matrix), dtype=np.float64)
    col_mat = row_mat.T

    row_tmp, col_tmp = row_mat, col_mat

    # 甲/列
    col_num = len(col_mat)
    row_num = len(row_mat)  # 列元素个数
    row_mat = np.hstack((row_mat, np.array([-1] * row_num).reshape(row_num, 1)))
    row_mat = np.vstack((row_mat, np.array([1] * col_num + [0])))

    # 乙/行
    col_mat = np.hstack((col_mat, np.array([-1] * col_num).reshape(col_num, 1)))
    col_mat = np.vstack((col_mat, np.array([1] * row_num + [0])))

    print(col_mat,np.array([0] * col_num + [1]))
    col_result = np.linalg.solve(col_mat, np.array([0] * col_num + [1]))
    row_result = np.linalg.solve(row_mat, np.array([0] * row_num + [1]))

    print(np.round(col_result, decimals=2).tolist(), np.round(row_result,
                                                              decimals=2).tolist(), col_tmp.tolist(), row_tmp.tolist())
    return [np.round(col_result, decimals=2).tolist(), np.round(row_result,
                                                                decimals=2).tolist()], col_tmp.tolist(), row_tmp.tolist()

# result = bestPure([[1, 1, 1], [1, -2, -3], [3, -2, 3]])
# print(result)
# print(bestMixed([[7, 4], [3, 6]]))
