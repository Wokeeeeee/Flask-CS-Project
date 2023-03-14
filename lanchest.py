import numpy as np
import matplotlib.pyplot as plt


def predict(R0, B0, a, b, mode):
    if mode == "squareLaw":
        R0_square = R0 ** 2  # 红方兵力的平方
        B0_square = B0 ** 2  # 蓝方兵力的平方
        if R0_square * b > B0_square * a:  # 根据平方律的胜负条件做比较
            return "red"
        else:
            return "blue"
    else:
        if R0 * b > B0 * a:
            return "red"
        else:
            return "blue"


def firstLinearLaw(R, B, a, b, t):
    R.append(R[t] - a)
    B.append(B[t] - b)
    return R, B


def secondLinearLaw(R, B, a, b, t):
    k = b * 1.0 * R[0] / (a * B[0])
    rb = np.exp(-1 * a * B[0] * (k - 1) * t)
    R.append(-1 * R[0] * (k - 1) / (rb - k))
    B.append(-1 * B[0] * (k - 1) * rb / (rb - k))
    return R, B


def SquareLaw(R, B, a, b, t):
    ch = lambda x: (np.exp(x) + np.exp(-x)) / 2
    sh = lambda x: (np.exp(x) - np.exp(-x)) / 2
    R.append(R[0] * ch(np.sqrt(a * b) * t) - (np.sqrt(b * 1.0 / a) * B[0]) * sh(np.sqrt(a * b) * t))
    B.append(B[0] * ch(np.sqrt(a * b) * t) - (np.sqrt(a * 1.0 / b) * R[0]) * sh(np.sqrt(a * b) * t))
    return R, B


def lanchestLaw(R0, B0, a, b, mode):
    R = [R0, ]  # 用于记录红方兵力变化的列表
    B = [B0, ]  # 用于记录蓝方病理变化的列表

    T = 1000  # 仿真总步长
    dt = 1  # 时间间隔
    total_t = 0
    winner = ""
    if mode == "firstLinear":  # 采用平方律的战斗过程
        # 预测战斗进程
        winner = predict(R0, B0, a, b, mode)
        for t in np.arange(0, T, dt):
            firstLinearLaw(R, B, a, b, t)
            if R[-1] < 1e-10 or B[-1] < 1e-10:
                total_t = t + 1
                break
    elif mode == "secondLinear":  # 采用线性律的战斗过程
        winner = predict(R0, B0, a, b, mode)
        for t in np.arange(0, T, dt):
            secondLinearLaw(R, B, a, b, t)
            if R[-1] < 1e-10 or B[-1] < 1e-10:
                total_t = t + 1
                break
    elif mode == "squareLaw":
        winner = predict(R0, B0, a, b, mode)
        for t in np.arange(0, T, dt):
            SquareLaw(R, B, a, b, t)
            if R[-1] < 1e-10 or B[-1] < 1e-10:
                total_t = t + 1
                break
    return winner, [round(x, 2) for x in R], [round(x, 2) for x in B], total_t


if __name__ == '__main__':
    # 第一线性方程样例    x0=12,y0=12 a=1/15 b=1/10    -> red t=120 red-left=4
    winner, R, B, t = lanchestLaw(12, 12, 1.0 / 15, 1.0 / 10, "firstLinear")
    print("第一线性：", winner, int(R[-1]), int(B[-1]), t)
    print(len(B))

    winner, R, B, t = lanchestLaw(50, 15, 3, 1, "secondLinear")
    print("第二线性：", winner, int(R[-1]), int(B[-1]), t)

    winner, R, B, t = lanchestLaw(1000, 500, 0.01, 0.01, "squareLaw")
    print("平方律：", winner, int(R[-1]), int(B[-1]), t)
