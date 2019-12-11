#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a parse dir get media path to make ffmpeg bash file '

__author__ = 'kevin deng'


import re
import os


#pat = re.compile(r'([\w\s.]+?).(\d{4}).([\w]+)') #编译运行，提高效率

_media_type = (".wmv",".rm",".rmvb",".avi",".mpeg",".mpg",".mp4",".mkv")

def write_media_trans(dir, smid, fmedia):  
    yid = os.walk(dir)  
    for rootDir, pathList, fileList in yid:  
        for file in fileList:  
            filepath = os.path.join(rootDir, file)

            fext = os.path.splitext(file)
            if fext[1] in _media_type:
                name_in = filepath.replace("\\", "/")
                name_out = name_in.replace("_mold/","_mold/new/");

                opath = os.path.dirname(name_out)
                if os.path.exists(opath) == False:
                    print(opath)
                    os.makedirs(opath)

                mstr = "./ffmpeg -i \"" + name_in.replace("D:", "/d") + '\"' + smid + '\"' + name_out.replace("D:", "/d") + '\"\n'
                fmedia.write(mstr);

# smid:音视频编码参数
def make_media_trans_sh(dir, smid, fname):
    try:
        fmedia = open(fname, 'w')
        write_media_trans(dir, smid, fmedia)
    finally:
        if fmedia:
            fmedia.close()


def write_media_cuts(dir, scut, fmedia):  
    yid = os.walk(dir)  
    for rootDir, pathList, fileList in yid:  
        for file in fileList:  
            filepath = os.path.join(rootDir, file)

            fext = os.path.splitext(file)
            if fext[1] in _media_type:
                name_in = filepath.replace("\\", "/")
                name_out = name_in.replace("_mold/","_mold/new/");

                opath = os.path.dirname(name_out)
                if os.path.exists(opath) == False:
                    print(opath)
                    os.makedirs(opath)

                mstr = "./ffmpeg " + scut + " -accurate_seek -i \"" + name_in.replace("D:", "/d") + '\" -codec copy \"' + name_out.replace("D:", "/d") + '\"\n'
                fmedia.write(mstr);

 # scut 切割开始时间和切割时长，如从头开始的5分钟： "-ss 00:00:00 -t 00:05:00"
def make_media_cuts_sh(dir, scut, fname):
    try:
        fmedia = open(fname, 'w')
        write_media_cuts(dir, scut, fmedia)
    finally:
        if fmedia:
            fmedia.close()

# 生成的文件因为utf8，不能直接作为linux sh使用，需要复制到sh脚本中。
if __name__=='__main__':
    # smid = " -c:v libx264 -b:v 800k -r 25 -s 1280x720 -c:a libfdk_aac -ab 128k -ac 2 -ar 44100 "
    # make_media_trans_sh("D:/data/_mold/英文版1~5季 1080P", smid, "./peiqi.sh")
    # smid = " -map 0:0 -c:v libx264 -b:v 500k -r 25 -s 600x336 -map 0:1 -c:a libfdk_aac -ab 128k -ac 2 -ar 44100 "
    # make_media_trans_sh("D:/data/_mold/英文版1~5季 1080P/第4季52集", smid, "./peiqi4.sh")
    # smid = " -map 0:0 -c:v libx264 -b:v 800k -r 25 -s 1280x720 -map 0:1 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/英文版1~5季 1080P/第5季20集", smid, "./peiqi5.sh")
    # smid = " -c:v libx264 -b:v 800k -r 25 -s 1280x720 -c:a libfdk_aac -ab 128k -ac 2 -ar 44100 "
    # make_media_trans_sh("D:/data/_mold/中文版1~5季 720P", smid, "./peiqi_cn.sh")
    scut = "-ss 00:00:00 -t 00:05:00"
    make_media_cuts_sh("D:/data/_mold/中文版1~5季 720P", scut, "./peiqi_cuts.sh")

