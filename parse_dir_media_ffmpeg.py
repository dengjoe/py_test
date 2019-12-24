#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a parse dir get media path to make ffmpeg bash file '

__author__ = 'kevin deng'


import re
import os


#pat = re.compile(r'([\w\s.]+?).(\d{4}).([\w]+)') #编译运行，提高效率

_media_type = (".wmv",".vob",".rm",".rmvb",".avi",".mpeg",".mpg",".mp4",".mkv")
_media_type_old = (".wmv",".vob",".rm",".rmvb",".avi",".mpeg",".mpg")

def write_media_trans(dir, smid, fmedia):  
    yid = os.walk(dir)  
    for rootDir, pathList, fileList in yid:  
        for file in fileList:  
            filepath = os.path.join(rootDir, file)

            fext = os.path.splitext(file)
            if fext[1].lower() in _media_type:
                name_in = filepath.replace("\\", "/")
                name_out = name_in.replace("_mold/","_mold/new/");

                opath = os.path.dirname(name_out)
                if os.path.exists(opath) == False:
                    print(opath)
                    os.makedirs(opath)

                portion = os.path.splitext(name_out)
                if portion[1].lower() in _media_type_old: 
                    name_out = portion[0] + ".mp4" 
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
            if fext[1].lower() in _media_type:
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
    # smid = " -c:v libx264 -b:v 600k -r 25 -s 720x576 -c:a libfdk_aac -ab 128k -ac 2 -ar 44100 "
    # make_media_trans_sh("D:/data/_mold/基础级7个/1.Word World 单词世界", smid, "./1word.sh")
    # smid = " -c:v libx264 -b:v 600k -r 25 -s 704x478 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/基础级7个/2.Super Why阅读魔法", smid, "./2why.sh")
    # smid = " -c:v libx264 -b:v 500k -r 24000/1001 -s 512x384 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/2.神奇校车Magic School Bus", smid, "./magic1.sh")
    # smid = " -c:v libx264 -b:v 700k -r 24000/1001 -s 800x448 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/2.神奇校车02", smid, "./magic2.sh")
    # smid = " -c:v libx264 -b:v 1800k -r 24000/1001 -s 1280x720 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/7.Discovery史上100个伟大发现", smid, "./discovery.sh")
    # smid = " -c:v libx264 -b:v 600k -r 25 -s 720x576 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/入门级5-9/巴迪英文歌谣vob高清（推荐）", smid, "./巴迪英文歌谣.sh")
    # smid = " -c:v libx264 -b:v 800k -r 25 -s 720x480 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/入门级1-4/4.经典英文童谣+Wee+Sing（唱歌啦）", smid, "./wee.sh")
    # smid = " -c:v libx264 -b:v 500k -r 24/1001 -s 640x360 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/基础级7个/2.Super Why2", smid, "./super2.sh")
    smid = " -map 0:0 -c:v libx264 -b:v 1800k -r 25 -s 1280x720 -map 0:1 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 -map 0:2 -c:s copy "
    make_media_trans_sh("D:/data/_mold/BBC_720p", smid, "./bbc.sh")
    smid = " -map 0:0 -c:v libx264 -b:v 2000k -r 25 -s 1440x810 -map 0:1 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 -map 0:2 -c:s copy "
    make_media_trans_sh("D:/data/_mold/AE 大卫.爱登堡：生命溯源 - 2集", smid, "./ae.sh")
    smid = " -c:v libx264 -b:v 1800k -r 25 -s 1280x720 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    make_media_trans_sh("D:/data/_mold/AB 宇宙的奇迹 - 4集", smid, "./ab.sh")
    smid = " -c:v libx264 -b:v 800k -r 25 -s 768x576 -c:a libfdk_aac -ab 128k -ac 2 -ar 44100 "
    make_media_trans_sh("D:/data/_mold/汉字宫第四部", smid, "./汉字宫第四部.sh")

    # scut = "-ss 00:00:00 -t 00:05:00"
    # make_media_cuts_sh("D:/data/_mold/中文版1~5季 720P", scut, "./peiqi_cuts.sh")

