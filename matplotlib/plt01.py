#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
	matplotlib test
"""

import matplotlib.pyplot as plt
from pylab import mpl 

# 设置中文显示
mpl.rcParams['font.sans-serif'] = ['SimHei'] 
# 黑体	SimHei
# 微软雅黑	Microsoft YaHei
# 微软正黑体	Microsoft JhengHei
# 新宋体	NSimSun
# 新细明体	PMingLiU
# 细明体	MingLiU
# 标楷体	DFKai-SB
# 仿宋	FangSong
# 楷体	KaiTi
# 仿宋_GB2312	FangSong_GB2312
# 楷体_GB2312	KaiTi_GB2312

def plt_set_param(title, xlabel, ylabel):
	plt.title(title, fontsize=14)
	plt.xlabel(xlabel, fontsize=14)
	plt.ylabel(ylabel, fontsize=14)
	plt.tick_params(axis="both", labelsize=14)

squares = [1,4,9,16,25]

# 折线图
def plot01():
	plt.plot(squares)
	plt_set_param("Square Numbers", "value", "Square of value")
	plt.show()


def plot02():
	input_values = [1,2,3,4,5]
	plt_set_param("Square Numbers", "value", "Square of value")
	plt.plot(input_values, squares)
	plt.savefig("plt01_plot02.png")
	# plt.show()

def plot03():
	in_values = [1,2,3,4,5]
	y1 = [12,4,6,5,9]
	plt_set_param("折线图——平方", "value", "Square of value")
	plt.plot(in_values, squares)
	plt.plot(in_values, y1, color='red', linewidth=1.0, linestyle='--') # 叠加第2条折线图
	plt.savefig("plt01_plot03.png")


# 散点图
def scatter01():
	input_values = [1,2,3,4,5]
	plt_set_param("Square Numbers", "value", "Square of value")
	plt.scatter(input_values, squares, c=(0,0,0.8))
	plt.show()

def scatter02():
	xvalues = list(range(1,100))
	yvalues = [x**2 for x in xvalues]
	plt_set_param("散点图——平方值", "value", "Square of value")
	plt.scatter(xvalues, yvalues, c=yvalues, cmap=plt.cm.Blues)
	# plt.show()
	plt.savefig("plt01_scatter02.png", bbox_inches="tight")

def scatter03():
	xvalues = list(range(1,100))
	yvalues = [x**2 for x in xvalues]
	plt_set_param("散点图——平方值", "value", "Square of value")
	plt.scatter(xvalues, yvalues, c=yvalues, cmap=plt.cm.Blues)
	plt.grid(True)	# 显示网格
	plt.savefig("plt01_scatter03.png", bbox_inches="tight")


# 直方图
def bar01():
	xvalues = list(range(1,12))
	yvalues = [x**2 for x in xvalues]
	plt_set_param("平方值", "value", "Square of value")
	plt.bar(xvalues, yvalues)
	plt.grid(True)
	plt.xticks(xvalues)  # 修改x轴的刻度
	plt.savefig("plt01_bar01.png", bbox_inches="tight")

import numpy as np

def bar02():
	index = np.arange(5)
	print(index)
	xl01 = list(range(1,6))  # 只能用于计算，不能用于多数据的x轴显示
	yl01 = [x**2 for x in xl01]
	yl02 = [2,20,12,6,40]
	plt_set_param("平方值", "value", "Square of value")
	bar_width = 0.35
	plt.bar(index, yl01, bar_width, color='b')
	plt.bar(index+bar_width, yl02, bar_width, color='r')
	plt.grid(True)
	plt.xticks(index+bar_width, ['one','two','three','four','five'])  # 修改x轴的刻度,及显示文字
	plt.savefig("plt01_bar02.png", bbox_inches="tight")

if __name__ == '__main__':
	# plot01()
	# plot02()	
	# plot03()
	# scatter01()		
	# scatter02()	
	# scatter03()	
	# bar01()	
	bar02()