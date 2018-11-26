#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import psutil

# pip install psutil

' test psutil cpu, mem, and net. '

__author__ = 'Kevin deng'


def test_cpu():
	print("");
	print("cpu logical count: %d" % psutil.cpu_count())
	print("cpu pysical count: %d" % psutil.cpu_count(logical=False))

	print("cpu percent: ", psutil.cpu_percent())

def test_mem():
	print("");
	mem = psutil.virtual_memory()
	print(mem)
	print("mem total: %.2f(M)" % float(mem.total/1024/1024))
	print("mem used: %.2f(M)" % float(mem.used/1024/1024))
	print("mem free: %.2f(M)" % float(mem.free/1024/1024))

def test_disk():
	print("");
	disks = psutil.disk_partitions()
	for dis in disks:
		print(dis)

	dios = psutil.disk_io_counters(perdisk=True)
	# print(dios)
	for k,v in dios.items():
		print(k, ":", v)


def test_net():
	print("\nnet all:");
	nio_all = psutil.net_io_counters()
	print(nio_all)

	print("\nnet eth:");
	nios = psutil.net_io_counters(pernic=True)
	# print(nios)
	# print("");
	for nio,v in nios.items():
		print(nio, ":", v)


if __name__=="__main__":
	test_cpu()
	test_mem()
	test_disk()
	test_net()