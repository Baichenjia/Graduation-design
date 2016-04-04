# -*- coding: utf-8 -*-
__author__ = 'Bai Chenjia'

import jieba.posseg as pseg
import sys
import time
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
reload(sys)
sys.setdefaultencoding("utf-8")


# 1.对某个用户的微博进行分词处理，保留名词，连接成字符串，写入文件并返回str
def handel_weibo(filename):
	fp = open("f://emotion/mysite/Label_extract/weibo_corpus/" + filename, 'r')
	contents = []
	for line in fp.readlines():    # 按行处理
		line = line.strip()
		line.decode('utf-8')
		seg_lines = pseg.cut(line)  # 分词标注
		for seg_line in seg_lines:   # 判断如果是名词则保留
			if seg_line.flag == 'n' or seg_line.flag == 'nr' or seg_line.flag == 'ns' or seg_line.flag == 'nt' or seg_line.flag == 'nz':
				contents.append(seg_line.word)  # 保留名词
	#print "length:", len(contents)
	fp.close()
	# 将生成的列表写入文件
	fp_handel = open('f://emotion/mysite/Label_extract/weibo_corpus_handel/handel_' + filename, 'w+')
	for content in contents:
		fp_handel.write(content)
		fp_handel.write('\n')
	fp_handel.close()


# 2.处理所有的原始语料，即30个人的所有微博，抽取名词写入文件
def handel_total_weibo():
	for i in range(30):
		handel_weibo(str(i) + '.txt')
		print str(i) + '.txt 处理完毕....'

###############################注： 函数 1 和 2 运行完后会生成文件，今后便不再调用


# 3.读取处理好的30个博主的原始语料，生成str返回
def read_handel_list():
	str_handel_list = []
	for i in range(30):
		str_handel_list.append("")    # 分别记录30位博主的微博
		filename = "f://emotion/mysite/Label_extract/weibo_corpus_handel/handel_" + str(i) + ".txt"
		fp = open(filename, 'r')   # 读取文件形成列表
		contents = []
		for content in fp.readlines():
			content = content.strip()
			content.decode('utf-8')
			contents.append(content)
		fp.close()
		str_handel_list[i] = ' '.join(contents)
	return str_handel_list


# 4.处理待测试的博主chinese_weibo.txt，提取名词，生成str返回
def read_test_list():
	fp = open("f://emotion/mysite/weibo_crawler/chinese_weibo.txt", 'r')
	contents = []
	for line in fp.readlines():    # 按行处理
		line = line.strip()
		line.decode('utf-8')
		seg_lines = pseg.cut(line)  # 分词标注
		for seg_line in seg_lines:   # 判断如果是名词则保留
			if seg_line.flag == 'n' or seg_line.flag == 'nr' or seg_line.flag == 'ns' or seg_line.flag == 'nt' or seg_line.flag == 'nz':
				contents.append(seg_line.word)  # 保留名词
	fp.close()
	#for w in contents:
	#	print w

	# 生成str作为函数返回值
	str_test = ' '.join(contents)
	return str_test


# 5.主程序，计算chinese_weibo.txt中微博名词的TF-IDF值，返回排名前100的词
def TFIDF_result():
	str_handel_list = read_handel_list()   # 返回30个博主微博名词序列集合，列表每个元素是一个str
	str_test = read_test_list()  # 读取待测试博主的所有微博，返回值为str
	# 构建TF-IDF语料库
	corpus = str_handel_list[:]  # TF-IDF语料集合
	corpus.append(str_test)    # 最后一个元素是待测试语料
	print "TF-IDF corpus building success..."
	######################### 使用scikit-learn进行 TF-IDF加权计算
	# 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
	vectorizer = CountVectorizer()
	# 该类会统计每个词语的tf-idf权值
	transformer = TfidfTransformer()
	# 第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
	tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
	# 获取词袋模型中的所有词语
	word = vectorizer.get_feature_names()
	# 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重
	weight = tfidf.toarray()
	print "TF-IDF score is calcuated success..."
	# 输出第30类文本，即待测试文本的TF-IDF权值
	results = []
	for j in range(len(word)):
		if word[j] == '网页' or word[j] == '链接' or len(word[j]) == 1:  # 剔除无用信息和长度为1的词
			continue
		results.append((word[j], weight[30][j]))  # 构成元组（词，权值）
	sorted_results = sorted(results, key=lambda result: result[1], reverse=True)   # 按照权值排序
	# 取TF-IDF权值前100的词返回
	fp_tfidf_result = open("f://emotion/mysite/Label_extract/result_tfidf.txt", 'w+')
	tfidf_results = []
	for i in range(100):   # 提取权值排名前100的词，写入文件，生成列表返回
		tfidf_results.append((sorted_results[i][0], sorted_results[i][1]))
		fp_tfidf_result.write(sorted_results[i][0] + ' ' + str(round(sorted_results[i][1], 10)))
		fp_tfidf_result.write('\n')
	fp_tfidf_result.close()
	return tfidf_results


