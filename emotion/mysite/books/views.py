# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.http import Http404
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from mysite.books.models import *
from mysite.weibo_crawler.multi_crawler import main_carwler
from mysite.weibo_emotion import hownet_handel
from mysite.weibo_emotion import readfile
from mysite.Sentiment_dict import dict_main
from mysite.Sentiment_dict import text_process
from mysite.Label_extract import Tfidf_count
from mysite.Label_extract import Textrank_count
from mysite.Label_extract import Cluster_calc_similarity
from mysite.Label_extract import Cluster_count

neg_a, neg_b, neg_d, neg_i, neg_l, neg_n, neg_v, neg_z = [], [], [], [], [], [], [], []
pos_a, pos_b, pos_d, pos_i, pos_l, pos_n, pos_v, pos_z = [], [], [], [], [], [], [], []
but_word, no_word = [], []

#本函数实现了search_form.html中的action，即search方法
def search(request):
    """
    明确地判断q是否包含在request.GET中,
    对于用户提交过来的数据，甚至是正确的数据，都需要进行过滤。
    在这里若没有进行检测，那么用户提交一个空的表单将引发KeyError异常
    """
    # 错误信息
    errors = []
    if 'q' in request.GET:
        q = request.GET['q']
        if not q:   #不为空
            errors.append('Enter a search term, it is empty')
        elif len(q) > 20:
            errors.append('Please enter at most 20 characters')
        #获取数据库中标题包含q的书籍
        else:
            books = Book.objects.filter(title__icontains=q)
            return render_to_response('search_results.html', {'books': books, 'query': q})
    return render_to_response('search_form.html', {'errors': errors})


def login(request):
	error = []
	if request.method == 'POST':    #表单提交时作出相应
		Username = request.POST.get("username")  #获取文本框的用户名
		Password = request.POST.get("p")         #获取文本框的密码
		print "Username:",Username
		print "Password",Password     #测试
		try:
			sql_obj = user.objects.filter(username=Username)  #从数据库根据用户名检索密码
		except:
			error.append("错误信息：")
			error.append("对不起，用户名不存在!")   #如果检索不到密码输出不存在
		else:
			sql_password = sql_obj[0].userpassword  #提取密码字段
			print "SQLPassword",sql_password  #测试
			if sql_password != Password:
				error.append("错误信息：")
				error.append("对不起，密码错误!")   #如果检索到密码但不相等则表示密码错误
			else:
				"""
				error.append("登录成功！")  #用户名密码都正确则登录成功
				"""
				return HttpResponseRedirect('/emotion_steps_1/')
		print "error",error[:]  #测试
	contact = "contact"
	return render_to_response('login.html', {'error':error,'contact':contact})   #向表单传递参数

def register(request):
	error2 = []
	result = False  #是否可以注册的标志
	if request.method == 'POST':
		form_username = request.POST.get("user")
		form_password = request.POST.get("passwd")
		form_repassword = request.POST.get("passwd2")
		form_qq = request.POST.get("qq")    #获取表达中用户输入的用户名密码QQ信息
		print 'form:',form_username,form_password,form_repassword  #测试
		#并不需要对表单相关输入合法性进行验证，JAVASCRIPT语句已经完成
		"""
		try:
			sql_user = user.object.get(username=form_username)
		except:
			result = True   #检索不到该数据，则可以插入给用户
			print "result:",result
		else:
			result = False
			error2.append("该用户名已经存在！请更换")  #可以检索到该数据，表示该用户名已经存在
		if result == True:  #如果可以插入用户
			print 'error2',error2[:]    #测试
		"""
		new_user = user(username=form_username,userpassword=form_password,userqq=form_qq) #构造一个对象
		new_user.save()  #插入数据库中
		error2.append("用户注册成功！请登录！")
		print 'error2',error2[:]    #测试
	return render_to_response('login.html', {'error2':error2})

def emotion_steps_index(request):
	index = "emotion_steps_index"
	step1 = "emotion_steps_1"
	step2 = "emotion_steps_2"
	step3 = "emotion_steps_3"
	step4 = "emotion_steps_4"
	step5 = "emotion_steps_5"
	return render_to_response('emotion_steps_index.html', locals())

