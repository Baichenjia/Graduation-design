# -*- coding: utf-8 -*-
__author__ = 'Bai Chenjia'
# 处理情感字典，分词标注后按照不同词性写入不同的文件

import jieba.posseg as pseg
import sys
import codecs
import re
reload(sys)
sys.setdefaultencoding('utf-8')

def jieba_cut():
	#处理pos_all_dict文件
	fp_pos = open("hownet/pos_all_dict.txt", "r")   # 原始的积极词的词典
	fp_pos_cut = codecs.open('hownet/pos_all_cut.txt', "w+", encoding='UTF-8')  # 将结果保存到另一个文档中
	contents = fp_pos.readlines()
	for content in contents:
		word = content.decode("utf-8")  # 解码
		word_tag = pseg.cut(word)
		str_tag = ""
		for tag in word_tag:
			str_tag += str(tag.word) + '/' + str(tag.flag)
		p = re.compile(r'/x(.*)')
		str_tag = p.sub(r'\1', str_tag)   # 提取第一分组
		fp_pos_cut.write(str_tag)
	fp_pos.close()
	fp_pos_cut.close()

	#处理pos_all_dict文件
	fp_neg = open("hownet/neg_all_dict.txt", "r")   # 原始的积极词的词典
	fp_neg_cut = codecs.open('hownet/neg_all_cut.txt', "w+", encoding='UTF-8')  # 将结果保存到另一个文档中
	contents = fp_neg.readlines()
	for content in contents:
		word = content.decode("utf-8")  # 解码
		word_tag = pseg.cut(word)
		str_tag = ""
		for tag in word_tag:
			str_tag += str(tag.word) + '/' + str(tag.flag)
		p = re.compile(r'/x(.*)')
		str_tag = p.sub(r'\1', str_tag)  # 提取第一分组
		fp_neg_cut.write(str_tag)
	fp_neg.close()
	fp_neg_cut.close()

# 将词性进行处理，词性归并
def handel_cixing(list_content):
	content = list_content[:]
	new_content = []
	#print "content", content[0][1]
	if (content[0][1] == '/ad') or (content[0][1] == '/an'):
		new_content.append(content[0][0])
		new_content.append('/a')

	elif content[0][1] == '/dg':
		new_content.append(content[0][0])
		new_content.append('/d')

	elif (content[0][1] == '/Ng') or (content[0][1] == '/nrt') or (content[0][1] == '/nr') or (content[0][1] == '/ns') or (content[0][1] == '/ns') or (content[0][1] == '/nt') or (content[0][1] == '/nz'):
		new_content.append(content[0][0])
		new_content.append('/n')

	elif content[0][1] == '/tg':
		new_content.append(content[0][0])
		new_content.append('/t')

	elif (content[0][1] == '/vg') or (content[0][1] == '/vd') or (content[0][1] == '/vn'):
		new_content.append(content[0][0])
		new_content.append('/v')

	else:
		new_content.append(content[0][0])
		new_content.append(content[0][1])
	if len(new_content) > 2:
		print 'error'
	return new_content


