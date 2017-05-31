#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" 
下载新浪博客html至如下目录规范，并对正文进行规范的提取和整理。
path_root 根目录可以生成目录html
 |-images 存放图片
 |-text   存放博文html
"""

__author__ = 'Kevin deng'


from bs4 import BeautifulSoup
import urllib.request as urllib2
import datetime
import time
import os


def read_txt_file(filename):
	with open(filename, 'r', encoding='utf8') as f:
		return f.read()

def write_txt_file(filename, content):
	with open(filename, 'w', encoding='utf8') as f:
		return f.write(content)

def write_bin_file(filename, content):
	with open(filename, 'wb') as f:
		return f.write(content)

def make_dir(spath):
	if os.path.isdir(spath)==False:
		os.mkdir(spath)

def download_url(url):
	count = 0
	while 1:
		try:
			page = urllib2.urlopen(url)
			return page.read()
		except urllib2.HTTPError as e:  
			print('The server couldn\'t fulfill the request: %s, %s' % (e.code, url))
		except urllib2.URLError as e:   
			print('Failed to reach a server: %s, %s' %(e.reason, url)) 
		except BaseException as e:   
			print("Error in:", url, e) 
		finally:
			count += 1
			if count>3:
				return None
			time.sleep(0.5)

# <td class="blog_tag">
# <span class="SG_txtb">标签：</span>
# <a href="http://search.sina.com.cn/?c=blog&amp;q=%BD%CC%D3%FD&amp;by=tag" target="_blank">教育</a>
# </td>
# </td>
# <td class="blog_class">
# <span class="SG_txtb">分类：</span>
# <a href="http://blog.sina.com.cn/s/articlelist_1333581473_10_1.html" target="_blank">解读精英教育系列</a>
# </td>
def clean_blog_tags(content):
	"""blog tags简化调整"""
	blog_tag = content.find("td", attrs={"class": "blog_tag"})
	h3s = blog_tag.find_all("h3")
	for h3 in h3s:
		del h3.a["href"]
		del h3.a["target"]
		h3.replace_with(h3.a)

	blog_class = content.find("td", attrs={"class": "blog_class"})
	aas = blog_class.find_all("a")
	for aa in aas:
		del aa["href"]
		del aa["target"]


def extract_content(bsobj, url):
	"""提取blog中的有效内容到一个新的html对象，返回"""
	meta = bsobj.find("meta")
	title = bsobj.find("title")
	content = bsobj.find("div", id="articlebody")

	# print(title.string)
	# print(content.attrs)
	# print("children=%d, descendants=%d" % (len(list(content.children)), len(list(content.descendants))))

	clean_content_tags(content)
	# print("children=%d, descendants=%d" % (len(list(content.children)), len(list(content.descendants))))

	# 标签：简化调整
	clean_blog_tags(content)

	# 标签前插入原文地址行，标签后正文前，插入空行,
	article_tag = content.find("div", id="sina_keyword_ad_area")

	strurl = "<div><a href=%s>查看原文</a></div>" % url
	url_line = BeautifulSoup(strurl, "lxml")
	article_tag.insert_before(url_line.div)
	null_line = BeautifulSoup("<div><br></div>", "lxml")
	article_tag.insert_after(null_line.div)


	# 创建新的html对象
	strhtml = "<title></title><body><style> body{background-color:#E1E6E0} </style></body>"
	mainobj = BeautifulSoup(strhtml, "lxml")
	mainobj.head.append(meta)
	
	main_title = mainobj.find("title")
	main_title.string = title.string
	# print(mainobj)

	main_body = mainobj.find("body")
	main_body.append(content)

	return mainobj


# 转载按钮：<div class="turnBoxzz">
# 此博文包含图片的标识：<span class="img2"> ---
# 所有评论：<div class="allComm">
# 分享等信息：
# 		<div id="share" class="shareUp"> 分享
# 		<div class="articalInfo">
# 		<div class="blogzz_zzlist borderc" id="blog_quote" style="display:none">
# 		<div id="loginFollow"></div>
# 		<div class="articalfrontback articalfrontback2 clearfix">
# 		<div class="clearit"></div>  在前后篇之后，有多个

def del_div_class(tag, classname):
	divs = tag.find_all("div", attrs={"class": classname})
	for div in divs:
		div.decompose()

def del_div_id(tag, idname):
	div = tag.find("div", id=idname)
	if div:
		div.decompose()

def del_script(tag):
	divs = tag.find_all("script")
	for div in divs:
		div.decompose()

def clean_content_tags(bsobj):
	del_div_class(bsobj, "turnBoxzz")
	div = bsobj.find("span", attrs={"class": "img2"})
	if div:
		div.decompose()

	del_div_class(bsobj, "allComm")
	del_div_id(bsobj, "share")
	del_div_class(bsobj, "articalInfo")
	del_div_class(bsobj, "blogzz_zzlist borderc")
	del_div_class(bsobj, "articalfrontback articalfrontback2 clearfix")
	del_div_id(bsobj, "loginFollow")
	del_div_class(bsobj, "clearit")
	del_script(bsobj)


# <img alt="中国需要Academy：需要真正的教育和真正的学术理想！" height="690" name="image_operate_67351349686207710" real_src="http://s5.sinaimg.cn/middle/4f7cd6a1x7ac0d4ab96d4&amp;690" src="./中国需要Academy：需要真正的教育和真正的学术理想！_教育张清一_新浪博客_files/4f7cd6a1x7ac0d4ab96d4&amp;690" title="中国需要Academy：需要真正的教育和真正的学术理想！" width="527"/>
def clean_img_tag(img_tag, path_root, path_images, sdt, i):
	"""
	整理简化图像标签的内容
	sdt-博文发布时间字符串
	i-图片在博文中的序号，从1开始
	"""

	#先下载到指定目录，再替换src
	img_fname = "%s/%s/%s_%d.jpeg" % (path_root, path_images, sdt, i)

	try:
		imgurl = img_tag["real_src"]
	except:
		print("error without real_src in ", img_tag)
		return

	img = download_url(imgurl)
	if img!=None:
		write_bin_file(img_fname, img)
	else:
		print("img down error %s: ../%s/%s_%d.jpeg" % (img_tag["src"], path_images, sdt, i))
 
	img_tag["src"] = "../%s/%s_%d.jpeg" % (path_images, sdt, i)

	# 去掉img的real_src，title，name,action-data，action-type字段
	del img_tag["real_src"]
	del img_tag["title"]
	del img_tag["name"]
	del img_tag["action-data"]
	del img_tag["action-type"]

	img_tag.parent.replace_with(img_tag)


def download_blog_html(url, path_root, path_html, path_images):
	"""
	下载url的博客html，提取博客正文，保存到指定text目录，图片都保存到images目录
	path_html，path_images是path_root的子目录名
	"""
	html = download_url(url)
	if html==None:
		print("Error in down %s", url)
		return 

	bsobj = BeautifulSoup(html, "lxml")
	newobj = extract_content(bsobj, url)

	# 提取日期 <span class="time SG_txtc">(2012-10-07 21:22:55)</span>
	dtime = newobj.find("span", attrs={"class": "time SG_txtc"})
	dt = datetime.datetime.strptime(dtime.string, "(%Y-%m-%d %H:%M:%S)")
	sdt = dt.strftime("%Y-%m%d_%H%M%S")

	# 图像索引的处理，包括保存图像
	img_tags = newobj.find_all("img") 
	i = 1
	for img in img_tags:
		clean_img_tag(img, path_root, path_images, sdt, i)
		i += 1

	# print(newobj)
	html_fname = "%s/%s/%s.html" % (path_root, path_html, sdt)
	write_txt_file(html_fname, str(newobj))


def download_blogs(url, path_root, path_html, path_images):
	"""下载当前新浪博客目录页的所有博文，并返回下一页的url"""
	html = download_url(url)
	bsobj = BeautifulSoup(html, "lxml")

	for blog in bsobj.find_all("span", attrs={"class": "atc_title"}):
		html_url = blog.a.attrs["href"]
		download_blog_html(html_url, path_root, path_html, path_images)
		time.sleep(0.2)

	#<li class="SG_pgnext"><a href="http://blog.sina.com.cn/s/articlelist_1333581473_0_2.html" title="跳转至第 2 页">下一页&nbsp;&gt;</a></li>
	nextpage = bsobj.find("li", attrs={"class": "SG_pgnext"})
	if nextpage:
		time.sleep(1.5)
		return nextpage.a.attrs["href"]
	else:
		return None


def download_all_blogs(index_url, path_root):
	"""下载所有博文到指定根目录"""
	path_html = "text"
	path_images = "images"
	make_dir(path_root)
	make_dir("%s/%s" % (path_root, path_html))
	make_dir("%s/%s" % (path_root, path_images))

	while index_url:
		index_url = download_blogs(index_url, path_root, path_html, path_images)


def test_down_blog():
	url = "http://blog.sina.com.cn/s/blog_4f7cd6a10102e05f.html"
	path_root = "./aaa_blog"
	path_html = "text"
	path_images = "images"
	download_blog_html(url, path_root, path_html, path_images)


def test_extract_content():
	url = "http://blog.sina.com.cn/s/blog_4f7cd6a10102e05f.html"
	html = read_txt_file("./doc/zhang-sina-blog01.html")
	bsobj = BeautifulSoup(html, "lxml")
	newobj = extract_content(bsobj, url)
	write_txt_file("./doc/bbb.html", str(newobj))


if __name__=='__main__':
	# test_extract_content()
	# test_down_blog()

	download_all_blogs("http://blog.sina.com.cn/s/articlelist_1333581473_0_1.html", "./zhang1_blogs") 
