#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a urllib test module '

__author__ = 'Kevin deng'

from urllib import parse
import urllib.request as urllib2

def test_urlopen():
	response = urllib2.urlopen("http://www.baidu.com/", timeout=10)
	print(response.read())

def test_post():
	values = {"username":"1016903103@qq.com","password":"XXXX"}
	data = parse.urlencode(values) 
	url = "https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn"
	request = urllib2.Request(url, data)
	response = urllib2.urlopen(request)
	print(response.read())

def test_get():
	values = {"username":"1016903103@qq.com","password":"XXXX"}
	data = parse.urlencode(values) 
	print("urlencode:", data)
	url = "http://passport.csdn.net/account/login"
	geturl = url + "?"+data
	request = urllib2.Request(geturl)
	try:
		response = urllib2.urlopen(request)
		print(response.read())
	except urllib2.URLError as e:
		print(e.reason)

def test_headers():
# 其他常用headers的属性：
# User-Agent : 有些服务器或 Proxy 会通过该值来判断是否是浏览器发出的请求
# Content-Type : 在使用 REST 接口时，服务器会检查该值，用来确定 HTTP Body 中的内容该怎样解析：
# 	application/xml ： 在 XML RPC，如 RESTful/SOAP 调用时使用
# 	application/json ： 在 JSON RPC 调用时使用
# 	application/x-www-form-urlencoded ： 浏览器提交 Web 表单时使用
# 	在使用服务器提供的 RESTful 或 SOAP 服务时， Content-Type 设置错误会导致服务器拒绝服务

	url = 'http://www.qiushibaike.com/hot/'
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'  
	#在构建request时传入，在请求时，就加入了headers传送，服务器若识别了是浏览器发来的请求，就会得到响应。
	headers = { 'User-Agent' : user_agent }  

	# values = {'username' : 'cqc',  'password' : 'XXXX' }  
	# data = urllib.urlencode(values)  
	request = urllib2.Request(url, None, headers)  
	try:
		response = urllib2.urlopen(request)  
		print(response.read())
	except urllib2.URLError as e:
		print(e.reason)


def test_proxy(enable_proxy):
	proxy_handler = urllib2.ProxyHandler({"http" : 'http://some-proxy.com:8080'})
	null_proxy_handler = urllib2.ProxyHandler({})
	if enable_proxy:
	    opener = urllib2.build_opener(proxy_handler)
	else:
	    opener = urllib2.build_opener(null_proxy_handler)
	urllib2.install_opener(opener)


def test_url():
	url = r'https://docs.python.org/3.5/search.html?q=parse&check_keywords=yes&area=default'
	parseResult = parse.urlparse(url)
	print("\nparseResult:",parseResult)
	param_dict = parse.parse_qs(parseResult.query)
	print("\nparam_dict:", param_dict)
	print("q0:", param_dict['q'][0])

if __name__=='__main__':
	# test_proxy(True)
	test_urlopen()
	test_headers()
	# test_post()
	# test_get()
	test_url()	