"""
6.后处理，提取出标签
方法：查看权值前100的关键词中是否有相邻的组合存在，仅抽取出在原文中出现次数超过 2 次的组合计算权重
扩展后的词串权重，为组成它的词语的权重之和。按照权重排序后，抽取前 10 作为自动生成的用户标签
"""
def post_handel_tfidf():
	# 读取排名前100的词和权值
	fp_result = open('f://emotion/mysite/Label_extract/result_tfidf.txt', 'r')
	results = {}          # 字典存储词和权值共100个
	words = []   # 存储100个词
	for result in fp_result.readlines():
		result = result.strip()
		word, score = result.split(' ')  # 按空格分割，分别为词和权值
		results[word] = float(score)  # str转为float
		words.append(word)
	fp_result.close()
	#读取原始微博连成字符串
	fp_weibo = open('f://emotion/mysite/weibo_crawler/chinese_weibo.txt', 'r')
	weibo_list = []
	for content in fp_weibo.readlines():
		content = content.strip()
		weibo_list.append(content)
	fp_weibo.close()

	#将排名前100的词组成词对，查找在原始微博中出现的次数，并记录
	labels = []
	for i in range(100):
		for j in range(i, 100):
			str1 = words[i] + words[j]
			str2 = words[j] + words[i]  # 连成词对的两种不同形式
			str1_count = 0   # str1出现的次数
			str2_count = 0   # str2出现的次数
			if str1 == "网页链接" or str2 == "网页链接" or words[i] == "链接" or words[j] == "链接":  # 去除噪音
				continue
			if words[i] == words[j]:  # 剔除噪音和相等的情况
				continue
			for sent in weibo_list:
				str1_count += sent.count(str1)
				str2_count += sent.count(str2)
			if str1_count > 1:  # 如果出现次数大于2次，则表示该标签较为稳定，可以加入考虑
				labels.append((str1, results[words[i]] + results[words[j]]))  # 添加元组（词组，TF-IDF值）
			if str2_count > 1:
				labels.append((str2, results[words[i]] + results[words[j]]))  # 添加元组（词组，TF-IDF值）
	sorted_labels = sorted(labels, key=lambda w: w[1], reverse=True)   # 按照词组的tf-idf权值排序
	set_sorted_labels = list(set(sorted_labels))
	set_sorted_labels.sort(key=sorted_labels.index)  # 去重

	# 取得排名前10的标签返回
	result_labels = []
	if len(set_sorted_labels) > 10:
		i = 0
		for word1, score1 in set_sorted_labels:
			if i > 10:
				break
			i += 1
			if word1 == '事件沉船':
				word1 = '沉船事件'
			result_labels.append((word1, score1))
	else:
		result_labels = set_sorted_labels[:]
	for label in result_labels:
		print label[0], label[1]
	return result_labels



if __name__ == '__main__':
	start = time.clock()
	#handel_total_weibo() # 处理30个人的所有微博，抽取名词写入文件。处理完毕后该函数不再运行
	tfidf_results = TFIDF_result()
	result_labels = post_handel_tfidf()
	print "running time" + str(time.clock()-start) + ' s'
