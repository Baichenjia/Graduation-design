# -*- coding: utf-8 -*-
__author__ = 'Bai Chenjia'

import re
from bs4 import BeautifulSoup
from Getraw_HTML import get_rawHTML
import Login
#BeautifulSooup不适合解析中文文本，尝试过但是没有成功

import sys
reload(sys)
sys.setdefaultencoding("utf-8")  #设置默认编码，防止在写入文件时出现编码问题

def filter_tags(htmlstr):
	#先过滤CDATA
	re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>',re.I)      #匹配CDATA   re.I表示忽略大小写
	re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',re.I)    #Script
	re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',re.I)    #style
	re_br = re.compile('<br\s*?/?>')    #处理换行
	re_h = re.compile('</?\w+[^>]*>')     #HTML标签
	re_comment = re.compile('<!--[^>]*-->')   #HTML注释
	s = re_cdata.sub('',htmlstr)  #去掉CDATA

	s = re_script.sub('',s)  #去掉SCRIPT
	s = re_style.sub('',s)   #去掉style
	s = re_br.sub('',s)    #将br转换为换行
	s = re_h.sub('',s)   #去掉HTML 标签
	s = re_comment.sub('',s)   #去掉HTML注释

	s = re.sub(r'\\t','',s)
	s = re.sub(r'\\n\\n','',s)
	s = re.sub(r'\\r','',s)
	s = re.sub(r'<\/?\w+[^>]*>','',s)

	#s = re.sub(r'<\\\/div\>','',s)  #去除<\/div>
	#s = re.sub(r'<\\\/a\>','',s)  #去除<\/a>
	#s = re.sub(r'<\\\/span\>','',s)  #去除<\/span>
	#s = re.sub(r'<\\\/i\>','',s)  #去除<\/i>
	#s = re.sub(r'<\\\/li\>','',s)  #去除<\/li>
	s = re.sub(r'<\\\/dd\>','',s)  #去除<\/dd>
	s = re.sub(r'<\\\/dl\>','',s)  #去除<\/dl>
	s = re.sub(r'<\\\/dt\>','',s)  #去除<\/dt>
	#s = re.sub(r'<\\\/ul\>','',s)  #去除<\/ul>
	#s = re.sub(r'<\\\/em\>','',s)  #去除<\/em>
	#s = re.sub(r'<\\\/p\>','',s)  #去除<\/p>
	s = re.sub(r'<\\\/label\>','',s)  #去除<\/label>
	s = re.sub(r'<\\\/select\>','',s)  #去除<\/select>
	s = re.sub(r'<\\\/option\>','',s)  #去除<\/option>
	s = re.sub(r'<\\\/tr\>','',s)  #去除<\/tr>
	s = re.sub(r'<\\\/td\>','',s)  #去除<\/td>

	s = re.sub(r'@[^<]*','',s)   #去掉@后字符
	s = re.sub(r'<a[^>]*>[^<]*','',s)


	#去掉多余的空行
	blank_line = re.compile(r'(\\n)+')
	s = blank_line.sub('\n',s)     #将连续换行转换成一个换行
	s = s.replace('  ','')

	return s


def Handel(content, fp2):
	Handel_text = []
	lines = content.splitlines(True)    #按行分割每行分别处理
	for line in lines:
		#在用正则表达式处理之前首先根据开头的内容进行匹配
		if re.match(r'(\<script\>FM\.view\(\{\"ns\"\:\"pl\.content\.homeFeed\.index\"\,\"domid\"\:\"Pl_Official)(.*)', line):
			#print "line",line
			#调用正则表达式处理函数进行处理
			temp_new = filter_tags(line)
			#print "temp_new",temp_new
			Handel_text.append(filter_tags(line))   #调用正则处理函数

	content_chinese = ""   #初始化，最后的中文字符串
	for text in Handel_text:
		#print "text",text
		cha_text = unicode(text,'utf-8')  #编码
		#中文,空格,标点，引号，顿号，感叹号
		word = re.findall(ur"[\u4e00-\u9fa5]+|，|。|：|\s|\u00A0|\u3000|'#'|\d|\u201C|\u201D|\u3001|\uFF01|\uFF1F|\u300A|\u300B|FF1B|FF08|FF09",cha_text)
		if word:   #如果该句子中含有上述字符
			#print "word",word
			for char in word:
				if char == ' ':
					content_chinese += ' '
				elif char == '\s':       #三种空格的形式
					content_chinese += ' '
				elif char == '\u00A0':   #中文空格
					content_chinese += ' '
				elif char == '\u3000':   #英文空格
					content_chinese += ' '
				elif char == '#':
					content_chinese += '\n'
				else:
					content_chinese += char
		content_chinese += '\n'
	#循环结束，content_chinese生成
	#写入文件handel.txt中

	fp3 = open("f://emotion/mysite/weibo_crawler/handel.txt","w+")
	fp3.write(content_chinese)
	fp3.close()

	#打开该文件
	fp1 = open("f://emotion/mysite/weibo_crawler/handel.txt","r")
	read = fp1.readlines()
	pattern = re.compile(ur"[\u4e00-\u9fa5]+")  #中文文本
	#fp2 = open("chinese_weibo.txt","a")  #初始化写入文件
	for readline in read:
		utf8_readline = unicode(readline,'utf-8')
		if pattern.search(utf8_readline):   #如果在该句话中能找到中文文本则进行处理
			#print readline #测试
			split_readline = readline.split(' ')  #由空格对文本进行分割，split_readline是一个list
			for c in split_readline:
				c = re.sub(r'发布者：[.]*','',c)   #去掉“发布者”
				c = re.sub(r'百度[.]*','',c)   #去掉“百度”
				c = re.sub(r'正在加载中[.]*','',c)
				c = re.sub(r'360安全浏览[.]*','',c)
				c = re.sub(r'抱歉[.]*','',c)
				c = re.sub(r'.*?高速浏览.*','',c)
				#print c,len(c)
				if len(c) > 16:  #提出过短的文本，utf-8编码中一个中文为3个字节长度
					fp2.write(c)
					#print "c",c
	fp1.close()
	#fp2.close()  #文件关闭
	#print "成功解析网页提取微博并且存入chinese_weibo.txt"

if __name__ == '__main__':
	#自行设定要抓取的网页，抓取范冰冰微博的1到5页
	Login.login()
	for i in range(4):
		i = i + 1
		url = 'http://weibo.com/yaochen?is_search=0&visible=0&is_tag=0&profile_ftype=1&page=' + str(i) + '#feedtop'
		#url = 'http://weibo.com/fbb0916?is_search=0&visible=0&is_tag=0&profile_ftype=1&page=' + str(i) + '#feedtop'
		content = get_rawHTML(url)
		Handel(content)   #测试，调用该函数执行
