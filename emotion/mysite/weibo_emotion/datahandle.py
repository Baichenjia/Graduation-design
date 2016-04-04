# -*- coding: utf-8 -*-
__author__ = 'Bai Chenjia'

import jieba
import sys
import re
import codecs
import time
reload(sys)
sys.setdefaultencoding('utf-8')

#对data.txt原始的语料进行处理，去除客观语句：保留1-1主观正面，1-2主观反面
def Delate_keguan():
	str1 = "1	1"
	str2 = "1	2"
	f = open('emotion_file/data.txt', 'r')
	f1 = open('emotion_file/data_zhuguan.txt', 'w')
	#按行读取文件，预处理
	for line in f.readlines():
		if str1 in line or str2 in line:  # 如果包含需要的文本,则对文本进行预处理
			line = re.sub("COAE2014", '', line)
			line = re.sub(r"#翡翠#_weibo", '', line)
			line = re.sub(r"#保险#_weibo", '', line)
			line = re.sub(r"#保险#_weibo", '', line)
			line = re.sub(r"&保险&", '', line)
			line = re.sub(r"&翡翠&", '', line)
			line = re.sub(r"#手机#_weibo", '', line)
			line = re.sub(r"&手机&", '', line)
			line = re.sub(r"car_review", '', line)
			line = re.sub(r"COAE2012", '', line)
			line = re.sub(r"digital_review", '', line)
			line = re.sub(r"unknown_review", '', line)
			line = re.sub(r"视频：", '', line)
			line = re.sub(r"视频为", '', line)
			line = re.sub(r"COAE2011", '', line)
			line = re.sub(r"编辑点评 ：", '', line)
			line = re.sub(r"组图：", '', line)
			line = re.sub(r"图文：", '', line)
			line = re.sub(r"图为：", '', line)
			line = re.sub(r"导读：", '', line)
			line = re.sub(r"字号：", '', line)
			line = re.sub(r"COAE2009", '', line)
			line = re.sub(r"news_review&user_review", '', line)
			line = re.sub(r"2012NLP&&CC", '', line)
			line = re.sub(r"#菲军舰恶意撞击#_weibo", '', line)
			line = re.sub(r"#国旗下讨伐教育制度#_weibo", '', line)
			line = re.sub(r"#韩寒方舟子之争#_weibo", '', line)
			line = re.sub(r"#假和尚搂女子#_weibo", '', line)
			line = re.sub(r"#奖状植入广告#_weibo", '', line)
			line = re.sub(r"#90后暴打老人#_weibo", '', line)
			line = re.sub(r"#90后当教授#_weibo", '', line)
			line = re.sub(r"#六六叫板小三#_weib", '', line)
			line = re.sub(r"#名古屋市长否认南京大屠杀#_weibo", '', line)
			line = re.sub(r"#彭宇承认撞了南京老太#_weibo", '', line)
			line = re.sub(r"#皮鞋果冻#_weibo", '', line)
			line = re.sub(r"#苹果封杀360#_weibo", '', line)
			line = re.sub(r"#三亚春节宰客#_weibo", '', line)
			line = re.sub(r"#食用油涨价#_weibo", '', line)
			line = re.sub(r"#洗碗工留剩菜被开除#_weibo", '', line)
			line = re.sub(r"#学雷锋被钓鱼执法#_weibo", '', line)
			line = re.sub(r"#中国教师收入全球几垫底#_weibo", '', line)
			line = re.sub(r"#官二代求爱不成将少女毁容#_weibo", '', line)
			line = re.sub(r"编辑点评：", '', line)
			line = re.sub(r"经销商点评 ：", '', line)
			line = re.sub(r"[中关村在线家电频道原创] ", '', line)
			line = re.sub(r"#官员调研#_weibo", '', line)
			line = re.sub(r"#iPad3#_weibo", '', line)
			line = re.sub(r"#疯狂的大葱#_weibo", '', line)
			line = re.sub(r"#官员财产公示#_weibo", '', line)
			line = re.sub(r"&", '', line)
			line = re.sub(r"分享！", '', line)
			line = re.sub(r"天顺祥！", '', line)
			line = re.sub(r"分享时间！", '', line)
			line = re.sub(r"，这款宝贝很不错，推荐给你哦～：", '', line)
			line = line.strip()
			f1.write(line)    # 处理后写入data_zhuguan中
			f1.write('\n')
	print "对data.txt原始的语料进行处理，去除客观语句：保留1-1主观正面，1-2主观反面"
	f1.close()
	f.close()


