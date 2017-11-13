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

def read_txt_file(filename):
	with open(filename, 'r', encoding='utf8') as f:
		return f.read()

def write_txt_file(filename, content):
	with open(filename, 'w', encoding='utf8') as f:
		return f.write(content)


def change_text_style(fname):
	html = read_txt_file(fname)
	bsobj = BeautifulSoup(html, "lxml")
	style = bsobj.find("style")
	# print(style.string)

	style.string = " body{font-size:20px;font-weight:bold;background-color:#E1E6E0} "

	p = bsobj.find("p")
	if p:
		strfont = "<font color=\"#005356\">"
		font_line = BeautifulSoup(strfont, "lxml")
		p.insert_before(font_line.font)
		font = bsobj.find("font")
		ps = bsobj.find_all("p")
		for para in ps:
			font.append(para)

	write_txt_file(fname, str(bsobj))


def list_path_files(dir):  
	fids = os.walk(dir)  
	for rootDir, pathList, fileList in fids:  
		for file in fileList:  
			fname = os.path.join(rootDir, file)
			# change_text_style(fname)



if __name__=='__main__':
	list_path_files("C:/test/python_code/py_test/bs4/清一博客/text")
	# change_text_style("C:/test/python_code/py_test/bs4/清一博客/text/2007-1106_122119.html")
	pass