#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 
对下载的新浪博客html文件进行遍历，生成索引html文件
path_root 根目录可以生成目录html
 |-images 存放图片
 |-text   存放博文html
"""

__author__ = 'Kevin deng'


from bs4 import BeautifulSoup
import datetime
import time
import os


def list_path_files(dir):  
	fids = os.walk(dir)  
	for rootDir, pathList, fileList in fids:  
		for file in fileList:  
			fname = os.path.join(rootDir, file)
			pass


if __name__=='__main__':
	# list_path_files()
	pass