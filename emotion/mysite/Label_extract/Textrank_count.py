# -*- coding: utf-8 -*-
__author__ = 'Bai Chenjia'
import jieba.posseg as pseg
import sys
import time
import networkx as nx
import numpy as np
reload(sys)
sys.setdefaultencoding("utf-8")


"""
1.将要处理的微博内容按每条微博进行分词，去除停用词，保留名词，形成一个二级列表返回
如：原始微博为：['这间酒店位于北京东三环，里面摆放很多雕塑，文艺气息十足', '答谢宴于晚上8点开始']
经过处理后为：[[ '酒店', '位于, '北京, '东三环, '摆放, '雕塑, '文艺, '气息' ],[ '答谢', '宴于, '晚上' ]]
"""
def handel_weibo_data():
	#读取要处理的微博正文提取名词，去除停用词
	fp = open("f://emotion/mysite/weibo_crawler/chinese_weibo.txt", 'r')
	weibo_data = []   # 所有的微博，为一个二级列表[[句子][句子][句子]]其中句子已经被分词去停用词并保留名词
	for line in fp.readlines():    # 按行处理
		contents = []
		line = line.strip()
		line.decode('utf-8')
		seg_lines = pseg.cut(line)  # 分词标注
		for seg_line in seg_lines:   # 判断如果是名词则保留
			if seg_line.flag == 'n' or seg_line.flag == 'nr' or seg_line.flag == 'ns' or seg_line.flag == 'nt' or seg_line.flag == 'nz':
				contents.append(seg_line.word)  # 保留名词
		weibo_data.append(contents)
	fp.close()
	return weibo_data

"""
2.构建矩阵。
方法：用户微博文本构建以候选关键词（即选取的名词）为节点的无向图
滑动窗口定为一条微博的长度，即倘若两个词在同一条微博中出现，就认为它们之间存在较强的语义联系，共现次数加1
对每一条微博进行同样的词对共现次数提取，图节点间边的权重记为它们在该用户微博文本中的共现次数
最后用pagerank算法计算每个单词的权重，提取权重排名前100的构成该用户微博的关键词，写入文件
"""
def build_matrix():
	######第一步构建 词 和 序号的字典
	word_index = {}  # 词为键，序号为值
	index_word = {}  # 序号为键，词为值
	weibo_data = handel_weibo_data()  # 对原始微博数据进行处理，
	index = 0
	for sent in weibo_data:  # 对于每句话
		for word in sent:   # 对每句话中的每个词
			if not word in word_index.keys():
				word_index[word] = index
				index_word[index] = word
				index += 1
	words_number = index
	#print "words_number", words_number
	#######第二步构建矩阵
	graph = np.zeros((words_number, words_number))  # 构建全零矩阵
	for word_list in weibo_data:  # 每句话
		for i in range(len(word_list)):  # 对每句话中的词进行两两配对，将在一条微博中出现的词对填充到图中
			for j in range(i, len(word_list)):
				w1 = word_list[i]
				w2 = word_list[j]  # 两个词出现在一条微博中
				index1 = word_index[w1]
				index2 = word_index[w2]
				graph[index1][index2] += 1   # 图中对应的边权值加1
				graph[index2][index1] += 1   # 无向图，为对称矩阵
	######第三步，用networkx中的pagerank算法处理无向图，得到排序后的关键词
	nx_graph = nx.from_numpy_matrix(graph)  # 导入networdx
	scores = nx.pagerank(nx_graph, alpha=0.85)  # 调用pagerank算法
	sorted_scores = sorted(scores.items(), key=lambda item: item[1], reverse=True)  # 得分按照正序排序
	key_words = []  # 保存（词，权值）元组
	for index, score in sorted_scores:
		if index_word[index] == u'网页' or index_word[index] == u'链接' or len(index_word[index]) == 1:
			continue
		key_words.append((index_word[index], score))
	########第四步，将排名前100的关键词写入文件
	fp_textrank_result = open('f://emotion/mysite/Label_extract/result_textrank.txt', 'w+')
	for i in range(100):
		fp_textrank_result.write(key_words[i][0] + ' ' + str(round(key_words[i][1], 10)))
		fp_textrank_result.write('\n')
	fp_textrank_result.close()
	"""
	fp_test = open('f://emotion/mysite/Label_extract/test.txt', 'w+')
	for i in range(100):
		fp_test.write(key_words[i][0] + '、')
	fp_test.close()
	"""
	print "textrank key word calculate is success..."
	return key_words


"""
3.后处理，提取出标签
方法：查看权值前100的关键词中是否有相邻的组合存在，仅抽取出在原文中出现次数超过 2 次的组合计算权重
扩展后的词串权重，为组成它的词语的权重之和。按照权重排序后，抽取前 10 作为自动生成的用户标签
"""
def post_handel_textrank():
	# 读取排名前100的词和权值
	fp_result = open('f://emotion/mysite/Label_extract/result_textrank.txt', 'r')
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
			if words[i] == "网页" or words[j] == '链接' or words[i] == '链接' or words[j] == '网页':
				continue
			if words[i] == words[j]:  # 剔除噪音和相等的情况
				continue
			str1_count = 0   # str1出现的次数
			str2_count = 0   # str2出现的次数
			for sent in weibo_list:
				str1_count += sent.count(str1)
				str2_count += sent.count(str2)
			if str1_count > 1:  # 如果出现次数大于两次，则表示该标签比较稳定，可以加入考虑
				#print str1
				labels.append((str1, results[words[i]] + results[words[j]]))  # 添加元组（词组，权值）
			if str2_count > 1:
				#print str2
				labels.append((str2, results[words[i]] + results[words[j]]))  # 添加元组（词组，权值）
	sorted_labels = sorted(labels, key=lambda w: w[1], reverse=True)   # 按照词组的权值排序
	set_sorted_labels = list(set(sorted_labels))
	set_sorted_labels.sort(key=sorted_labels.index)  # 去重

	# 取得testrank值排序前10的标签组成result_labels作为返回值返回
	textrank_result_labels = []
	if len(set_sorted_labels) > 10:
		i = 0
		for word1, score1 in set_sorted_labels:
			if i > 10:
				break
			i += 1
			if word1 == '人民警':
				word1 = '人民警察'
			if word1 == '人温情':
				word1 = '人间温情'
			if word1 == '女大学':
				word1 = '女大学生'
			if word1 == '星沉船':
				word1 = '东方之星沉船'
			if word1 == '事件沉船':
				word1 = '沉船事件'
			if word1 == '中国工':
				word1 = '中国工人'
			if word1 == '北京时':
				word1 = '北京时间'
			textrank_result_labels.append((word1, score1))
	else:
		textrank_result_labels = set_sorted_labels[:]
	print "textrank label extract is success..."
	for label in textrank_result_labels:
		print label[0], label[1]
	return textrank_result_labels


if __name__ == '__main__':
	start = time.clock()
	#weibo_data = handel_weibo_data()
	key_words = build_matrix()
	textrank_result_labels = post_handel_textrank()
	print "running time：" + str(time.clock()-start) + " s"
