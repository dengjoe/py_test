#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
	matplotlib test
"""

import matplotlib.pyplot as plt
import numpy as np
from pylab import mpl 

# 设置中文显示
mpl.rcParams['font.sans-serif'] = ['SimHei'] 
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
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


# 显示图例
def test_legend():
	x = np.arange(1, 11)

	l1, = plt.plot(x, x*x, 'r')  # 注意，必须要逗号，否则不显示
	l2, = plt.plot(x, x*x*x, 'b')  
	# loc表示位置的；
	plt.legend([l1, l2], ['first', 'second'], loc = 'upper left') 
	plt.grid(True)
	plt.show()

def test_multi_plot():
	t = np.arange(0., 5., 0.2)

	# red dashes, blue squares and green triangles
	# plt.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
	l1, = plt.plot(t, t, 'r--')
	l2, = plt.plot(t, t**2, 'bs')
	p1 = plt.legend(handles=[l1, l2], labels = ['a', 'b'], loc = 'upper left')

	l3, = plt.plot( t, t**3, 'g^')
	plt.legend(handles=[l3], labels = ['c'], loc = 'lower right')

	plt.gca().add_artist(p1)  # 这里很重要，否则p1不显示
	plt.show()

def test_multi_2():
	x = np.random.uniform(-1, 1, 4)
	y = np.random.uniform(-1, 1, 4)
	p1, = plt.plot([1,2,3])
	p2, = plt.plot([3,2,1])
	l1 = plt.legend([p2, p1], ["line 2", "line 1"], loc='upper left')
	 
	p3 = plt.scatter(x[0:2], y[0:2], marker = 'D', color='r')
	p4 = plt.scatter(x[2:], y[2:], marker = 'D', color='g')
	# This removes l1 from the axes.
	plt.legend([p3, p4], ['label', 'label1'], loc='lower right', scatterpoints=1)

	# Add l1 as a separate artist to the axes
	plt.gca().add_artist(l1)
	plt.show()


if __name__ == '__main__':
	# plot01()
	# plot02()	
	# plot03()
	# scatter01()		
	# scatter02()	
	# scatter03()	
	# bar01()	
	# bar02()
	# test_legend()
	test_multi_plot()
	test_multi_2()