#去除停用词
def Delete_stopwords():
	print '分词并去除停用词...'
	f_stop = open('emotion_file/stopwords.txt')  # 停用词列表打开
	f_stop_list = []
	for word in f_stop.readlines():
		f_stop_list.append(word)
	f_stop.close()

	f_text = open("emotion_file/data_zhuguan.txt", "r")   # 读取文本
	f_nostop = codecs.open('emotion_file/data_zhuguan_nostop.txt', 'w', encoding='UTF-8')
	for text in f_text.readlines():  # 按行读取进行分词和去除停用词
		f_seg_list = list(jieba.cut(text, cut_all=False))  # 精确模式
		for word in f_seg_list:
			if word in f_stop_list:
				print word
			else:
				f_nostop.write(word)
	f_text.close()
	print"停用词去除完成..."  # 反馈结果


# 把文本的正反极性存入另一个文件 data_jixing.txt 该文件值保存文本极性
def Store_polarity():
	str1 = "1	1"   # 主观积极
	str2 = "1	2"   # 主观消极
	f = open('emotion_file/data_zhuguan_nostop.txt', 'r')  # 已经去除停用词的文件
	f1 = open('emotion_file/data_jixing.txt', 'w')  # 该文件只保留data文本的极性
	#按行读取文件，并匹配字符串中间内容
	lines = f.readlines()
	for line in lines:
		if str1 in line:
			f1.write("1\n")   # 主观积极
		if str2 in line:
			f1.write("2\n")   # 主观消极
	f1.close()
	f.close()


