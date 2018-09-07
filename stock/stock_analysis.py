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


# stock原始数据，保存为DataFrame格式
class StockOriginData(object):
    def __init__(self, sid):
        self._sid = sid
        __read_stock_data(sid)

    def __read_stock_data(sid):
        # 读取负债表数据
        self._fzb = pd.read_csv(r'data/%s_fzb.csv' % (stock_id),
            encoding='utf-8', header=0, index_col=None)
        add_report_time(self._fzb, "报表日期")

        # 读取利润表数据
        self._lrb = pd.read_csv(r'data/%s_lrb.csv' % (stock_id),
            encoding='utf-8', header=0, index_col=None)
        add_report_time(self._lrb, "报表期截止日")

        # 读取流量表数据
        self._llb = pd.read_csv(r'data/%s_llb.csv' % (stock_id),
            encoding='utf-8', header=0, index_col=None)
        add_report_time(self._llb, "报表期截止日") 
        return

    @property
    def fzb(self):
        return self._fzb;
    @property
    def lrb(self):
        return self._lrb;
    @property
    def llb(self):
        return self._llb;


def add_report_time(data, index_name):
    list_time = []
    for i in data[index_name]:
        str_i = str(i)
        list_time.append(str_i[:4] + '-' + str_i[4:6] + '-' + str_i[6:8])
    print(list_time)

    data['报告时间'] = [pd.to_datetime(t) for t in list_time]
    data.index = data['报告时间']
    return
    

# 
class StockCalculate(object):
    # 按类别提取数据，month 12月为年报数据，6月为半年报，3、9月为季报。
    def __init__(self, data, month):
        self._fzb = data.fzb[data.fzb.index.month == month]
        self._lrb = data.lrb[data.lrb.index.month == month]
        self._llb = data.llb[data.llb.index.month == month]

    def caculate(self):
        result = pd.DataFrame()
        result.index = self._fzb.data['报告时间']

        # 负债表
        result['货币资金'] = self._fzb.data['货币资金']/1000000
        result['应收账款'] = self._fzb.data['应收账款']/1000000
        result['资产总计'] = self._fzb.data['资产总计']/1000000
        result['应付利息'] = self._fzb.data['应付利息']/1000000
        result['应付账款'] = self._fzb.data['应付账款']/1000000
        result['负债合计'] = self._fzb.data['负债合计']/1000000
        

        # 利润表
        result['营业总收入'] = self._lrb.data['营业总收入']/1000000
        result['营业收入'] = self._lrb.data['营业收入']/1000000
        result['营业总成本'] = self._lrb.data['营业总成本']/1000000
        result['营业成本'] = self._lrb.data['营业成本']/1000000

        result['营业利润'] = self._lrb.data['营业利润']/1000000
        result['净利润'] = self._lrb.data['净利润']/1000000
        result['归母净利润'] = self._lrb.data['归属于母公司所有者的净利润']/1000000
          
        result['营业利润率'] = result['营业利润'] / result['营业收入']
        result['净利率'] = result['归母净利润'] / result['营业收入']
        result['毛利率'] = (result['营业收入'] - result['营业成本']) / result['营业收入']
        
        # 流量表
        
        return result



# 根据月份筛选数据，如12月为年报数据，6月为半年报，3、9月为季报。
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
    data = read_stock_data(sid)
    # 将年报数据筛选出来
    data_year = get_data_month(data, 12)
    result = get_data_ratio(data_year)

    # data_plot(sid, result, '营业收入', year)
    # data_bar(sid, result, '归母净利润', year)
 


if __name__=='__main__':
    plot_stock("SH600519", 2017)
    # plot_stock("SH601668", 2018)
