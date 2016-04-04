# -*- coding: utf-8 -*-
__author__ = 'Bai Chenjia'
import WeiboLogin
import urllib2
import re
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

def login():
	username = '13173400814'
	pwd = 'bcj296050240'      #我的新浪微博的用户名和密码
	weibologin = WeiboLogin.WeiboLogin(username, pwd)   #调用模拟登录程序
	if weibologin.Login():
		print "登陆成功..！"  #此处没有出错则表示登录成功
