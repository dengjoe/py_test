#! python3
# -*- coding: utf-8 -*-

''' 
下载hls的ts文件，测试下载速度并记录日志到当前目录 
其计时函数只能在windows下正常运行，linux下会计时不准确
'''

__author__ = 'Kevin deng'

import os
import sys
import urllib.request
import time
import datetime


def parse_m3u8(data):
	""" 解析并返回m3u8的ts列表 """
	uris = []
	if len(data)<1:
		return uris

	for name in data.split("\n"):
		# if name.find(".ts") != -1:
		if name[-3:]==".ts" :
			uris.append(name.strip())
	return uris

def parse_m3u8_file(fname):
	with open(fname, "r") as f:
		uris = parse_m3u8(f.read())
		print(uris)


def get_url_data(url):
	""" http get 下载文件 """
	try:
		response = urllib.request.urlopen(url)
		return response.read()
	except urllib.error.URLError as e:
		print("Error:", url, e)
		return None

def write_file_data(filename, data):
	with open(filename, 'wb') as f:
		f.write(data)


def download_m3u8(url, outpath=".", log=None):
	urlpath = os.path.dirname(url)
	uris = []
	last_uri = ""

	if log:
		with open(log, "w") as fp:
			while True:
				data = get_url_data(url)
				if data:
					uris = parse_m3u8(data.decode())

				if len(uris)>0:
					for uri in uris:
						if uri > last_uri:
							cl0 = time.clock()
							data = get_url_data(urlpath+"/"+uri)
							cl1 = time.clock()
							speed = len(data)/(1024*1024*(cl1-cl0))
							content = "%s len=%d time=%f(s) speed=%.03f(M bytes/s)" % (uri, len(data), cl1-cl0, speed)
							print(content)
							fp.write(content+"\n")
							fp.flush()
							last_uri = uri

							if data == None:
								print("%s get None", uri)
								continue
							# write_file_data(outpath + "/" + uri, data)

	return 



# parse_m3u8_file("d:\\21.m3u8")

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("Usage: %s m3u8_url"  % sys.argv[0])
		sys.exit(2)

	now = datetime.datetime.now()
	logname = "./hls_down-%s.log" % now.strftime("%Y-%m-%d_%H.%M.%S")
	print(logname)
	download_m3u8(sys.argv[1], log=logname)
