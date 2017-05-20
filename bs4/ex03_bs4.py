#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test of urllib '

__author__ = 'Kevin deng'

from bs4 import BeautifulSoup
# from urllib import parse
import urllib.request as urllib2


def get_html(url):
	page = urllib2.urlopen(url)
	html = page.read()
	return html

def write_html(filename, html):
	with open(filename, 'wb') as f:
		f.write(html)



def find_all_h3(bsobj):
	#<h3><a href="/article/46853799.html" title="时寒冰：税负争论终止生出超大利空">时寒冰：税负争论终止生出超大利空</a></h3>
	for blog in bsobj.find_all("h3"):
		print(blog.a.attrs)

	# <div id="blog_article_content">
	# 	<p>税负争论终止生出超大利空时寒冰有关企业税收负担重还是不重的争论，终于有了明确的官方结论。新华社播发了财政部前部长、全国社保基金理事会理事长楼继伟的观点。他的观点主要如下：一，中国的税负不重。楼继伟表示，美国企业所得税率为35%，中国税率是25%。从国际比较来看，无论哪个口径，中国宏观税负都低于世界平均水平。楼继伟指出：“比较税负，关键看宏观税负，即总收入与名义GDP的比值。如果不包括国有土地使用权出让收入，2014、2015年我国宏观...</p>
	# </div>
	for abstract in bsobj.find_all("div", id="blog_article_content"):
		print(abstract.p.string)


def test_html_parse():
	html = get_html("http://blog.ifeng.com/946563.html")
	#write_html("./shindex.html", html)
	bsobj = BeautifulSoup(html, "lxml")
	#print(type(bsobj))
	find_all_h3(bsobj)


if __name__=='__main__':
    test_html_parse()