def emotion_steps_1(request):
	index = "emotion_steps_index"
	step1 = "emotion_steps_1"
	step2 = "emotion_steps_2"
	step3 = "emotion_steps_3"
	step4 = "emotion_steps_4"
	step5 = "emotion_steps_5"
	return render_to_response('emotion_steps_1.html', locals())

def emotion_steps_2(request):
	index = "emotion_steps_index"
	step1 = "emotion_steps_1"
	step2 = "emotion_steps_2"
	step3 = "emotion_steps_3"
	step4 = "emotion_steps_4"
	step5 = "emotion_steps_5"
	return render_to_response('emotion_steps_2.html', locals())

def emotion_steps_3(request):
	index = "emotion_steps_index"
	step1 = "emotion_steps_1"
	step2 = "emotion_steps_2"
	step3 = "emotion_steps_3"
	step4 = "emotion_steps_4"
	step5 = "emotion_steps_5"
	return render_to_response('emotion_steps_3.html', locals())

def emotion_steps_4(request):
	step1 = "emotion_steps_1"
	step2 = "emotion_steps_2"
	step3 = "emotion_steps_3"
	step4 = "emotion_steps_4"
	step5 = "emotion_steps_5"
	return render_to_response('emotion_steps_4.html', locals())

def emotion_steps_5(request):
	index = "emotion_steps_index"
	step1 = "emotion_steps_1"
	step2 = "emotion_steps_2"
	step3 = "emotion_steps_3"
	step4 = "emotion_steps_4"
	step5 = "emotion_steps_5"
	return render_to_response('emotion_steps_5.html', locals())

def contact_new(request):
	error_subject = []
	error_email = []
	error_message = []
	if request.method == 'POST':
		subject = request.POST.get('subject')
		if not subject:
			error_subject.append("subject error")
		message = request.POST.get('message')
		if not message:
			error_message.append("message error")
		email = request.POST.get('email')
		if not email:
			error_email.append("email error")
		if email and '@' not in email:
			error_email.append("email error")
		print subject,' ',message,' ',email
		print error_email[:]
		if len(error_message) == 0:
			if len(error_subject) == 0:
				if len(error_email) == 0:
					send_mail(
						request.POST['subject'],
						request.POST['message'],
						request.POST.get('email', '1317340814@163.com'),
						['296050240@qq.com'], False, None, None)
					return HttpResponseRedirect('/contact/thanks/')
	return render_to_response('contact_new.html', {
		'error_subject':error_subject,
		'error_email':error_email,
		'error_message':error_message,
		'subject': request.POST.get('subject', ''),
		'message': request.POST.get('message', ''),
		'email': request.POST.get('email', ''),
	})


def thanks(request):
	return render_to_response('thanks.html')

# 根据用户选择的微博域名爬取指定人物的微博
def form_crawler(request):
	index = "emotion_steps_index"
	step1 = "emotion_steps_1"
	step2 = "emotion_steps_2"
	step3 = "emotion_steps_3"
	step4 = "emotion_steps_4"
	step5 = "emotion_steps_5"
	error_subject = []
	if request.method == 'POST':
		subject = request.POST.get('weibo_url')
		if not subject:
			error_subject.append("subject error")
		if len(error_subject) == 0:
			weibo_url = request.POST.get("weibo_url")
			page_num = request.POST.get("page_num")
			if not page_num:
				page_num = 2
			else:
				page_num = int(page_num)
			new_contents = main_carwler(weibo_url, page_num)
			return render_to_response('emotion_steps_1.html', {'contents':new_contents,'index':index,'step1':step1,'step2':step2,'step3':step3,'step4':step4,'step5':step5})
	return render_to_response('emotion_steps_1.html', {'error_subject':error_subject,'index':index,'step1':step1,'step2':step2,'step3':step3,'step4':step4,'step5':step5})