#构建积极倾向的词典，按按词性分类，写入不同的文件中
def classify_pos():
	#处理积极的词典
	fp_pos_cut = open('f://emotion/mysite/weibo_emotion/hownet/pos_all_cut.txt', 'r')
	f_pos_a = codecs.open('f://emotion/mysite/weibo_emotion/hownet/dic/pos_a.txt', 'w', encoding='UTF-8')
	f_pos_b = codecs.open('f://emotion/mysite/weibo_emotion/hownet/dic/pos_b.txt', 'w', encoding='UTF-8')
	f_pos_d = codecs.open('f://emotion/mysite/weibo_emotion/hownet/dic/pos_d.txt', 'w', encoding='UTF-8')
	f_pos_i = codecs.open('f://emotion/mysite/weibo_emotion/hownet/dic/pos_i.txt', 'w', encoding='UTF-8')
	f_pos_l = codecs.open('f://emotion/mysite/weibo_emotion/hownet/dic/pos_l.txt', 'w', encoding='UTF-8')
	f_pos_n = codecs.open('f://emotion/mysite/weibo_emotion/hownet/dic/pos_n.txt', 'w', encoding='UTF-8')
	f_pos_v = codecs.open('f://emotion/mysite/weibo_emotion/hownet/dic/pos_v.txt', 'w', encoding='UTF-8')
	f_pos_z = codecs.open('f://emotion/mysite/weibo_emotion/hownet/dic/pos_z.txt', 'w', encoding='UTF-8')

	str1 = "/a"   # 形容词
	str2 = "/b"   # 区别词
	str3 = "/d"   # 副词
	str4 = "/i"   # 成语
	str5 = "/l"   # 习用语
	str6 = "/n"   # 名词
	str7 = "/v"   # 动词
	str8 = "/z"   # 状态词

	# 处理pos_all_cut文件
	contents = fp_pos_cut.readlines()
	for content in contents:
		content = content.decode("utf-8")  # 解码
		p = re.compile(r'(.*?)(/\w+)')
		list_content = p.findall(content)   # 将标注后的词汇转化成列表
		#print "list_content", list_content[:]
		if len(list_content) == 0:   # 如果为0则不写入
			continue

		if len(list_content) == 1:
			handel_content = handel_cixing(list_content[:])[:]    # 将词性经过归并处理归并成几个大类
		else:                      # 如果词被切分则当做习用语
			handel_content = []
			p2 = re.compile(r'/\w+')
			#print "content", content
			handel_content.append(p2.sub('', content).strip())   # 去掉分割的标签，统一加上标签/l
			handel_content.append('/l')
			#print "handel_content", handel_content[0], handel_content[1]
		#print "--------词性预处理完毕，一个list代表一行，有两个元素，分别为词和词性"

		if handel_content[1] == str1:     # 形容词a
			f_pos_a.write(handel_content[0])
			f_pos_a.write('\n')
		elif handel_content[1] == str2:     # 区别词b
			f_pos_b.write(handel_content[0])
			f_pos_b.write('\n')
		elif handel_content[1] == str3:     # 副词d
			f_pos_d.write(handel_content[0])
			f_pos_d.write('\n')
		elif handel_content[1] == str4:     # 成语i
			f_pos_i.write(handel_content[0])
			f_pos_i.write('\n')
		elif handel_content[1] == str5:     # 习用语l
			f_pos_l.write(handel_content[0])
			f_pos_l.write('\n')
		elif handel_content[1] == str6:     # 名词n
			f_pos_n.write(handel_content[0])
			f_pos_n.write('\n')
		elif handel_content[1] == str7:     # 动词v
			f_pos_v.write(handel_content[0])
			f_pos_v.write('\n')
		elif handel_content[1] == str8:     # 状态词z
			f_pos_z.write(handel_content[0])
			f_pos_z.write('\n')
		else:
			pass

	f_pos_a.close()
	f_pos_b.close()
	f_pos_d.close()
	f_pos_i.close()
	f_pos_l.close()
	f_pos_n.close()
	f_pos_v.close()
	f_pos_z.close()
	#积极倾向词典构建完毕


