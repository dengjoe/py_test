#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module to catch article list '

__author__ = 'Kevin deng'


from bs4 import BeautifulSoup

from article_item import ArticleItem
from url_html import get_html

def get_articles_sina(bsobj, path, fout, fileout):
	articles = []
	for blog in bsobj.find_all("span", attrs={"class": "atc_title"}):
		href = blog.a.attrs["href"]
		article = ArticleItem(blog.a.string, href)
		articles.append(article)

	i = 0
	for ti in bsobj.find_all("span", attrs={"class": "atc_tm SG_txtc"}):
		articles[i].time = ti.string.strip()+":00"
		i += 1

	fout(articles, fileout) 
	#<li class="SG_pgnext"><a href="http://blog.sina.com.cn/s/articlelist_1333581473_0_2.html" title="跳转至第 2 页">下一页&nbsp;&gt;</a></li>
	nextpage = bsobj.find("li", attrs={"class": "SG_pgnext"})
	if nextpage:
		return nextpage.a.attrs["href"]
	else:
		return None
		
def get_articles_ifeng(bsobj, path, fout, fileout):
	articles = []
	for blog in bsobj.find_all("h3"):
		href = path + blog.a.attrs["href"]
		article = ArticleItem(blog.a.attrs["title"], href)
		articles.append(article)

	i = 0
	# for ti in bsobj.find_all("div", class_="blog_main_time"): #这种也行，不过下面attrs的更通用
	for ti in bsobj.find_all("div", attrs={"class": "blog_main_time"}):
		articles[i].time = ti.p.string.strip()
		i += 1

	i = 0
	for abstract in bsobj.find_all("div", id="blog_article_content"):
		articles[i].abstract = abstract.p.string
		i += 1

	fout(articles, fileout)
	nextpage = bsobj.find("a", text="下一页")
	if nextpage:
		return path + nextpage.attrs["href"]
	else:
		return None


def catch_all_titles(path, url, fout, fileout):
	html = get_html(url)
	bsobj = BeautifulSoup(html, "lxml")

	if path.find("ifeng.com") > 0:
		return get_articles_ifeng(bsobj, path, fout, fileout)
	elif  path.find("sina.com.cn") > 0:
		return get_articles_sina(bsobj, path, fout, fileout)
	else:
		return None


def articles_stdout(articles, fileout=None):
	for article in articles:
		article.print()

def articles_write(articles, fileout):
	with open(fileout, 'a', encoding='utf8') as f:
		for article in articles:
			heads = article.time + " \t《"+article.title+"》" + " \t" + article.herf + "\n"
			f.write(heads)
			# f.write("  " + article.abstract + "\n\n")


def test_catch(path, url, outname):
	# path = "http://blog.ifeng.com"
	# url = path + "/946563.html"
	# outname = "./shihanbing.txt"
	fout = articles_write
	# fout = articles_stdout

	while url:
		url = catch_all_titles(path, url, fout, outname)
		print(url)


if __name__=='__main__':
	# test_catch("http://blog.ifeng.com", "http://blog.ifeng.com/946563.html", "./shihanbing.txt")	
	test_catch("http://blog.sina.com.cn", "http://blog.sina.com.cn/s/articlelist_1333581473_0_1.html", "./zhangqingyi.txt")	

# http://blog.ifeng.com/946563-2.html 的目录索引
# <div class="page">
# 	<span class="current">1</span> 
# 	<a href="/946563-2.html">2</a> 
# 	<a href="/946563-3.html">3</a> 
# 	<a href="/946563-4.html">4</a> 
# 	<a href="/946563-5.html">5</a> 
# 	<a href="/946563-2.html">下一页</a> 
# 	<a href="/946563-68.html">尾页</a>
# </div>

# <div class="page">
# 	<a href="/946563-1.html">首页</a> 
# 	<a href="/946563-1.html">上一页</a> 
# 	<a href="/946563-1.html">1</a> 
# 	<span class="current">2</span> 
# 	<a href="/946563-3.html">3</a> 
# 	<a href="/946563-4.html">4</a> 
# 	<a href="/946563-5.html">5</a> 
# 	<a href="/946563-3.html">下一页</a> 
# 	<a href="/946563-69.html">尾页</a>
# </div>

# <div class="page">
# 	<a href="/946563-1.html">首页</a> 
# 	<a href="/946563-68.html">上一页</a> 
# 	<a href="/946563-65.html">65</a> 
# 	<a href="/946563-66.html">66</a> 
# 	<a href="/946563-67.html">67</a> 
# 	<a href="/946563-68.html">68</a> 
# 	<span class="current">69</span> 
# </div>