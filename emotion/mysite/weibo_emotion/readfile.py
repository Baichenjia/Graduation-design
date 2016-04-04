# -*- coding: utf-8 -*-
__author__ = 'Bai Chenjia'

import re
import urllib, urllib2, json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from result import test_file

def read_zhuguan():
	fp_zhuguan = open('f://emotion/mysite/weibo_emotion/emotion_file/data_zhuguan_nostop.txt','r')
	sents = []
	i = 0
	for content in fp_zhuguan.readlines():
		i += 1
		if i > 1000:
			break
		sent = []   # 用于记录每一行的三个部分
		p = re.compile(r'(.*?)\s+(\d)\s+(\d)')
		content.decode('UTF-8')
		content.strip()
		contents = p.match(content)
		try:
			#print contents.group(1)  # 句子正文部分
			#print contents.group(2)
			#print contents.group(3),'\n'
			sent.append(contents.group(1))  # 句子正文部分
			sent.append(contents.group(3))  # 句子极性部分
		except:
			print i,content
		else:
			sents.append(sent)
	return sents

def read_xiangliang():
	fp_xiangliang = open('f://emotion/mysite/weibo_emotion/emotion_file/data_count.txt','r')
	xiangliang = []
	i = 0
	for content in fp_xiangliang.readlines():
		i += 1
		if i == 1:
			continue
		if i > 1000:
			break
		p = re.compile(r'\s+')
		content.strip()
		contents = p.split(content)
		#print "contents",contents[:]
		contents.pop(18)
		#print len(contents)
		xiangliang.append(contents)
	return xiangliang

def read_result():
	test_file()   # 将爬取到的微博分析后写入文件
	fp_result = open('f://emotion/mysite/weibo_emotion/emotion_file/test_result.txt', 'r')
	results = []
	for content in fp_result.readlines():
		p = re.compile(r'^(.*?)is(.*?)is(.*)$')
		contents = p.match(content)
		result = []
		result.append(contents.group(1).decode("utf-8"))
		result.append(contents.group(2))
		result.append(contents.group(3).decode("utf-8"))
		#print result
		results.append(result)
	fp_result.close()
	return results


if __name__ == '__main__':
	#sents = read_zhuguan()[:]   # 读取data_zhuguan_nostop，保留句子和极性
	#xiangliang = read_xiangliang()[:]
	results = read_result()[:]
	#read_result2()