#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
测试广西发流的脚本。完成以下工作：
1、修改config.xml其中的<Down><Url>内容为测试url
2、发出wget命令通知vss推流设备：
wget "http://192.168.10.12:9876/vss?programid=1&event=1&channelid=1&delay1=5&delay2=25"
3、启动dispatcher
4、等待此轮dispatcher播放完毕后，再过几分钟，杀死dispatcher
5、修改config.xml的Url为后续m3u8地址
6、重启dispatcher
前提是配置好config.xml,启动vss推流和ffmpeg转码。
'''

__author__ = 'Kevin deng'

import time
import os
import sys
import xml.etree.ElementTree as ET


# xml文件读写
def load_xml_file(fname):
	with open(fname, 'r') as f:
		return ET.fromstring(f.read())

def save_xml_file(fname, root):
	with open(fname, 'wb') as f:
		strxml = ET.tostring(root, encoding='utf8')
		f.write(strxml)


def exec_pg(path, args):
	''' 执行一个带参数的外部程序,返回pid。只能在linux下执行'''
	pid = os.fork()
	if pid<0:
		print("fork error: %d" % pid)
	elif pid==0:
		ret = os.execv(path, args)
		return ret
	elif pid>0:
		print("fork new pg: %d" % pid)
	
	return pid


def kill_pg(pid):
	""" 杀死指定pid的linux进程 """
	cmd = "kill -9 %s" % pid
	print(cmd)
	return os.system(cmd)	

def system_cmd(cmd):
	return os.system(cmd)


def modify_xml_url(root, flag):
	for url in root.iter('Url'):
		if flag== 0:
			url.text = "http://192.168.10.12:8880/down/wangshulun/test00.m3u8"
		else :
			url.text = "http://192.168.10.12:8880/down/wangshulun/test010.m3u8"


def modif_config_file(fname, flag):
	root = load_xml_file(fname);
	if root==None:
		print("error in load_xml_file")
		return

	modify_xml_url(root, flag)
	save_xml_file(fname, root)


def do_work():
	cmd = "wget --timeout=5 --tries=2 \"http://192.168.10.12:9876/vss?programid=1&event=1&channelid=1&delay1=5&delay2=25\""
	system_cmd(cmd)	
	
	confname = "./config.xml"
	modif_config_file(confname, 0)

	dispatch_path = "./dispatcher"
	dispatch_args = ["dispatcher"]
	pid = exec_pg(dispatch_path, dispatch_args)

	#wait 4 minutes
	time.sleep(240)
	kill_pg(pid)

	modif_config_file(confname, 1)
	system_cmd(dispatch_path)	


if __name__ == '__main__':
	do_work()
