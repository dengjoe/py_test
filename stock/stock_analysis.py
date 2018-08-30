#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test matplotlib module to draw stock'

__author__ = 'kevin deng'


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pylab import mpl

# https://blog.csdn.net/u010758410/article/details/71743225
mpl.rcParams['font.sans-serif'] = ['FangSong'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题




# 读取csv文件，转化为DataFrame格式
def get_all_data(stock_id):
    # 读取利润表数据
    lrb = pd.read_csv(r'data/%s_lrb.csv' % (stock_id),
        encoding='utf-8', header=0, index_col=None)

    list_lrb = []
    for i in lrb['报表期截止日']:
        str_i = str(i)
        # i_ = i[:4] + '-' + i[4:6] + '-' + i[6:8]
        list_lrb.append(str(i))
    list_lrb_0 = []
    for i in list_lrb:
        i_ = i[:4] + '-' + i[4:6] + '-' + i[6:8]
        list_lrb_0.append(i_)

    lrb['报告时间'] = [pd.to_datetime(t) for t in list_lrb_0]

    lrb.index = lrb['报告时间']

    data = lrb[::-1]
    return data


# 根据月份筛选数据，如12月为年报数据
def get_data_month(data, month):
    data_month = data[data.index.month == month]
    return data_month


# 筛选、计算需要的数据
def get_data_ratio(data):
    result = pd.DataFrame()
    
    result['营业收入'] = data['营业收入']/1000000
    result['归母净利润'] = data['归属于母公司所有者的净利润']/1000000
    result['营业利润'] = data['营业利润']/1000000
      
    result['营业利润率'] = data['营业利润'] / data['营业收入']
    result['净利率'] = data['归属于母公司所有者的净利润'] / data['营业收入']
    result['毛利率'] = (data['营业收入'] - data['营业成本']) / data['营业收入']
    
    result.index = data['报告时间']
    return result


# 根据数据进行作图
def data_plot(sid, data, ratio, year, kind='bar'):
    # x轴的数值和年份显示
    datalen = len(data)
    x_0 = list(range(datalen))
    x_names = tuple([str(i) for i in range(year - datalen, year)])
    print(x_names)
   
    # plt.title(ratio)
    print(data[ratio].values)

    # data[ratio].plot(kind=kind)
    plt.plot(data[ratio].values)

    # 图示
    plt.legend([sid], loc='upper left')

    plt.xlabel("Year")
    plt.ylabel(ratio+"(百万)")
    plt.xticks(x_0, x_names, rotation=90)
    plt.grid(True)
    # plt.grid(color='#95a5a6', linestyle='--', linewidth=1, axis='y',alpha=0.4)
    plt.savefig(r'pic/%s_%s.png' % (sid,ratio,))
#     plt.show();
    return

# 根据数据进行作bar图
def data_bar(sid, data, ratio, year, kind='bar'):
    # x轴的数值要按年份显示，需要生成和转换
    datalen = len(data)
    x_0 = list(range(datalen))
    x_names = tuple([str(i) for i in range(year - datalen, year)])
   
    # Y轴如果是数字，则自动根据数值来设置，不需要单独设

    bar_width = 0.35
    plt.bar(x_0, data[ratio].values, bar_width, color='b')

    # 图示
    plt.legend([sid], loc='upper left')
    # xy轴
    plt.xlabel("Year")
    plt.ylabel(ratio+"(百万)")
    plt.xticks(x_0, x_names, rotation=90)
    plt.grid(True)

    # plt.savefig(r'pic/%s_%s.png' % (sid,ratio,))
    plt.show();
    return


# 股票代码，输入年份（如年报数据只到2016年，则输入2017）
def plot_stock(sid, year):
    # 读取利润表数据
    data = get_all_data(sid)
    # 将年报数据筛选出来
    data_year = get_data_month(data, 12)
    result = get_data_ratio(data_year)

    data_plot(sid, result, '营业收入', year)
    data_bar(sid, result, '归母净利润', year)
 


if __name__=='__main__':
    plot_stock("SH600519", 2017)
    # plot_stock("SH601668", 2018)