#构建消极倾向的词典，按按词性分类，写入不同的文件中
def classify_neg():
	#处理消极的词典
	fp_neg_cut = open('f://emotion/mysite/weibo_emotion/hownet/neg_all_cut.txt', 'r')
	f_neg_a = codecs.open('f://emotion/mysite/weibo_emotion/hownet/dic/neg_a.txt', 'w', encoding='UTF-8')
	f_neg_b = codecs.open('f://emotion/mysite/weibo_emotion/hownet/dic/neg_b.txt', 'w', encoding='UTF-8')
	f_neg_d = codecs.open('f://emotion/mysite/weibo_emotion/hownet/dic/neg_d.txt', 'w', encoding='UTF-8')
	f_neg_i = codecs.open('f://emotion/mysite/weibo_emotion/hownet/dic/neg_i.txt', 'w', encoding='UTF-8')
	f_neg_l = codecs.open('f://emotion/mysite/weibo_emotion/hownet/dic/neg_l.txt', 'w', encoding='UTF-8')
	f_neg_n = codecs.open('f://emotion/mysite/weibo_emotion/hownet/dic/neg_n.txt', 'w', encoding='UTF-8')
	f_neg_v = codecs.open('f://emotion/mysite/weibo_emotion/hownet/dic/neg_v.txt', 'w', encoding='UTF-8')
	f_neg_z = codecs.open('f://emotion/mysite/weibo_emotion/hownet/dic/neg_z.txt', 'w', encoding='UTF-8')

	str1 = "/a"   # 形容词
	str2 = "/b"   # 区别词
	str3 = "/d"   # 副词
	str4 = "/i"   # 成语
	str5 = "/l"   # 习用语
	str6 = "/n"   # 名词
	str7 = "/v"   # 动词
	str8 = "/z"   # 状态词

	# 处理neg_all_cut文件
	contents = fp_neg_cut.readlines()
	for content in contents:
		content = content.decode("utf-8")  # 解码
		p = re.compile(r'(.*?)(/\w+)')
		list_content = p.findall(content)   # 将标注后的词汇转化成列表
		#print "list_content", list_content[:]
		if len(list_content) == 0:   # 如果为0则不写入
			continue

		if len(list_content) == 1:
			handel_content = handel_cixing(list_content[:])[:]    # 将词性经过归并处理归并成几个大类
		else:                      # 如果词被切分则当做习用语
			handel_content = []
			p2 = re.compile(r'/\w+')
			#print "content", content
			handel_content.append(p2.sub('', content).strip())
			handel_content.append('/l')
			#print "handel_content", handel_content[0], handel_content[1]
		#print "--------词性预处理完毕，一个list代表一行，有两个元素，分别为词和词性"

		if handel_content[1] == str1:     # 形容词a
			f_neg_a.write(handel_content[0])
			f_neg_a.write('\n')
		elif handel_content[1] == str2:     # 区别词b
			f_neg_b.write(handel_content[0])
			f_neg_b.write('\n')
		elif handel_content[1] == str3:     # 副词d
			f_neg_d.write(handel_content[0])
			f_neg_d.write('\n')
		elif handel_content[1] == str4:     # 成语i
			f_neg_i.write(handel_content[0])
			f_neg_i.write('\n')
		elif handel_content[1] == str5:     # 习用语l
			f_neg_l.write(handel_content[0])
			f_neg_l.write('\n')
		elif handel_content[1] == str6:     # 名词n
			f_neg_n.write(handel_content[0])
			f_neg_n.write('\n')
		elif handel_content[1] == str7:     # 动词v
			f_neg_v.write(handel_content[0])
			f_neg_v.write('\n')
		elif handel_content[1] == str8:     # 状态词z
			f_neg_z.write(handel_content[0])
			f_neg_z.write('\n')
		else:
			pass

	f_neg_a.close()
	f_neg_b.close()
	f_neg_d.close()
	f_neg_i.close()
	f_neg_l.close()
	f_neg_n.close()
	f_neg_v.close()
	f_neg_z.close()
	#积极倾向词典构建完毕

# 读取原始情感词典返回List
def read_dic():
	fp_pos = open('f://emotion/mysite/weibo_emotion/hownet/pos_all_dict.txt', 'r')
	fp_neg = open('f://emotion/mysite/weibo_emotion/hownet/neg_all_dict.txt', 'r')
	pos_all_dic = []
	i, j = 0, 0
	for word in fp_pos.readlines():
		i += 1
		if i > 1000:
			break
		pos_all_dic.append(word)
	neg_all_dic = []
	for word in fp_neg.readlines():
		j += 1
		if j >= 1000:
			break
		neg_all_dic.append(word)
	fp_pos.close()
	fp_neg.close()
	return pos_all_dic, neg_all_dic

