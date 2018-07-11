#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a parse dir change file name with ", The -" or ", A - " to head. '

__author__ = 'kevin deng'


import re
import os

_file_type = (".mobi",".epub")
_sreplace = " - " #替换字符串


def is_find_file_pat(filename, pats):
	i = 0
	for tstr in pats:
		if filename.find(tstr) >= 0:
			return i
		else:
			i += 1
			continue
	return -1

def new_file_name(filename, pat):
	aname = filename.replace(pat, _sreplace)
	head = pat[2:pat.find("-")]
	return head+aname

def parse_fnames(dir, pats, flog):  
    yid = os.walk(dir)  
    for rootDir, pathList, fileList in yid:  
        for file in fileList:  
            filepath = os.path.join(rootDir, file)

            fext = os.path.splitext(file)
            if fext[1] in _file_type:
	            # renam pats file name, if has same file, rm it . 
	            n = is_find_file_pat(file, pats)
	            if n>=0:
	            	# rename
	            	new_name = new_file_name(file, pats[n])
	            	new_path = os.path.join(rootDir, new_name)

	            	flog.write(file + "\t=>\t" + new_name + '\n')
	            	print(file + "\t=>\t" + new_name)

	            	if os.path.isfile(new_path):
	            		os.remove(new_path)
	            	os.rename(filepath, new_path)


def  parse_dir(dir):
	try:
		flog = open(dir+"/finds_info.txt", 'w')
		sfinds = (", The - ", ", A - ", ", An - ")
		parse_fnames(dir, sfinds, flog)
	finally:
		if flog:
			flog.close()


if __name__=='__main__':
    parse_dir("F:/迅雷下载/English/7700mobi/7700.Mobi.All.Ebooks")