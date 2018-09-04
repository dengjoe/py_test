#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a pandas test demo'

__author__ = 'kevin deng'


import pandas as pd
import numpy as np 


def df_print_info(df):
	# 查看列的数据类型
	print("dtypes:\n", df.dtypes) 

	# 查看行键、列键、值列表
	print("index:", df.index)  	    # 获取行键列表
	print("columns:", df.columns) 	# 获取列键列表
	print("values:\n", df.values)	# 获取值列表，是个list，相当于二维数组

	# 查看快速统计汇总: 和、平均值、最大、最小等
	print("describe():\n", df.describe())

	# 行或列的均值
	print("mean():\n", df.mean())  # 列, 等同0
	print("mean(1):\n", df.mean(1)) # 行


# create a dataframe and save to a csv file
def df_save_easy01(fname):
	dates = pd.date_range('20130101', periods=6)
	print("dates:\n", dates)

	df = pd.DataFrame(np.random.randn(6,4), index=dates, columns=list('ABCD'))
	print("df:\n", df)
	df.to_csv(fname)

# read a dataframe from a csv file
def df_read_easy01(fname):
	df = pd.read_csv(fname, encoding='utf-8', header=0, index_col=None)
	df_print_info(df)


def df_dicts():
	print("===== df_dicts: =====")
	dict0 =  {'score':  [ 8.9, 8.2, 9.3 ],
	        'category': ['悬疑', '动作', '爱情']
	    }
	df = pd.DataFrame(dict0)	
	print(df)
	print(df['score']) # 选择列
	print("\ndf.loc[[0, 2]]:\n", df.loc[[0, 2]]) # 选择行
	print(df.loc[[0, 1], ['category'] ]) # 选择行列

	# change index and columes
	df.index = ['movie_1', 'movie_2', 'movie_3']
	df.columns = ['种类', '分数']
	print("\n", df)
	print(df['分数']) # 选择列
	print(df.loc[['movie_1', 'movie_3']]) # 选择行

# create by list
d01=pd.DataFrame([["Joe","Kelly"],[234,456],[12,34]],index=["a","b","c"], columns=[3,5])
print(d01)

# create by dict
d02=pd.DataFrame({"name":["Joe","Kelly"], "value":[12,34]},index=["a","b"])
print(d02)

if __name__=='__main__':
	fname0 = "./easy01.csv"
	# df_easy01(fname0);	
	# df_read_easy01(fname0)
	df_dicts()