# 读取分类字典
def read_classify():
	neg_a, neg_b, neg_d, neg_i, neg_l, neg_n, neg_v, neg_z = [], [], [], [], [], [], [], []
	pos_a, pos_b, pos_d, pos_i, pos_l, pos_n, pos_v, pos_z = [], [], [], [], [], [], [], []
	but_word, no_word = [], []

	# 构建消极情感词典
	fp_neg_a = open('f://emotion/mysite/weibo_emotion/hownet/dic/neg_a.txt')
	for word in fp_neg_a.readlines():
		neg_a.append(word)
	fp_neg_a.close()

	fp_neg_b = open('f://emotion/mysite/weibo_emotion/hownet/dic/neg_b.txt')
	for word in fp_neg_b.readlines():
		neg_b.append(word)
	fp_neg_b.close()

	fp_neg_d = open('f://emotion/mysite/weibo_emotion/hownet/dic/neg_d.txt')
	for word in fp_neg_d.readlines():
		neg_d.append(word)
	fp_neg_d.close()

	fp_neg_i = open('f://emotion/mysite/weibo_emotion/hownet/dic/neg_i.txt')
	for word in fp_neg_i.readlines():
		neg_i.append(word)
	fp_neg_i.close()

	fp_neg_l = open('f://emotion/mysite/weibo_emotion/hownet/dic/neg_l.txt')
	for word in fp_neg_l.readlines():
		neg_l.append(word)
	fp_neg_l.close()

	fp_neg_n = open('f://emotion/mysite/weibo_emotion/hownet/dic/neg_n.txt')
	for word in fp_neg_n.readlines():
		neg_n.append(word)
	fp_neg_n.close()

	fp_neg_v = open('f://emotion/mysite/weibo_emotion/hownet/dic/neg_v.txt')
	for word in fp_neg_v.readlines():
		neg_v.append(word)
	fp_neg_v.close()

	fp_neg_z = open('f://emotion/mysite/weibo_emotion/hownet/dic/neg_z.txt')
	for word in fp_neg_z.readlines():
		neg_z.append(word)
	fp_neg_z.close()
	#消极情感词典构建完毕
	#构建积极情感词典
	fp_pos_a = open('f://emotion/mysite/weibo_emotion/hownet/dic/pos_a.txt')
	for word in fp_pos_a.readlines():
		pos_a.append(word)
	fp_pos_a.close()

	fp_pos_b = open('f://emotion/mysite/weibo_emotion/hownet/dic/pos_b.txt')
	for word in fp_pos_b.readlines():
		pos_b.append(word)
	fp_pos_b.close()

	fp_pos_d = open('f://emotion/mysite/weibo_emotion/hownet/dic/pos_d.txt')
	for word in fp_pos_d.readlines():
		pos_d.append(word)
	fp_pos_d.close()

	fp_pos_i = open('f://emotion/mysite/weibo_emotion/hownet/dic/pos_i.txt')
	for word in fp_pos_i.readlines():
		pos_i.append(word)
	fp_pos_i.close()

	fp_pos_l = open('f://emotion/mysite/weibo_emotion/hownet/dic/pos_l.txt')
	for word in fp_pos_l.readlines():
		pos_l.append(word)
	fp_pos_l.close()

	fp_pos_n = open('f://emotion/mysite/weibo_emotion/hownet/dic/pos_n.txt')
	for word in fp_pos_n.readlines():
		pos_n.append(word)
	fp_pos_n.close()

	fp_pos_v = open('f://emotion/mysite/weibo_emotion/hownet/dic/pos_v.txt')
	for word in fp_pos_v.readlines():
		pos_v.append(word)
	fp_pos_v.close()

	fp_pos_z = open('f://emotion/mysite/weibo_emotion/hownet/dic/pos_z.txt')
	for word in fp_pos_z.readlines():
		pos_z.append(word)
	fp_pos_z.close()

	fp_no_word = open('f://emotion/mysite/weibo_emotion/hownet/dic/no.txt')
	for word in fp_no_word.readlines():
		no_word.append(word)
	fp_no_word.close()

	fp_but_word = open('f://emotion/mysite/weibo_emotion/hownet/dic/but.txt')
	for word in fp_but_word.readlines():
		but_word.append(word)
	fp_but_word.close()

	return neg_a, neg_b, neg_d, neg_i, neg_l, neg_n, neg_v, neg_z, pos_a, pos_b, pos_d, pos_i, pos_l, pos_n, pos_v, pos_z, but_word, no_word

if __name__ == '__main__':
	#jieba_cut()   # 对原始语料进行分词标注
	classify_pos()   # 积极 对已经标注的原始语料按照词性写入不同的文件中
	classify_neg()    # 消极