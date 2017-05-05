#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'kevin deng'

import requests
 
payload = {'key1': 'value1', 'key2': 'value2'}
headers = {'content-type': 'application/json'}
r = requests.get("http://httpbin.org/get", params=payload, headers=headers)
print(r.url)
print(r.status_code)
print(r.text)
print(r.json())
print(r.cookies)

print("\npost")
url = "http://httpbin.org/post"
try:
	ret = requests.post(url, data=payload, timeout=0.01)
	print(ret.text)
except Exception as e:
	print(e, type(e))


print("\ncookies")
url = 'http://httpbin.org/cookies'
cookies = dict(cookies_are='working')
r = requests.get(url, cookies=cookies)
print(r.text)
print(r.cookies)