#分别计算每句中的nag_a,nag_d,nag_i,neg_l,neg_n,neg_v,pos_a,pos_d,pos_i,pos_l,pos_n,pos_v,but(转折词),no(否定词)
#构造 18 维向量
def Class_count():
	########################################################首先读取词典转为List
	#反向词典
	f_neg_a = open('hownet/dic/neg_a.txt')
	f_neg_b = open('hownet/dic/neg_b.txt')
	f_neg_d = open('hownet/dic/neg_d.txt')
	f_neg_i = open('hownet/dic/neg_i.txt')
	f_neg_l = open('hownet/dic/neg_l.txt')
	f_neg_n = open('hownet/dic/neg_n.txt')
	f_neg_v = open('hownet/dic/neg_v.txt')
	f_neg_z = open('hownet/dic/neg_z.txt')

	#正向词典
	f_pos_a = open('hownet/dic/pos_a.txt')
	f_pos_b = open('hownet/dic/pos_a.txt')
	f_pos_d = open('hownet/dic/pos_d.txt')
	f_pos_i = open('hownet/dic/pos_i.txt')
	f_pos_l = open('hownet/dic/pos_l.txt')
	f_pos_n = open('hownet/dic/pos_n.txt')
	f_pos_v = open('hownet/dic/pos_v.txt')
	f_pos_z = open('hownet/dic/pos_v.txt')

	##################################构造反面词列表
	f_neg_a_text = f_neg_a.read()
	f_neg_a.close()
	f_neg_a_list = f_neg_a_text.split('\n')  # 读取词库的词，编码，转为list

	f_neg_b_text = f_neg_b.read()
	f_neg_b.close()
	f_neg_b_list = f_neg_b_text.split('\n')  # 读取词库的词，编码，转为list

	f_neg_d_text = f_neg_d.read()
	f_neg_d.close()
	f_neg_d_list = f_neg_d_text.split('\n')  # 读取词库的词，编码，转为list

	f_neg_i_text = f_neg_i.read()
	f_neg_i.close()
	f_neg_i_list = f_neg_i_text.split('\n')   # 读取词库的词，编码，转为list

	f_neg_l_text = f_neg_l.read()
	f_neg_l.close()
	f_neg_l_list = f_neg_l_text.split('\n')  # 读取词库的词，编码，转为list

	f_neg_n_text = f_neg_n.read()
	f_neg_n.close()
	f_neg_n_list = f_neg_n_text.split('\n')  # 读取词库的词，编码，转为list

	f_neg_v_text = f_neg_v.read()
	f_neg_v.close()
	f_neg_v_list = f_neg_v_text.split('\n')  # 读取词库的词，编码，转为list

	f_neg_z_text = f_neg_z.read()
	f_neg_z.close()
	f_neg_z_list = f_neg_z_text.split('\n')  # 读取词库的词，编码，转为list

	##################################构造正面词列表
	f_pos_a_text = f_pos_a.read()
	f_pos_a.close()
	f_pos_a_list = f_pos_a_text.split('\n')  # 读取词库的词，编码，转为list

	f_pos_b_text = f_pos_b.read()
	f_pos_b.close()
	f_pos_b_list = f_pos_b_text.split('\n')  # 读取词库的词，编码，转为list

	f_pos_d_text = f_pos_d.read()
	f_pos_d.close()
	f_pos_d_list = f_pos_d_text.split('\n')  # 读取词库的词，编码，转为list

	f_pos_i_text = f_pos_i.read()
	f_pos_i.close()
	f_pos_i_list = f_pos_i_text.split('\n')  # 读取词库的词，编码，转为list

	f_pos_l_text = f_pos_l.read()
	f_pos_l.close()
	f_pos_l_list = f_pos_l_text.split('\n')  # 读取词库的词，编码，转为list

	f_pos_n_text = f_pos_n.read()
	f_pos_n.close()
	f_pos_n_list = f_pos_n_text.split('\n')   # 读取词库的词，编码，转为list

	f_pos_v_text = f_pos_v.read()
	f_pos_v.close()
	f_pos_v_list = f_pos_v_text.split('\n')   # 读取词库的词，编码，转为list

	f_pos_z_text = f_pos_z.read()
	f_pos_z.close()
	f_pos_z_list = f_pos_z_text.split('\n')   # 读取词库的词，编码，转为list

	##################################构造转折词列表
	f_but = open('hownet/dic/but.txt')
	f_but_text = f_but.read()
	f_but.close()
	f_but_list = f_but_text.split('\n')   # 读取词库的词，编码，转为list

	##################################构造否定词列表
	f_no = open('hownet/dic/no.txt')
	f_no_text = f_no.read()
	f_no.close()
	f_no_list = f_no_text.split('\n')   # 读取词库的词，编码，转为list
############################################################词典构建完毕