"""
# 提取原始情感词典
def emotion_dic(request):
	if request.method == 'POST':
		pos_all_dic = []
		neg_all_dic = []
		pos_all_dic, neg_all_dic = hownet_handel.read_dic()  # 调用函数读取原始词典内容
		return render_to_response('emotion_steps_2.html',locals())
	return render_to_response('emotion_steps_2.html')
"""
# 获取原始情感词典
def dic_pos_all(request):
	pos_all_dic, neg_all_dic = hownet_handel.read_dic()  # 调用函数读取原始词典内容
	return render_to_response('dic_tem/pos_all.html',{"pos_all_dic":pos_all_dic})

def dic_neg_all(request):
	pos_all_dic, neg_all_dic = hownet_handel.read_dic()  # 调用函数读取原始词典内容
	return render_to_response('dic_tem/neg_all.html',{"neg_all_dic":neg_all_dic})


def classify_dic():
	global neg_a, neg_b, neg_d, neg_i, neg_l, neg_n, neg_v, neg_z, pos_a, pos_b, pos_d, pos_i, pos_l, pos_n, pos_v, pos_z, but_word, no_word
	# 调用函数按照词性进行分类，分别写入不同的文件中
	#hownet_handel.classify_pos()   # 积极 对已经标注的原始语料按照词性写入不同的文件中
	#hownet_handel.classify_neg()    # 消极
	# 调用函数读取分类的情感词典
	neg_a, neg_b, neg_d, neg_i, neg_l, neg_n, neg_v, neg_z, pos_a, pos_b, pos_d, pos_i, pos_l, pos_n, pos_v, pos_z, but_word, no_word = hownet_handel.read_classify()


# 将词典词性标注后分类
classify_dic()   # 按照词性将不同的词放到不同的文本中
def dic_pos_a(request):
	return render_to_response('dic_tem/pos_a.html',{'pos_a': pos_a})
def dic_pos_b(request):
	return render_to_response('dic_tem/pos_b.html',{'pos_b': pos_b})
def dic_pos_d(request):
	return render_to_response('dic_tem/pos_d.html',{'pos_d': pos_d})
def dic_pos_i(request):
	return render_to_response('dic_tem/pos_i.html',{'pos_i': pos_i})
def dic_pos_l(request):
	return render_to_response('dic_tem/pos_l.html',{'pos_l': pos_l})
def dic_pos_n(request):
	return render_to_response('dic_tem/pos_n.html',{'pos_n': pos_n})
def dic_pos_v(request):
	return render_to_response('dic_tem/pos_v.html',{'pos_v': pos_v})
def dic_pos_z(request):
	return render_to_response('dic_tem/pos_z.html',{'pos_z': pos_z})
def dic_neg_a(request):
	return render_to_response('dic_tem/neg_a.html',{'neg_a': neg_a})
def dic_neg_b(request):
	return render_to_response('dic_tem/neg_b.html',{'neg_b': neg_b})
def dic_neg_d(request):
	return render_to_response('dic_tem/neg_d.html',{'neg_d': neg_d})
def dic_neg_i(request):
	return render_to_response('dic_tem/neg_i.html',{'neg_i': neg_i})
def dic_neg_l(request):
	return render_to_response('dic_tem/neg_l.html',{'neg_l': neg_l})
def dic_neg_n(request):
	return render_to_response('dic_tem/neg_n.html',{'neg_n': neg_n})
def dic_neg_v(request):
	return render_to_response('dic_tem/neg_v.html',{'neg_v': neg_v})
def dic_neg_z(request):
	return render_to_response('dic_tem/neg_z.html',{'neg_z': neg_z})
def dic_but_word(request):
	return render_to_response('dic_tem/but_word.html',{'but_word': but_word})
def dic_no_word(request):
	return render_to_response('dic_tem/no_word.html',{'no_word': no_word})

##############################3333# 第三个页面，极性分类
# 提取待训练数据（去除停用词后的）
def jixing_get_zhuguan(request):
	sents = readfile.read_zhuguan()
	return render_to_response('classify_jixing/get_zhuguan.html',{'sents': sents})

