# -*- coding: utf-8 -*-
__author__ = 'Bai Chenjia'
# 实现新浪微博的模拟登录
import urllib2
import cookielib   # 加载网络编程的重要模块
import WeiboEncode
import WeiboSearch

class WeiboLogin:
	#python魔法方法，当初始化该类的对象时会调用此函数
	def __init__(self, user, pwd, enableProxy = False):    # enableProxy表示是否使用代理服务器，默认关闭
		print "初始化新浪微博登录..."
		self.userName = user
		self.passWord = pwd
		self.enableProxy = enableProxy  # 初始化类成员

		# 在提交POST请求之前需要GET获取两个参数,得到的数据中有 "servertime" 和 "nonce" 的值，是随机的
		self.serverUrl = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.18)&_=1407721000736"
		#loginUrl用于第二步，加密后的用户名和密码POST给这个URL
		self.loginUrl = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)"
		#self.postHeader = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0'}
		self.postHeader = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'}
		#self.postHeader = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)'}

	# 生成Cookie接下来的所有get和post请求都带上已经获取的cookie，因为稍大些的网站的登陆验证全靠cookie
	def EnableCookie(self, enableProxy):
		cookiejar = cookielib.LWPCookieJar()  # 建立COOKIE
		cookie_support = urllib2.HTTPCookieProcessor(cookiejar)
		if enableProxy:
			proxy_support = urllib2.ProxyHandler({'http': 'http://122.96.59.107:843'}) # 使用代理
			opener = urllib2.build_opener(proxy_support, cookie_support, urllib2.HTTPHandler)
			print "Proxy enable"
		else:
			opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
		urllib2.install_opener(opener)


	#获取 server time 和 nonce 参数，用于编码密码
	def GetServerTime(self):
		print "getting server time and nonce..."
		serverData = urllib2.urlopen(self.serverUrl).read()   # 获取网页内容
		print 'serverData', serverData
		try:
			# 在JSON中提取serverTime, nonce, pubkey, rsakv字段
			serverTime, nonce, pubkey, rsakv = WeiboSearch.sServerData(serverData)
			print "GetServerTime success"
			return serverTime, nonce, pubkey, rsakv
		except:
			print "解析serverData出错！"
			return None

	def getData(url):
		request = urllib2.Request(url)
		response = urllib2.urlopen(request)
		content = response.read()
		return content


	def Login(self):  # 登录程序
		self.EnableCookie(self.enableProxy)      # Cookie或代理服务器配置，调用自定义函数实现
		serverTime, nonce, pubkey, rsakv = self.GetServerTime()      # 登录第一步，调用函数获取上述信息
		# 准备好所有的POST参数返回postData
		postData = WeiboEncode.PostEncode(self.userName, self.passWord, serverTime, nonce, pubkey, rsakv)
		print "Getting postData success"
		#封装request请求，获得指定URL的文本
		req = urllib2.Request(self.loginUrl, postData, self.postHeader)   # 封装请求信息
		result = urllib2.urlopen(req)  # 登录第二步向self.loginUrl发送用户和密码
		text = result.read()    # 读取内容
		#print text
		"""
		登陆之后新浪返回的一段脚本中定义的一个进一步登陆的url
		之前还都是获取参数和验证之类的，这一步才是真正的登陆
		所以你还需要再一次把这个url获取到并用get登陆即可
		"""
		try:
			loginUrl = WeiboSearch.sRedirectData(text)  # 得到重定位信息后，解析得到最终跳转到的URL
			urllib2.urlopen(loginUrl)  # 打开该URL后，服务器自动将用户登陆信息写入cookie，登陆成功
			print loginUrl


			"""
			content = content.decode("gbk")  # 处理要写入的文本使其可以保留中文文本
			fw = open('content.txt', 'w')
			fw.write(content.encode("u8"))  #写入时进行编码
			fw.close()
			"""
		except:
			print "login failed..."
			return False
		print "login success"
		return True


#主函数新建登录对象，然后登录
if __name__ == '__main__':
	weibologin = WeiboLogin('13173400814', 'bcj296050240') # 用户名、密码
	if weibologin.Login():
		print "登陆成功！"
	"""
	req = urllib2.Request(url='http://weibo.com/yaochen',)
	result = urllib2.urlopen(req)
	text = result.read()
	print len(result.read())
	print eval("u'''"+text+"'''")
	"""