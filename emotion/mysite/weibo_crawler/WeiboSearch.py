# -*- coding: utf-8 -*-
__author__ = 'Bai Chenjia'
import re
import json

# 在 serverData 中查找 server time 和 nonce
# 解析过程主要使用了正则表达式和JSON
def sServerData(serverData):
	p = re.compile('\((.*)\)')    # 定义正则表达式
	jsonData = p.search(serverData).group(1)  # 通过正则表达式查找并提取分组1
	data = json.loads(jsonData)
	serverTime = str(data['servertime'])   # 获取data中的相应字段，Json对象为一个字典
	nonce = data['nonce']
	pubkey = data['pubkey']
	rsakv = data['rsakv']  # 获取字段
	return serverTime, nonce, pubkey, rsakv


#Login中解析重定位结果部分函数
def sRedirectData(text):
	"""
	#在运行过程中打印text的信息如下:
	<html>
		<head>
		<title>����ͨ��֤</title>
		<meta http-equiv="refresh" content="0; url=&#39;http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack&retcode=4402&reason=%B1%A7%C7%B8%A3%A1%B5%C7%C2%BC%CA%A7%B0%DC%A3%AC%C7%EB%C9%D4%BA%F2%D4%D9%CA%D4&#39;"/>
		<meta http-equiv="Content-Type" content="text/html; charset=GBK" />
		</head>
		<body bgcolor="#ffffff" text="#000000" link="#0000cc" vlink="#551a8b" alink="#ff0000">
		<script type="text/javascript" language="javascript">
		location.replace("http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack&retcode=4402&reason=%B1%A7%C7%B8%A3%A1%B5%C7%C2%BC%CA%A7%B0%DC%A3%AC%C7%EB%C9%D4%BA%F2%D4%D9%CA%D4");
		</script>
		</body>
		</html>
	因此需要从中抽取出location.replace后的括号中的地址，用正则表达式完成
	"""""
	p = re.compile('location\.replace\([\'"](.*?)[\'"]\)')
	loginUrl = p.search(text).group(1)
	print 'loginUrl:',loginUrl   # 输出信息，若返回值含有 'retcode = 0' 则表示登录成功
	return loginUrl








"""
# 在 serverData 中查找 server time 和 nonce
# 解析过程主要使用了正则表达式和JSON
def sServerData(serverData):
	p = re.compile('\((.*)\)')  # 定义正则表达式
	jsonData = p.search(serverData).group(1)  # 通过正则表达式查找并提取分组1
	data = json.loads(jsonData)
	serverTime = str(data['servertime'])  # 获取data中的相应字段，Json对象为一个字典
	nonce = data['nonce']
	pubkey = data['pubkey']
	rsakv = data['rsakv']        # 获取字段
	return serverTime, nonce, pubkey, rsakv
"""
#Login中解析重定位结果部分函数
"""
def sRedirectData(text):
	"""
"""
	在运行过程中打印text的信息如下
	<html>
		<head>
		<title>����ͨ��֤</title>
		<meta http-equiv="refresh" content="0; url=&#39;http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack&retcode=4402&reason=%B1%A7%C7%B8%A3%A1%B5%C7%C2%BC%CA%A7%B0%DC%A3%AC%C7%EB%C9%D4%BA%F2%D4%D9%CA%D4&#39;"/>
		<meta http-equiv="Content-Type" content="text/html; charset=GBK" />
		</head>
		<body bgcolor="#ffffff" text="#000000" link="#0000cc" vlink="#551a8b" alink="#ff0000">
		<script type="text/javascript" language="javascript">
		location.replace("http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack&retcode=4402&reason=%B1%A7%C7%B8%A3%A1%B5%C7%C2%BC%CA%A7%B0%DC%A3%AC%C7%EB%C9%D4%BA%F2%D4%D9%CA%D4");
		</script>
		</body>
		</html>
	因此需要从中抽取出location.replace后的括号中的地址，用正则表达式完成
	"""
"""
	p = re.compile('location\.replace\(\"(.*)\"\);')  # 此处和之前略有区别，小心！
	loginUrl = p.search(text).group(1)
	print "loginUrl", loginUrl   # 获取到location.replace后的内容
	return loginUrl
"""