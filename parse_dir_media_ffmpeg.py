#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a parse dir get media path to make ffmpeg bash file '

__author__ = 'kevin deng'


import re
import os
from shutil import copyfile

#pat = re.compile(r'([\w\s.]+?).(\d{4}).([\w]+)') #编译运行，提高效率

_media_type = (".wmv",".vob",".rm",".rmvb",".avi",".mpeg",".mpg",".mp4",".mkv",".dat")
_media_type_old = (".wmv",".vob",".rm",".rmvb",".avi",".mpeg",".mpg",".dat")

def write_media_trans(dir, smid, fmedia):  
    yid = os.walk(dir)  
    for rootDir, pathList, fileList in yid:  
        for file in fileList:  
            filepath = os.path.join(rootDir, file)

            # 生成输出文件名
            name_in = filepath.replace("\\", "/")
            name_out = name_in.replace("_mold/","_mold/new/");

            # 创建输出目录
            opath = os.path.dirname(name_out)
            if os.path.exists(opath) == False:
                print(opath)
                os.makedirs(opath)

            fext = os.path.splitext(file)
            if fext[1].lower() in _media_type:
                # 生成ffmpeg转码命令
                portion = os.path.splitext(name_out)
                if portion[1].lower() in _media_type_old: 
                    name_out = portion[0] + ".mp4" 
                mstr = "./ffmpeg -i \"" + name_in.replace("D:", "/d") + '\"' + smid + '\"' + name_out.replace("D:", "/d") + '\"\n'
                fmedia.write(mstr);
            else:
                # 直接拷贝文件到输出目录
                copyfile(name_in, name_out)


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
    # smid = " -map 0:0 -c:v libx264 -b:v 1800k -r 25 -s 1280x720 -map 0:1 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 -map 0:2 -c:s copy "
    # make_media_trans_sh("D:/data/_mold/BBC_720p", smid, "./bbc.sh")
    # smid = " -map 0:0 -c:v libx264 -b:v 2000k -r 25 -s 1440x810 -map 0:1 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 -map 0:2 -c:s copy "
    # make_media_trans_sh("D:/data/_mold/AE 大卫.爱登堡：生命溯源 - 2集", smid, "./ae.sh")
    # smid = " -c:v libx264 -b:v 1800k -r 25 -s 1280x720 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/AB 宇宙的奇迹 - 4集", smid, "./ab.sh")
    # smid = " -c:v libx264 -b:v 800k -r 25 -s 768x576 -c:a libfdk_aac -ab 128k -ac 2 -ar 44100 "
    # make_media_trans_sh("D:/data/_mold/汉字宫第四部", smid, "./汉字宫第四部.sh")
    # smid = " -c:v libx264 -b:v 2000k -r 25 -s 1280x720 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/故宫100", smid, "./故宫100.sh")
    # smid = " -c:v libx264 -b:v 800k -r 25 -s 640x352 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/BBC Power of ART", smid, "./art.sh")
    # smid = " -map 0:0 -c:v libx264 -b:v 1800k -r 25 -s 1280x720 -map 0:1 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 -map 0:2 -c:s copy "
    # make_media_trans_sh("D:/data/_mold/茶,一片树叶的故事.2013", smid, "./茶.sh")
    # smid = " -c:v libx264 -b:v 1200k -r 30 -s 1280x720 -c:a libfdk_aac -ab 128k -ac 2 -ar 44100 "
    # make_media_trans_sh("D:/data/_mold/14.Caities Classroom Live 12个凯蒂的教室主题视频（18年更新 12有字幕）", smid, "./Caities.sh")
    # smid = " -map 0:0 -c:v libx264 -b:v 1800k -r 25 -s 1280x720 -map 0:1 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 -map 0:2 -c:s copy "
    # make_media_trans_sh("D:/data/_mold/720p", smid, "./720p1.sh")
    # smid = " -map 0:0 -c:v libx264 -b:v 700k -r 24000/1001 -s 816x602 -map 0:1 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 -map 0:2 -c:s copy "
    # make_media_trans_sh("D:/data/_mold/草原上的小木屋.Little.House.On.The.Prairie.1974", smid, "./草原上.sh")
    # smid = " -c:v libx264 -b:v 350k -r 24000/1001 -s 512x384 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/法律与秩序", smid, "./法律与秩序.sh")
    # smid = " -c:v libx264 -b:v 750k -r 24 -s 852x478 -c:a libfdk_aac -ab 128k -ac 2 -ar 44100 "
    # make_media_trans_sh("D:/data/_mold/《学习的背叛》(全3集）", smid, "./学习.sh")
    # smid = " -map 0:0 -c:v libx264 -b:v 900k -r 24000/1001 -s 1280x720 -map 0:1 -c:a libfdk_aac -ab 128k -ac 2 -ar 44100 -map 0:2 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/丁丁历险记", smid, "./丁丁历险记.sh")

    # smid = " -c:v libx264 -b:v 800k -r 24 -s 1280x720 -c:a libfdk_aac -ab 128k -ac 2 -ar 44100 "
    # make_media_trans_sh("D:/data/_mold/song", smid, "./song.sh")
    # smid = " -c:v libx264 -b:v 800k -r 30000/1001 -s 1280x720 -c:a libfdk_aac -ab 128k -ac 2 -ar 44100 "
    # make_media_trans_sh("D:/data/_mold/01.Super Simple Songs 1-3共44个视频（25个有英文字幕）", smid, "./01.Super.sh")
    # smid = " -c:v libx264 -b:v 800k -r 30 -s 1280x720 -c:a libfdk_aac -ab 128k -ac 2 -ar 44100 "
    # make_media_trans_sh("D:/data/_mold/18.官网同步更新20个视频（20个有英文字幕）", smid, "./18.官网同步.sh")
    # smid = " -c:v libx264 -b:v 800k -r 24000/1001 -s 1024x576 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/瑞克与莫蒂.Rick and Morty", smid, "./rick.sh")
    # smid = " -c:v libx264 -b:v 800k -r 24000/1001 -s 1024x576 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/Breaking.Bad.绝命毒师", smid, "./bad.sh")
    # smid = " -c:v libx264 -b:v 800k -r 24000/1001 -s 1024x576 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/无耻家庭", smid, "./无耻家庭.sh")
    
    # smid = " -map 0:0 -c:v libx264 -b:v 800k -r 30000/1001 -s 640x352 -map 0:1 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 -map 0:2 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/640x352", smid, "./640x352.sh")
    # smid = " -c:v libx264 -b:v 800k -r 25 -s 656x368 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000  "
    # make_media_trans_sh("D:/data/_mold/The Human Body.人体漫游.1998（8集）", smid, "./body.sh")
    # smid = " -c:v libx264 -b:v 800k -r 25 -s 512x384 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000  "
    # make_media_trans_sh("D:/data/_mold/Trials of Life.生命的起点.1990（12集）", smid, "./Trials.sh")
    # smid = " -c:v libx264 -b:v 800k -r 25 -s 640x480 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/Life.on.earth.生命的进化.1979（13集）", smid, "./Lifeoe.sh")
    # smid = " -map 0:0 -c:v libx264 -b:v 800k -r 30000/1001 -s 624x336 -map 0:1 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 -map 0:2 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/The Human Mind.人类心智.2003（3集）", smid, "./mind.sh")
    # smid = " -map 0:0 -c:v libx264 -b:v 800k -r 30000/1001 -s 608x336 -map 0:1 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 -map 0:2 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/Human Senses.人类感官.2003（3集）", smid, "./sense.sh")
    # smid = " -c:v libx264 -b:v 1800k -r 25 -s 1280x720 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/BBC 药物如何运作（3集）", smid, "./medic.sh")
    # smid = " -c:v libx264 -b:v 1800k -r 24000/1001 -s 1280x720 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/720p", smid, "./720-1.sh")
    # smid = " -c:v libx264 -b:v 1100k -r 25 -s 1024x576 -c:a libfdk_aac -ab 128k -ac 2 -ar 44100 "
    # make_media_trans_sh("D:/data/_mold/AB 地球造人 5集  How.Earth.Made.Us", smid, "./地球造人.sh")
    # smid = " -map 0:0 -c:v libx264 -b:v 800k -r 24000/1001 -s 640x352 -map 0:1 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 -map 0:2 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/B 人脑漫游6集 （4.1G）Brain.story", smid, "./人脑漫游.sh")
    # smid = " -c:v libx264 -b:v 800k -r 25 -s 704x400 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/光的故事 Light.Fantastic.2004（4集）", smid, "./光的故事.sh")
    # smid = " -c:v libx264 -b:v 800k -r 25 -s 640x352 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/BBC Secrets.of.the.Sexes.两性奥秘.2005（3集）", smid, "./两性奥秘.sh")
    # smid = " -map 0:0 -c:v libx264 -b:v 800k -r 30000/1001 -s 592x320 -map 0:1 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 -map 0:2 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/The Human.Instinct.人类本能.2002（4集）", smid, "./人类本能.sh")
    # smid = " -map 0:0 -c:v libx264 -b:v 800k -r 25 -s 576x432 -map 0:1 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 -map 0:2 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/BBC Ape-Man.人类起源.2000（6集）", smid, "./人类起源.sh")
    # smid = " -map 0:0 -c:v libx264 -b:v 800k -r 30000/1001 -s 640x352 -map 0:1 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 -map 0:2 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/时间机器 Time.Machine.2004（3集）", smid, "./时间机器 .sh")
    # smid = " -map 0:0 -c:v libx264 -b:v 800k -r 30000/1001 -s 640x352 -map 0:1 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 -map 0:2 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/BBC How.To.Build.A.Human.制造新人类.2002（4集）", smid, "./新人类.sh")
    # smid = " -map 0:0 -c:v libx264 -b:v 800k -r 30000/1001 -s 576x432 -map 0:1 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 -map 0:2 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/BBC Phobias.恐惧症大家谈.2005（2集）", smid, "./恐惧症.sh")
    # smid = " -c:v libx264 -b:v 1800k -r 25 -s 1280x720 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/Lost Land of the Volcano.火山的遗失之地.2009（3集）", smid, "./火山的遗失之地.sh")
    # smid = " -map 0:0 -c:v libx264 -b:v 1800k -r 25 -s 1280x720 -map 0:1 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 -map 0:2 -c:s copy  "
    # make_media_trans_sh("D:/data/_mold/BBC The Hottest Place on Earth.世界上最热的地方.2009（2集）", smid, "./世界上最热.sh")
    # smid = " -map 0:0 -c:v libx264 -b:v 800k -r 24000/1001 -s 640x352 -map 0:1 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 -map 0:2 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/BBC Wild.Weather.天有风云.2002（4集）", smid, "./天有风云.sh")
    # smid = " -c:v libx264 -b:v 800k -r 30000/1001 -s 512x384 -c:a libfdk_aac -ab 128k -ac 2 -ar 44100 "
    # make_media_trans_sh("D:/data/_mold/BBC The Private Life of Plants.植物私生活.1995（6集）", smid, "./植物私生活.sh")
    # smid = " -map 0:0 -c:v libx264 -b:v 800k -r 30000/1001 -s 512x384 -map 0:1 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 -map 0:2 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/BBC Earth Story.地球形成的故事.1998（8集）", smid, "./地球形成.sh")
    # smid = " -c:v libx264 -b:v 800k -r 25 -s 592x320 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/BBC State of the Planet.大地的声音.2000（3集）", smid, "./大地.sh")
    # smid = " -map 0:0 -c:v libx264 -b:v 800k -r 24000/1001 -s 640x352 -map 0:1 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 -map 0:2 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/BBC 蓝色星球1.2001", smid, "./蓝色星球1.sh")
    
    # smid = " -c:v libx264 -b:v 800k -r 25 -s 1280x720 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/01. 字母积木.Alphablocks全4季91集", smid, "./Alphablocks.sh")
    # smid = " -c:v libx264 -b:v 800k -r 29.93 -s 720x480 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/02. Kids ABC", smid, "./Kids ABC.sh")
    # smid = " -c:v libx264 -b:v 600k -r 25 -s 720x480 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/03. 迪斯尼美语世界", smid, "./迪斯尼美语.sh")
    # smid = " -c:v libx264 -b:v 800k -r 30000/1001 -s 720x480 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/04. 迪斯尼Zippy and Me", smid, "./zippy.sh")
    # smid = " -c:v libx264 -b:v 800k -r 25 -s 1280x720 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/巴迪", smid, "./巴迪.sh")
    # smid = " -c:v libx264 -b:v 800k -r 24000/1001 -s 640x352 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/B Supervolcano.超级火山 2集", smid, "./超级火山.sh")
    # smid = " -c:v libx264 -b:v 800k -r 30000/1001 -s 608x336 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/B 末日火山.BBC.Krakatoa.The.Last.Days", smid, "./末日火山.sh")
    # smid = " -c:v libx264 -b:v 350k -r 30000/1001 -s 352x240 -c:a libfdk_aac -ab 128k -ac 2 -ar 44100 "
    # make_media_trans_sh("D:/data/_mold/11. Sight word kids", smid, "./swk.sh")
    # smid = " -c:v libx264 -b:v 700k -r 25 -s 704x576 -c:a libfdk_aac -ab 128k -ac 2 -ar 44100 "
    # make_media_trans_sh("D:/data/_mold/09. 时代美语English_Time", smid, "./English_Time.sh")
    # smid = " -c:v libx264 -b:v 750k -r 25 -s 640x480 -c:a libfdk_aac -ab 128k -ac 2 -ar 48000 "
    # make_media_trans_sh("D:/data/_mold/13. 天才宝贝熊", smid, "./天才宝贝熊.sh")
    smid = " -c:v libx264 -b:v 500k -r 30000/1001 -s 512x384 -c:a libfdk_aac -ab 128k -ac 2 -ar 44100 "
    make_media_trans_sh("D:/data/_mold/07. 小爱因斯坦 Little Einsteins", smid, "./小爱因斯坦.sh")

    # smid = "  "
    # make_media_trans_sh("D:/data/_mold/", smid, "./.sh")


    # scut = "-ss 00:00:00 -t 00:05:00"
    # make_media_cuts_sh("D:/data/_mold/中文版1~5季 720P", scut, "./peiqi_cuts.sh")
    # scut = "-ss 00:00:20 -t 00:05:10"
    # make_media_cuts_sh("D:/data/_mold/故宫100", scut, "./100_cuts.sh")
    # scut = "-ss 00:00:30 -t 01:00:00"
    # make_media_cuts_sh("D:/data/_mold/魔法觉醒", scut, "./cut魔法觉醒.sh")
    # scut = "-ss 00:00:30 -t 01:00:00"
    # make_media_cuts_sh("D:/data/_mold/好兆头.Good.Omens.2019", scut, "./cut好兆头.sh")

    # scut = "-ss 00:00:00 -t 00:05:00"
    # make_media_cuts_sh("D:/data/_mold/", scut, "./.sh")
