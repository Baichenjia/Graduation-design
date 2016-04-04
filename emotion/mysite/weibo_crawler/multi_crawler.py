# -*- coding: utf-8 -*-
__author__ = 'Bai Chenjia'

import threading
import Login
import Getraw_HTML
import Gettext_CH
import time


def Crawler(number, weibo_url):
	Login.login()  #首先进行模拟登录
	fp4 = open("f://emotion/mysite/weibo_crawler/chinese_weibo.txt","w+")  #初始化写入文件
	for n in range(number):
		n = n + 1
		url = 'http://weibo.com/' + weibo_url + '?is_search=0&visible=0&is_tag=0&profile_ftype=1&page=' + str(n)
		print "crawler url",url
		content = Getraw_HTML.get_rawHTML(url)  # 调用获取网页源文件的函数执行
		print "page %d get success and write into raw_html.txt"%n
		Gettext_CH.Handel(content, fp4)         # 调用解析页面的函数
		print "page %d handel success and write into chinese_weibo.txt"%n
		#time.sleep(1)
	fp4.close()
	########## 数据爬取完毕！
	# 对爬取到的微博进行去重处理
	fp = open('f://emotion/mysite/weibo_crawler/chinese_weibo.txt', 'r')
	contents = []
	for content in fp.readlines():
		content = content.strip()
		contents.append(content)
	fp.close()
	set_contents = list(set(contents))
	set_contents.sort(key=contents.index)
	fp_handel = open('f://emotion/mysite/weibo_crawler/chinese_weibo.txt', 'w+')
	for content in set_contents:
		fp_handel.write(content)
		fp_handel.write('\n')
	fp_handel.close()


def main_carwler(weibo_url, page_num):
	contents = {}
	print "URL",weibo_url
	Crawler(page_num, weibo_url)   #调用函数开始爬取

	fp5 = open("f://emotion/mysite/weibo_crawler/chinese_weibo.txt", "r")
	index = 1
	for content in fp5.readlines():
		contents[index] = content
		#print "content",content
		index = index + 1
	new_contents = sorted(contents.items(),key=lambda e:e[0],reverse=False)   #排序
	fp5.close()
	return new_contents

if __name__ == '__main__':
	weibo_url = "gaoxiaosong"
	new_contents = main_carwler(weibo_url, 2)
	#for key,value in new_contents:
	#	print key," ",value