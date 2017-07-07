#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
生成srt字幕文件的脚本。
默认设置是：一行文本对应一行字幕，字幕时间间隔一致。
根据需要的开始时间和字幕时长、字幕条数，生成srt文件的内容如下：

1
09:20:00,000 --> 09:22:00,000
字幕显示了

2
09:22:00,000 --> 09:24:00,000
是什么内容呢？

'''

__author__ = 'Kevin deng'

import time
import sys


#时间戳timestamp(float)与字符串间的转换
def timestamp2str(timestamp):
	time_array = time.localtime(timestamp)
	return time.strftime("%Y-%m-%d %H:%M:%S", time_array)

def timestamp2str_date(timestamp):
	time_array = time.localtime(timestamp)
	return time.strftime("%Y-%m-%d", time_array)

def timestamp2str_time(timestamp):
	time_array = time.localtime(timestamp)
	return time.strftime("%H:%M:%S,000", time_array)

def str2timestamp(strtime):
	time_array = time.strptime(strtime, "%Y-%m-%d %H:%M:%S")
	return time.mktime(time_array)


def caculate_srt(foutname, time_begin, duration, number, finname=None):
	dtime = duration/number
	lines = []

	if finname:
		with open(finname, 'r') as f:
			lines = f.readlines()
			                    
	with open(foutname, "w") as f:
		for i in range(number):
			f.write("%d\n" % (i+1))
			tm_begin = time_begin + dtime*i
			tm_end   = tm_begin + dtime
			f.write("%s --> %s\n" % (timestamp2str_time(tm_begin), timestamp2str_time(tm_end)))
			if len(lines)>i:
				f.write(lines[i])
			else:
				f.write("\n")

			f.write("\n")


def test_make_srt():
	strbegin = timestamp2str_date(time.time()) + " " + "23:23:00"
	print(strbegin)
	begin_time = str2timestamp(strbegin)
	caculate_srt("./my.srt", begin_time, 120.6, 10)	
	# caculate_srt("./my.srt", begin_time, 120.6, 11, "./gensrt_in.txt")	


if __name__ == '__main__':
	if len(sys.argv) < 5:
		print("Usage: %s begin_time(xx:xx:xx) duration(s) number out_srtname [in_txtname]"  % sys.argv[0])
		sys.exit(5)

	strbegin = timestamp2str_date(time.time()) + " " + sys.argv[1]
	begin_time = str2timestamp(strbegin)

	inputname = None
	if len(sys.argv) == 6:
		inputname = sys.argv[5]

	caculate_srt(sys.argv[4], begin_time, float(sys.argv[2]), int(sys.argv[3]), inputname)

	# test_make_srt()
