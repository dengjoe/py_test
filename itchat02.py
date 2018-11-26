#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test itchat module '

__author__ = 'kevin deng'

import itchat

itchat.login()
#爬取自己好友相关信息， 返回一个json文件
#friends = itchat.get_friends(update=True)[0:]
chatrooms = itchat.get_chatrooms(update=True)[0:]
print(chatrooms)


# def search_friends(self, name=None, userName=None, remarkName=None, nickName=None, wechatAccount=None):
#     return self.storageClass.search_friends(name, userName, remarkName, nickName, wechatAccount)
# def search_chatrooms(self, name=None, userName=None):
#     return self.storageClass.search_chatrooms(name, userName)
# def search_mps(self, name=None, userName=None):
#     return self.storageClass.search_mps(name, userName)
    

   