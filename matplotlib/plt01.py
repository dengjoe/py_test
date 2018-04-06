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
	plt.plot(input_values, squares)
	plt_set_param("Square Numbers", "value", "Square of value")
	plt.savefig("p01.png")
	# plt.show()

# 散点图
def scatter01():
	input_values = [1,2,3,4,5]
	plt.scatter(input_values, squares, c=(0,0,0.8))
	plt_set_param("Square Numbers", "value", "Square of value")
	plt.show()

def scatter02():
	xvalues = list(range(1,1000))
	yvalues = [x**2 for x in xvalues]
	plt.scatter(xvalues, yvalues, c=yvalues, cmap=plt.cm.Blues)
	plt_set_param("平方值", "value", "Square of value")
	# plt.show()
	plt.savefig("p02.png", bbox_inches="tight")

def scatter03():
	xvalues = list(range(1,1000))
	yvalues = [x**2 for x in xvalues]
	plt.scatter(xvalues, yvalues, c=yvalues, cmap=plt.cm.Blues)
	plt_set_param("平方值", "value", "Square of value")
	plt.grid(True)
	plt.savefig("p03.png", bbox_inches="tight")

# 直方图
def bar01():
	xvalues = list(range(1,12))
	yvalues = [x**2 for x in xvalues]
	plt.bar(xvalues, yvalues)
	plt_set_param("平方值", "value", "Square of value")
	plt.grid(True)
	plt.xticks(xvalues)  # 修改x轴的刻度
	plt.savefig("p04.png", bbox_inches="tight")

def bar02():
	xvalues = list(range(1,6))
	yvalues = [x**2 for x in xvalues]
	plt.bar(xvalues, yvalues)
	plt_set_param("平方值", "value", "Square of value")
	plt.grid(True)
	plt.xticks(xvalues, ['one','two','three','four','five'])  # 修改x轴的刻度,及显示文字
	plt.savefig("p05.png", bbox_inches="tight")

if __name__ == '__main__':
	# plot01()
	# plot02()	
	# scatter01()		
	# scatter02()	
	# scatter03()	
	# bar01()	
	bar02()