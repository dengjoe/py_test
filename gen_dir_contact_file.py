#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 
生成符合ffmpeg contact demux的file.txt文件，用于合并mp3等媒体文件
"""

__author__ = 'Kevin deng'


import os


def gen_file_txt(dir, foutname):  
	fids = os.walk(dir)  
	with open(foutname, "w") as f:			
		for rootDir, pathList, fileList in fids:  
			for file in fileList:  
				fname = "file '" + os.path.join(rootDir, file) + "'\n"
				f.write(fname)


if __name__ ==  '__main__':
	gen_file_txt("G:\_多媒体\音乐-歌曲\CD_mp3", "G:\_多媒体\音乐-歌曲\CD_mp3\\file.txt")
	