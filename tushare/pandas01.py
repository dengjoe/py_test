#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd   
import numpy as np 
import matplotlib.pyplot as plt

# Series
def Series_demo1():
	s1 = pd.Series([1,3,5,np.nan,6,8])
	print(s1)

	s2 = pd.Series(data=[1,2,3,4,2],index = ['a','b','c','d','e'])
	print(s2)
	print(s2.index)  	# 获取键列表
	print(s2.values)	# 获取值列表

	print(s2.value_counts()) # 直方图函数


# DataFrame
def df_demo1():
	# 以能够被转换成类似序列结构的字典对象来初始化
	df1 = pd.DataFrame({ 'A' : 1.,
	                     'B' : pd.Timestamp('20130102'),
	                     'C' : pd.Series(1,index=list(range(4)),dtype='float32'),   #生成Series对象,取的是value
	                     'D' : np.array([3] * 4,dtype='int32'),  					#生成numpy对象
	                     'E' : pd.Categorical(["test","train","test","train"]),
	                     'F' : 'foo' })  
	print("\n---------------")
	print(df1)
	# 查看列的数据类型
	print(df1.dtypes) 

	# 循环查看数据
	for index,row in df1.iterrows():
		print('行索引:',index)
		print('行数据:',row)



# 查看df的数据，包括提取部分数据
def df_datas():
	print("\n----------df_datas:----------")

	# 以numpy array来初始化数据，并给出行列的名
	dates = pd.date_range('20130101', periods=6)
	print("dates:\n", dates)

	df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
	print("df:\n", df)

	# 查看列的数据类型
	print("dtypes:\n", df.dtypes) 

	# 查看行键、列键、值列表
	print("index:", df.index)  	# 获取行键列表
	print("columns:", df.columns) 	# 获取列键列表
	print("values:\n", df.values)	# 获取值列表

	# 查看快速统计汇总: 和、平均值、最大、最小等
	print("describe():\n", df.describe())

	# 行或列的均值
	print("mean():\n", df.mean())  # 列, 等同0
	print("mean(1):\n", df.mean(1)) # 行


	### 提取数据 ###
	
	print("A:")
	print(df['A'])

	# []切片
	print("[0:3]:")
	print(df[0:3])

	print("[\"20130102\":\"20130104\"]:")
	print(df["20130102":"20130104"])

	# loc 按标签
	print("loc[]:")
	print(df.loc['20130101'])
	print("")
	print(df.loc[:,['A','B']]) # 多个轴
	print("")
	print(df.loc["20130103":"20130104",['A','B']]) # 多个轴+切片
	print("")
	print(df.loc["20130104",['A','B']]) # 多个轴+定值index

	# at 快速访问，同loc
	print("at[]:")
	print(df.loc['20130101','A'])
	# print(df.at['20130101','A']) # error？：KeyError: '20130101'

	# iloc 按位置
	print("iloc[]:")
	print(df.iloc[3]) # 按行
	print("")
	print(df.iloc[3:5, 0:2]) # 行范围(3:5]
	print("")
	print(df.iloc[[1,2,4], [0,3]])

	print(df.iloc[1,3])
	# iat
	print(df.iat[1,3])  

	# 取头尾数据
	print("head():\n", df.head())   # 默认5
	print("tail(2):\n", df.tail(2))
	              
	# 条件选择
	print("条件选择:")
	print("df.A>0")
	print(df[df.A>0]) 
	print("df>0")
	print(df[df>0]) 

	# isin()
	df['E'] = ['one', 'one','two','three','four','three'] # 添加一列
	print(df)
	print(df[df['E'].isin(['two','four'])])


# 数据操作
def df_operate():
	print("\n---------df_operate:-----------")

	df = pd.DataFrame(np.random.randn(5, 4), columns=['A','B','C','D'])
	print(df)

	# 行列转置
	print(df.T)

	# 排序
	print("sort_index(axis=1, ascending=False):")
	print(df.sort_index(axis=1, ascending=False)) 	# 根据轴排序，只有0,1
	print("sort_values(by=\'B\'):")
	print(df.sort_values(by='B')) 		# 根据列的值排序

	# concat()
	# pieces = [df[1:3], df[5:]]
	# print(pieces)
	# pd.concat(pieces)
	# print(df)

	# merge()
	df1 = pd.DataFrame({"key":["day","day"], "val0":[23,2]}) # key 相同
	df2 = pd.DataFrame({"key":["day","day"], "sal":[34,20]})
	df3 = pd.merge(df1,df2, on="key")
	print(df3)

	df1 = pd.DataFrame({"key":["day","month"], "val0":[23,2]}) # key都不同
	df2 = pd.DataFrame({"key":["day","month"], "sal":[34,20]})
	df3 = pd.merge(df1,df2, on="key")
	print(df3)

	# append()
	print("append():")
	s = df3.iloc[1]
	df3.append(s, ignore_index=True)
	print(df3)

if __name__ == '__main__':
	Series_demo1()

	# df_demo1()
	# df_datas()
	df_operate()
