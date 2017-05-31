#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = 'kevin deng'


import time


class  ArticleItem(object):
	"""博客文章索引。包括文章title，url，发布时间，简要内容。"""
	def __init__(self, title, herf):
		self._title = title
		self._herf = herf
		self._time = ""
		self._timestamp = 0
		self._abstract = ""

	@property
	def title(self):
		return self._title

	@property
	def herf(self):
		return self._herf

	@property
	def time(self):
		return self._time

	@time.setter
	def time(self, ti):
		self._time = ti
		#转换为时间戳:
		timeArray = time.strptime(ti, "%Y-%m-%d %H:%M:%S")
		self._timestamp = int(time.mktime(timeArray))

	@property
	def time_stamp(self):
		return self._timestamp

	@property
	def abstract(self):
		return self._abstract

	@abstract.setter
	def abstract(self, abstr):
		self._abstract = abstr


	def print(self):
		print(self._time, " \t《"+self._title+"》", " \t", self._herf)
		print(self._abstract)

