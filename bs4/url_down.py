#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test of urllib '

__author__ = 'Kevin deng'

import urllib.request as urllib2


def get_url_data(url):
	response = urllib2.urlopen(url)
	return response.read()


def write_data(filename, data):
	with open(filename, 'wb') as f:
		f.write(data)

def down_url_datas(uri, prefix, postfix, startnumber, outpath):
	num = startnumber

	while True:
		fname = prefix + str(num) + postfix
		url = uri + "/" + fname
		try:
			data = get_url_data(url)
		except urllib2.HTTPError as e:
			print("Error:", url, e.code, e.reason)
			break

		if data:
			write_data(outpath + "/" + fname, data)
		else:
			break

		num += 1


#http://dash.edgesuite.net/akamai/bbb_30fps/bbb_30fps.mpd
def test_down():
	uri = "http://dash.edgesuite.net/akamai/bbb_30fps/bbb_30fps_480x270_600k"
	down_url_datas(uri, "bbb_30fps_480x270_600k_", ".m4v", 0, "D:\\work\\ijk_drm\\doc\\mpd\\akamai")

if __name__=='__main__':
    test_down()