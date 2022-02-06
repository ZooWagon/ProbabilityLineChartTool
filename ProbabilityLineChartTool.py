'''
ProbabilityLineChartTool
概率折线图生成工具
给定初始点数，增长阶段数，增长率符合的概率分布，
绘制点数变化的折线图，并将点数变化情况生成csv文件。
作者：ZooWagon
时间：2022.2.6 15:52
'''

import time
import numpy as np
import matplotlib.pyplot as plt

# 支持的概率分布代码
# 0-正态分布
support_pd = [0]
PHASE_MIN = 10
PHASE_MAX = 5000


# 欢迎
def print_hi():
    t = time.localtime(time.time())
    print("概率折线图生成工具")
    print("欢迎")
    print("当前时间：" + time.strftime("%Y-%m-%d %H:%M:%S", t))
    return t


# 读取概率分布参数
def read_pd():
    mode = eval(input("请输入概率分布（0-正态分布）："))
    ls = [mode]
    if mode == 0:
        e = eval(input("请输入期望（单位：%）："))
        s = eval(input("请输入标准差（单位：%）："))
        ls.append(e)
        ls.append(s)
    return ls


# 读取阶段参数
def read_ph():
    start_value = eval(input("请输入初始点数（正数）："))
    phase_num = eval(input("请输入变化阶段数（{:d} - {:d}正整数）：".format(PHASE_MIN, PHASE_MAX)))
    return [start_value, phase_num]


# 模拟点数变化
def simulate_index(pd_type, expectation, standard_deviation, start_index, phase_num):
    rate = []
    if pd_type == 0:  # 正态分布
        rate = expectation + standard_deviation * np.random.randn(phase_num)
    index = [start_index]
    for r in rate:
        index.append(index[-1] * (1 + r / 100))
    return rate, index


# 结果输出到文件
def output_to_file(rate, index, init_para, time_str):
    filename = "PLCT" + time_str + ".csv"
    fp = open(filename, "w", encoding='utf-8-sig')
    fp.write("概率分布代号,期望(%),标准差(%),初始点数,模拟阶段数\n")
    for i in range(len(init_para)):
        fp.write(str(init_para[i]) + "{:}".format("," if i != len(init_para) - 1 else "\n"))
    fp.write("阶段数,增长率(%),点数\n")
    fp.write("0,,{:f}\n".format(index[0]))
    for i in range(1, len(index)):
        fp.write("{:d},{:f},{:f}\n".format(i, rate[i - 1], index[i]))
    fp.close()
    return filename


# 对点数作图
def draw_index(index, time_str, para_pd):
    l = len(index)
    pic_name = "PLCT" + time_str + ".png"
    text_s = ""
    if para_pd[0] == 0:
        text_s = "增长率服从N({:.4f},{:.4f}^2)".format(round(para_pd[1], 4), round(para_pd[2], 4))
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.plot(list(range(l)), index, color='b')
    plt.xticks(np.array(range(0, l, (l // 10))))
    plt.text((l // 10) // 3, index[0], text_s, size=14, color="black",
             bbox=dict(facecolor="black", alpha=0.2))
    plt.title("增长率在概率分布下的点数模拟", size=18)
    plt.xlabel("天", size=14)
    plt.ylabel("点数", size=14)
    plt.axis("on")
    plt.savefig(pic_name)
    return pic_name


# 程序错误处理
# 0：未定义概率分布
# 1： 不合法阶段参数
def err_handler(err_code):
    if err_code == 0:
        print("请输入正确的概率分布代码。")
    elif err_code == 1:
        print("请输入正确的阶段参数。")
    print("已退出")


# 主函数
def main():
    t = print_hi()  # 欢迎
    time_str = time.strftime("%Y%m%d%H%M%S", t)  # 时间戳
    para_pd = read_pd()  # 读取概率分布参数
    if para_pd[0] not in support_pd:
        err_handler(0)  # 不支持的概率分布
        return
    para_ph = read_ph()  # 读取阶段参数
    if para_ph[0] < 0 or para_ph[1] < PHASE_MIN or para_ph[1] > PHASE_MAX:
        err_handler(1)
        return
    # 模拟点数
    rate, index = simulate_index(para_pd[0], para_pd[1], para_pd[2], para_ph[0], para_ph[1])
    # 输出到文件和绘图
    out_file_name = output_to_file(rate, index, para_pd + para_ph, time_str)
    print("结果已输出到文件 " + out_file_name)
    out_picture_name = draw_index(index, time_str, para_pd)
    print("点数已绘制成折线图 " + out_picture_name)
    # 退出
    input("按回车退出")
    print("退出")


main()