def jixing_get_xiangliang(request):
	xiangliang = readfile.read_xiangliang()[:]
	return render_to_response('classify_jixing/get_xiangliang.html',{'xiangliang': xiangliang})

def jixing_get_results(request):
	results = readfile.read_result()[:]
	return render_to_response('classify_jixing/get_results.html',{'results':results})

#############################4444# 第四个页面，情感词典方法的情感打分
def dic_level_one(request):  # 获取六种权值的词
	level_one_dict = text_process.read_quanzhi("one")
	return render_to_response('classify_dict/dic_level_one.html', {'level_one_dict': level_one_dict})
def dic_level_two(request):
	level_two_dict = text_process.read_quanzhi("two")
	return render_to_response('classify_dict/dic_level_two.html', {'level_two_dict': level_two_dict})
def dic_level_three(request):
	level_three_dict = text_process.read_quanzhi("three")
	return render_to_response('classify_dict/dic_level_three.html', {'level_three_dict': level_three_dict})
def dic_level_four(request):
	level_four_dict = text_process.read_quanzhi("four")
	return render_to_response('classify_dict/dic_level_four.html', {'level_four_dict': level_four_dict})
def dic_level_five(request):
	level_five_dict = text_process.read_quanzhi("five")
	return render_to_response('classify_dict/dic_level_five.html', {'level_five_dict': level_five_dict})
def dic_level_six(request):
	level_six_dict = text_process.read_quanzhi("six")
	return render_to_response('classify_dict/dic_level_six.html', {'level_six_dict': level_six_dict})

dic_results = []
def dic_get_result(request):   # 页面第二部分，获取分数
	global dic_results
	dic_results = dict_main.run_score()  # 计算每句话的极性得分，返回list，元素是（得分，微博）
	return render_to_response('classify_dict/dic_get_result.html', {'dic_results': dic_results})

def dic_get_analysis(request):
	global dic_results
	result_dict = dict_main.handel_result(dic_results)   # 计算结果的各种参数，返回字典
	pos_number = result_dict['pos_number']   # 正向微博数
	neg_number = result_dict['neg_number']   # 负向微博数
	mid_number = result_dict['mid_number']   # 中性微博数
	pos_mean = result_dict['pos_mean']  # 积极情感平均分
	neg_mean = result_dict['neg_mean']  # 消极情感平均分
	total_mean = result_dict['total_mean'] # 总的情感平均得分
	total_variance = result_dict['total_variance']  # 总的情感得分方差
	text_pos_number = result_dict['text_pos_number']   # 各种情感评价
	text_neg_number = result_dict['text_neg_number']
	text_mid_number = result_dict['text_mid_number']
	text_pos_mean = result_dict['text_pos_mean']
	text_neg_mean = result_dict['text_neg_mean']
	text_total_mean = result_dict['text_total_mean']
	text_total_var = result_dict['text_total_var']
	return render_to_response('classify_dict/dic_get_analysis.html', locals())

#############################5555# 第五个页面，三种标签抽取算法

def ag1_tfidf_result(request):
	tfidf_results = Tfidf_count.TFIDF_result()
	return render_to_response('classify_label/get_tfidf_result.html', locals())

def ag1_tfidf_label(request):
	result_labels = Tfidf_count.post_handel_tfidf()
	return render_to_response('classify_label/get_tfidf_label.html', locals())

def ag2_textrank_score(request):
	key_words = Textrank_count.build_matrix()
	return render_to_response('classify_label/get_textrank_score.html', locals())

def ag2_textrank_label(request):
	textrank_result_labels = Textrank_count.post_handel_textrank()
	return render_to_response('classify_label/get_textrank_label.html', locals())

def ag3_hit_corpus(request):
	word_number_list = Cluster_calc_similarity.read_hit_corpus()
	return render_to_response('classify_label/get_hit_corpus.html', locals())

def ag3_cluster_label(request):
	cluster_group_result, cluster_result_labels = Cluster_count.kmeans_cluster()
	return render_to_response('classify_label/get_cluster_label.html', locals())



