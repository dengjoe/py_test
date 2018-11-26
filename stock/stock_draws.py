#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' use matplotlib module to draw stock data'

__author__ = 'kevin deng'


import collections
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pylab import mpl
import stock_calculate

# https://blog.csdn.net/u010758410/article/details/71743225
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题




# 根据数据进行作图
def data_item_plot(sid, data, item, xlabel, ylabel):
    # x轴的数值和年份显示 data.index.year.values是numpy.ndarray对象
    x_0 = list(range(len(data)))
    x_names = data.index.year.values.tolist()
    x_names.reverse()
    # print(x_names)

    # plt.title(item)
    values = data[item].values.tolist()
    values.reverse()
    print("%s:\n" % item, values)
    plt.plot(values)

    # 图示
    plt.legend([sid], loc='upper left')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(x_0, x_names, rotation=90)
    plt.grid(True)
    # plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y',alpha=0.4)
    # plt.savefig(r'pic/%s_%s.png' % (sid,ratio,))
    plt.show();
    return

# 根据数据进行作bar图
def data_bar(sid, data, item, xlabel, ylabel):
    # x轴的数值要按年份显示，需要生成和转换
    x_0 = list(range(len(data)))
    x_names = data.index.year.values.tolist()
    x_names.reverse()
  
    # Y轴如果是数字，则自动根据数值来设置，不需要单独设

    bar_width = 0.35
    values = data[item].values.tolist()
    values.reverse()
    plt.bar(x_0, values, bar_width, color='b')

    # 图示 xy轴
    plt.legend([sid], loc='upper left')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(x_0, x_names, rotation=90)
    plt.grid(True)

    # plt.savefig(r'pic/%s_%s.png' % (sid,ratio,))
    plt.show();
    return


# 股票代码，输入年份（如年报数据只到2016年，则输入2017）
def plot_stock(sid):
    # 读取年报分析数据
    data = stock_calculate.get_stock_data(sid, 12)
    data_item_plot(sid, data, '营业收入', "Year", "营业收入(百万)")
    data_item_plot(sid, data, '净资产收益率', "Year", "净资产收益率")
    data_bar(sid, data, '负债率', "Year", "负债率")



if __name__=='__main__':
    plot_stock("SH600519")
    # plot_stock("SH601668", 2018)
