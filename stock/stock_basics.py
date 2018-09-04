#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a tushare module download stock basics, and download all csv datas from http://www.xueqiu.com/'

__author__ = 'kevin deng'

import os
import sys
import time
import urllib.request as urllib2
# python3已经没有了urllib2，仅有urllib，区别就在于urllib2相当于urllib.request，调用urllib2的方法时可以通过urllib.request调用。 
import tushare as ts
import pandas as pd
import socket
 
socket.setdefaulttimeout(20)  # 设置socket层的超时时间为20秒

# 下载A股基本面信息，保存到csv
def download_stock_basics(fname):
	df = ts.get_stock_basics()
	df.to_csv(fname)


# 下载url数据保存到本地文件
def download_url(url, local_fname):
	""" http get 下载文件 """
	
	# 检查本地文件是否存在，存在则返回
	if os.path.isfile(local_fname):
		return

	print(url)
	headers = {
	'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'
	}
	sleep_time = 5

	# 下载url文件，防止网站认为是攻击，并超时重试。
	while True:
		try:
			request = urllib2.Request(url, headers=headers)
			response = urllib2.urlopen(request, timeout = 10)
			# response = urllib.request.urlopen(url)
			# print(response)
			write_file_data(local_fname, response.read())
			response.close() 	# 没有进行request.close()操作，可能导致网站认定是攻击。
			break
		except urllib2.URLError as e:
			print("Error:", url, e)
			break
		except socket.timeout as e:  
			print("Error socket timout retry:\n",url)
			sleep_time += 5
			time.sleep(sleep_time)	
		except : 
			print("Error retry:") # 其他错误，如 [WinError 10054]
			sleep_time += 5
			time.sleep(sleep_time)	

	time.sleep(5)	# 下载后没有sleep几秒，会导致网站认定这种行为是攻击。 
	return

def write_file_data(filename, data):
	with open(filename, 'wb') as f:
		f.write(data)

# 取csv中股票代码，下载雪球网目录下的利润表、资产负债表、现金流量表
def download_stock_details(fname):
	df = pd.read_csv(fname, encoding='utf-8', dtype={'code': str}) # nrows=2
	# print("columns:", df.columns) 
	# print(df.loc[[1, 3, 8]])
	codes = df['code'].values
	# print(codes)

	for code in codes:
		if code[0] in ['5','6','9']: 
			scode = 'SH'+code	# ShangHai
		else:
			scode = 'SZ'+code	# ShenZhen

		url_fzb = "http://api.xueqiu.com/stock/f10/balsheet.csv?symbol=%s&page=1&size=10000" % scode
		url_lrb = "http://api.xueqiu.com/stock/f10/incstatement.csv?symbol=%s&page=1&size=10000" % scode
		url_llb = "http://api.xueqiu.com/stock/f10/cfstatement.csv?symbol=%s&page=1&size=10000" % scode
		download_url(url_fzb, ("data/%s_fzb.csv" % scode))
		download_url(url_lrb, ("data/%s_lrb.csv" % scode))
		download_url(url_llb, ("data/%s_llb.csv" % scode))







if __name__=='__main__':
	fname = 'data/all_basics.csv'
	# download_stock_basics(fname)
	download_stock_details(fname)
