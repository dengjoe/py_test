#!/usr/bin/env python2
# -*- coding: utf-8 -*-

' 进程管理：启动/停止/是否运行(返回 0-停止，1-运行) '

__author__ = 'Kevin deng'

# import subprocess
import commands
import sys
import os


def getpid(process):
    cmd = "ps -ef | grep '%s' | grep -v grep | grep -v procmd" % process
    info = commands.getoutput(cmd)
    infos = info.split("\n")
    # print infos

    for str in infos:
        names = str.split()
        if len(names) <8:
            continue

        name = os.path.basename(names[7])
        if name == process:
            print names
            return names[1]
    
    return -1

def process_monitor(processname, cmd):
    names = processname.split()
    pid = getpid(os.path.basename(names[0]))
    ret = 0

    if cmd == "start":
        if pid==-1:
            cmdpath = os.getcwd()
            apppath = os.path.dirname(names[0])
            cmd = "nohup %s &" % processname
            print cmd
            os.chdir(apppath)
            ret = os.system(cmd)
            os.chdir(cmdpath)
        else:
            print "%s is already runing." % processname
    elif cmd == "stop":
        if pid != -1:
            cmd = "kill -9 %s" % pid
            print cmd
            ret = os.system(cmd)
        else:
            print "%s is not runing." % processname
    elif cmd == "status":
        if pid==-1:
            ret = 0
        else:
            ret = 1

    return ret


if __name__=="__main__":
    if len(sys.argv) < 3:
        print "Usage: %s \"process params\" [start|stop|status]"  % sys.argv[0]
        sys.exit(2)

    ret = process_monitor(sys.argv[1], sys.argv[2])
    sys.exit(ret)
