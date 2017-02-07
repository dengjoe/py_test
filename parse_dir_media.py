#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a parse dir get media info module '

__author__ = 'kevin deng'


import re
import os


#pat = re.compile(r'([\w\s.]+?).(\d{4}).([\w]+)') #编译运行，提高效率

_media_type = (".wmv",".rm",".rmvb",".avi",".mpeg",".mpg",".mp4",".mkv")

def parse_media(dir, media_pat, fmedia, ferror):  
    yid = os.walk(dir)  
    for rootDir, pathList, fileList in yid:  
        for file in fileList:  
            filepath = os.path.join(rootDir, file)

            fext = os.path.splitext(file)
            if fext[1] in _media_type:
	            # regex to media name, year, chinese name. 
	            m = media_pat.match(file)
	            if m:
	            	mstr = m.group(1) + '\t' + m.group(2) + '\t' + m.group(3) + '\t' + filepath + '\n'
	            	fmedia.write(mstr);
	            	# print(m.groups())
	            else:
	            	mstr = filepath + "\n"
	            	ferror.write(mstr)
            else:
	            print(filepath)



def  parse_dir(dir):
	try:
		fmedia = open("./media_info.txt", 'w')
		ferror = open("./media_err.txt", 'w')
		pat = re.compile(r'([\w\s.\'\-]+?).(\d{4}).([\w\(\)\-：]+)')

		parse_media(dir, pat, fmedia, ferror)
	finally:
		if fmedia:
			fmedia.close()
		if ferror:
			ferror.close()


if __name__=='__main__':
    parse_dir("F:/movies")