#########################################################构建18维向量
	f = open("emotion_file/data_zhuguan_nostop.txt", "r")     # 去除停用词后的文本
	f1 = open("emotion_file/data_count.txt", "w")      # 写入了每句话的各个类别的词的数目统计
	f1.write("neg_a neg_b neg_d neg_i neg_l neg_n neg_v neg_z pos_a pos_b pos_d pos_i pos_l pos_n pos_v pos_z but no\n")
	for f_test in f.readlines():   # 读取data_zhuguan_nostop.txt
		# 逐行读取文件，每句话切分后统计每个词在各个文件中出现的次数
		neg_n_count, neg_v_count, neg_a_count, neg_d_count, neg_l_count, neg_i_count = 0, 0, 0, 0, 0, 0
		pos_n_count, pos_v_count, pos_a_count, pos_d_count, pos_l_count, pos_i_count = 0, 0, 0, 0, 0, 0
		neg_b_count, neg_z_count, pos_b_count, pos_z_count = 0, 0, 0, 0
		but_count = 0   # 转折词
		no_count = 0    # 否定词
		nn_count = ""    # 结果向量
		f_seg_list = list(jieba.cut(f_test, cut_all=False))   # 去除停用词后的文本进行分词
		#print f_test
		#print f_seg_list[:]
		for word in f_seg_list:  # 转成列表
			if word in f_neg_a_list:           # 逐个词检查在哪个词性列表中
				#print ' neg_a:', word,
				neg_a_count += 1
			if word in f_neg_b_list:
				#print ' neg_b:', word,
				neg_b_count += 1
			if word in f_neg_d_list:
				#print ' neg_d:', word,
				neg_d_count += 1
			if word in f_neg_i_list:
				#print ' neg_i:', word,
				neg_i_count += 1
			if word in f_neg_l_list:
				#print ' neg_l:', word,
				neg_l_count += 1
			if word in f_neg_n_list:
				#print ' neg_n:', word,
				neg_n_count += 1
			if word in f_neg_v_list:
				#print ' neg_v:', word,
				neg_v_count += 1
			if word in f_neg_z_list:
				#print ' neg_z:', word,
				neg_z_count += 1

			if word in f_pos_a_list:
				#print ' pos_a:', word,
				pos_a_count += 1
			if word in f_pos_b_list:
				#print ' pos_b:', word,
				pos_b_count += 1
			if word in f_pos_d_list:
				#print ' pos_d:', word,
				pos_d_count += 1
			if word in f_pos_i_list:
				#print ' pos_i:', word,
				pos_i_count += 1
			if word in f_pos_l_list:
				#print ' pos_l:', word,
				pos_l_count += 1
			if word in f_pos_n_list:
				#print ' pos_n:', word,
				pos_n_count += 1
			if word in f_pos_v_list:
				#print ' pos_v:', word,
				pos_v_count += 1
			if word in f_pos_z_list:
				#print ' pos_z:', word,
				pos_z_count += 1

			if word in f_but_list:
				#print ' but:', word,
				but_count += 1
			if word in f_no_list:
				#print ' no:', word
				no_count += 1

		#neg_a neg_b neg_d neg_i neg_l neg_n neg_v neg_z pos_a pos_b pos_d pos_i pos_l pos_n pos_v pos_z but no
		nn_count += str(neg_a_count)+" "+str(neg_b_count)+" "+str(neg_d_count)+" "+str(neg_i_count)+" "+str(neg_l_count)+" "+str(neg_n_count)+" "+str(neg_v_count)+" "+str(neg_z_count)+" "+str(pos_a_count)+" "+str(pos_b_count)+" "+str(pos_d_count)+" "+str(pos_i_count)+" "+str(pos_l_count)+" "+str(pos_n_count)+" "+str(pos_v_count)+" "+str(pos_z_count)+" "+str(but_count)+" "+str(no_count)+"\n"
		#print nn_count, '\n\n'
		f1.write(nn_count)  # 写入了每句话的各个类别的词的数目统计，data_count.txt
	f1.close()
	f.close()
	print"训练数据向量化完成..."  # 每句话的各个类别的词的数目统计写入data_count.txt

if __name__ == "__main__":
	#删除客观文本，保留主观文本。输入：data.txt   输出：data_zhuguan.txt
	#Delate_keguan()

	#在此前将data_zhuguan.txt的编码转换成UTF-8
	#去除停用词，利用文件stopwords.txt。输入:data_zhuguan.txt   输出:data_zhuguan_nostop.txt
	#Delete_stopwords()

	#提取极性，单独保存至文件data_jixing.txt
	#Store_polarity()

	#分别计算每句中各种词出现的次数。输入data_zhuguan_nostop.txt  输出data_count.txt
	start = time.clock()
	Class_count()
	end = time.clock()
	print "程序运行时间: %f s"%(end - start)