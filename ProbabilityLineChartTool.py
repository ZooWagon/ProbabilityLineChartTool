'''
ProbabilityLineChartTool
概率折线图生成工具
给定初始点数，增长阶段数，增长率符合的概率分布，
绘制点数变化的折线图，并将点数变化情况生成csv文件。
作者：ZooWagon
时间：2022.3.11 20:20
'''

import os
import time
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image, ImageDraw, ImageFont

# 支持的概率分布代码
# 0-正态分布
support_pd = [0]
PHASE_MIN = 10
PHASE_MAX = 50000
OUT_PATH = "./result/"
OUT_FOLDER = "result"


# 欢迎
def print_hi():
    t = time.localtime(time.time())
    print("概率折线图生成工具")
    print("欢迎")
    print("当前时间：" + time.strftime("%Y-%m-%d %H:%M:%S", t))
    if not os.path.exists(OUT_FOLDER):
        os.makedirs(OUT_FOLDER)


# 读取概率分布参数
def read_pd():
    mode = eval(input("请输入概率分布代号（0-正态分布）："))
    ls = [mode]
    if mode == 0:
        e = eval(input("请输入期望（单位：%）："))
        s = eval(input("请输入标准差（单位：%）："))
        ls.append(e)
        ls.append(abs(s))
        # print(str(e), str(s))
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
    fp = open(OUT_PATH + filename, "w", encoding='utf-8-sig')
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
    plt.clf()
    pic_name = "PLCT" + time_str + ".png"
    text_s = ""
    if para_pd[0] == 0:
        text_s = "增长率服从N({:s},{:s}^2)".format(str(para_pd[1]), str(para_pd[2]))
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.plot(list(range(l)), index, color='b')
    plt.xticks(np.array(range(0, l, (l // 10))))
    # plt.text((l // 10) // 3, index[0], text_s, size=14, color="black",
    #          bbox=dict(facecolor="black", alpha=0.2))
    plt.title("增长率在概率分布下的点数模拟", size=18)
    plt.xlabel("天", size=14)
    plt.ylabel("点数", size=14)
    plt.axis("on")
    plt.savefig(OUT_PATH + pic_name)
    return pic_name, text_s


# 增加概率分布说明的图表图片
def add_figure_des(fig_name, des_text):
    img = cv2.imread(OUT_PATH + fig_name)
    white_img = np.ones([80, 640, 3]) * 255
    img = np.vstack([img, white_img])
    img = img.astype(np.uint8)
    img = cv2ImgAddText(img, des_text, 200, 500)
    out_name = fig_name.replace(".png", "_2.png")
    cv2.imwrite(OUT_PATH + out_name, img)


# 在img的(left,top)位置写汉字text
def cv2ImgAddText(img, text, left, top, text_color=(0, 0, 0), text_size=20):
    if (isinstance(img, np.ndarray)):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    fontText = ImageFont.truetype(
        "font/msyh.ttc", text_size, encoding="utf-8")
    draw.text((left, top), text, text_color, font=fontText)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


# 程序错误处理
# 0：未定义概率分布
# 1： 不合法阶段参数
def err_handler(err_code):
    if err_code == 0:
        print("请输入正确的概率分布代码。")
    elif err_code == 1:
        print("请输入正确的阶段参数。")
    print("请重新输入")
    print_cutting_line()


# 打印分割线
def print_cutting_line():
    print("%s" % ('-' * 20))


# 获取时间戳
def get_timestamp():
    t1 = time.time()
    t_local = time.localtime(t1)
    t_str = time.strftime("%Y%m%d%H%M%S", t_local)
    mm = (t1 * 1000) % 1000
    return "%s_%03d" % (t_str, mm)


# 主函数
def main():
    while True:
        print_hi()  # 欢迎
        time_str = get_timestamp()  # 时间戳
        para_pd = read_pd()  # 读取概率分布参数
        if para_pd[0] not in support_pd:
            err_handler(0)  # 不支持的概率分布
            continue
        para_ph = read_ph()  # 读取阶段参数
        if para_ph[0] < 0 or para_ph[1] < PHASE_MIN or para_ph[1] > PHASE_MAX:
            err_handler(1)
            continue
        # 模拟点数
        rate, index = simulate_index(para_pd[0], para_pd[1], para_pd[2], para_ph[0], para_ph[1])
        # 输出到文件和绘图
        out_file_name = output_to_file(rate, index, para_pd + para_ph, time_str)
        print("结果已输出到文件 " + out_file_name)
        out_figure_name, des_text = draw_index(index, time_str, para_pd)
        print("点数已绘制成折线图 " + out_figure_name)
        add_figure_des(out_figure_name, des_text)
        print("上述文件在result目录下")
        # 退出
        x = input("输入0退出工具；输入其他继续模拟：")
        if x == '0':
            print("退出")
            break
        print_cutting_line()


main()
