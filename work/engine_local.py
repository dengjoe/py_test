#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
按照配置文件program_local.conf的时间安排，调用ffmpeg来发送本地节目源内容。
一个节目需要按播放时间顺序设置好要播放的节目源地址。
每个节目可以配置多个task（即ffmpeg），以满足不同的编码输出需求。
配置文件可以配置多个节目，需要看服务器配置来定。
'''

__author__ = 'Kevin deng'

import json
import time
import os
import sys


program_conf = "../conf/programs_local.json"
setting_conf = "../conf/settings.json"

class PgInput(object):
	''' 节目的输入。保存播放的开始时间，文件地址'''
	def __init__(self,  dic):
		self.begin_time = dic["begin_time"]
		time_array = time.strptime(self.begin_time, "%Y-%m-%d %H:%M:%S")
		self.begin_timestamp = time.mktime(time_array)
		self.url = dic["url"]

	def __str__(self):
		return "begin:%s url:%s" % (self.begin_time, self.url)

class PgTask(object):
	''' 节目的任务。保存ffmpeg的部分命令参数，负责ffmpeg进程的启动、停止'''
	def __init__(self, dic):
		self._pid = -1
		self.task_id = dic["task_id"]
		self.cmd = dic["cmd"]
		self.cmd_optional = dic["cmd_optional"]
		self.cmd_para = dic["cmd_para"]
		self.output = dic["output_url"] + dic["output_para"]

	def __del__(self):
		self.stop()

	def start(self, cmdpath, inurl):
		''' 启动任务,传入输入文件地址。先停止当前任务，再启动新任务 '''
		self.stop()
		cmd_args = "%s %s -i %s %s %s" % (self.cmd, self.cmd_optional, inurl, self.cmd_para, self.output)
		print("start[%d]: %s" % (self.task_id, cmd_args))
		# self._pid = 12345
		self._pid = exec_pg(cmdpath, cmd_args.split())

	def stop(self):
		if self._pid>0:
			cmd = "kill -9 %s" % self._pid
			print("stop: %s" % cmd)
			ret = os.system(cmd)	
			self._pid = -1		

class Program(object):
	''' 一套节目'''
	def __init__(self, dic):
		self._curinput = 0  #当前inputs的列表索引
		self.program_id = dic["program_id"]
		self.inputs  = []
		for item in dic["input"]:
			pinput = PgInput(item)
			self.inputs.append(pinput)

		self.tasks = []
		for item in dic["task"]:
			ptask = PgTask(item)
			self.tasks.append(ptask)

		now = time.time()
		for item in self.inputs:
			if now>=item.begin_timestamp:
				self._curinput += 1
		# print("program_id:%d curinput:%d" % (self.program_id, self._curinput))


	def __str__(self):
		desc = "program_id:%d input:%s task:%s" % (self.program_id, len(self.inputs), len(self.tasks))
		for pin in self.inputs:
			desc += '\n  ' + pin.__str__()
		return desc

	def run(self, cmdpath):
		'''运行节目：取当前时间，判断如果到达下一时间点，停止当前task进程，执行下一task进程'''
		now = time.time()
		for pin in self.inputs[self._curinput:]:
			if now>=pin.begin_timestamp:
				for task in self.tasks:
					task.start(cmdpath, pin.url)

				nowTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(now))				
				print(" program_id=%d, input[%d] %s" % (self.program_id, self._curinput, nowTime))
				self._curinput += 1
				break


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


def load_file_string(fname):
	with open(fname, 'r') as f:
		return f.read()


def json2Programs(strjson):
	ll = []
	l1 = json.loads(strjson)
	for dic in l1:
		ll.append(Program(dic))
	return ll

def json2Cmdpath(strjson):
	dic = json.loads(strjson)
	items = dic["tunnel"]
	for item in items:
		if item["cmd"]=="ffmpeg":
			print("ffmpeg: %s" % item["cmd_path"])
			return  item["cmd_path"]
	return None


if __name__ == '__main__':
	content = load_file_string(setting_conf)
	cmdpath = json2Cmdpath(content)
	if cmdpath==None:
		print("error in %s: without cmd:ffmpeg" % setting_conf)
		sys.exit(-2)

	content = load_file_string(program_conf)
	ls = json2Programs(content)
	for pg in ls:
		print(pg)
	print("\n")
	
	# count = 0
	while 1:
		for pg in ls:
			pg.run(cmdpath)
		time.sleep(1)
		# count += 1
		# if count>1500:
		# 	break

