# -*- coding: utf-8 -*-
__author__ = 'Bai Chenjia'

import Textrank_count
import Cluster_calc_similarity
import time
import sys
import numpy as np
from sklearn.cluster import KMeans
reload(sys)
sys.setdefaultencoding("utf-8")

"""
1.预处理
调用Textrank函数抽取排名前100的名词，存储，准备后续聚类。
"""
def pre_handel():
	key_words = Textrank_count.build_matrix()  # 调用Textrank_count中的函数返回按照权值排序的词语列表
	handel_words = key_words[:500]
	return handel_words

"""
2.kmeans聚类
"""
def kmeans_cluster():
	######### 1.将排名前100的词转为字典
	handel_words = pre_handel()   # 提取权值前100的词，（词，textrank值）
	words_number = len(handel_words)
	word_score = {}      # 词为键，textrank权值为值
	score_word = {}      # textrank权值为键，词为值
	for word, score in handel_words:
		word = word.decode('utf-8')  # 转为unicode
		word_score[word] = score
		score_word[score] = word
	index_word = {}     # 序号为键，词为值
	index = 0
	for word, score in handel_words:
		word = word.decode("utf-8")
		index_word[index] = word
		index += 1

	######### 2.构建矩阵，矩阵元素的值为两个元素的语义相似度
	sim_data = np.zeros((words_number, words_number))  # 构建全零矩阵
	for i in range(words_number):
		for j in range(words_number):
			sim_data[i][j] = Cluster_calc_similarity.cal_similarity(index_word[i], index_word[j])  # 相似度计算
		print str(i) + " row similarity count is over!"
	#for i in range(100):
	#	print sim_data[0][i]
	print "the matrix build success..."

	######## 3.k-means聚类
	"""
	# 测试效果，分多少簇最合适
	for i in range(3, 20, 1):
		clf = KMeans(n_clusters=i)
		s = clf.fit(sim_data)
		print i, clf.inertia_
	"""
	n_cluster = 10  # 簇的个数
	clf = KMeans(n_clusters=n_cluster)  # 应用聚类算法
	s = clf.fit(sim_data)
	#输出每个簇中的样本
	group_result = []
	for i in range(n_cluster):
		group_result.append([])   # 初始化
	for i in range(words_number):  # 对每个词进行循环
		num = clf.labels_[i]  # 判断每个词所属类别
		group_result[num].append(index_word[i])  # 将该词添加到类别对应的列表中

	# 构造list_group用于返回并在界面显示
	list_group = []
	for i in range(n_cluster):
		str_group = 'group' + str(i)
		str_words = ""
		for word in group_result[i]:
			str_words += word
			str_words += ' '
			str_words += '   '
		list_group.append((str_group, str_words))


	for i in range(n_cluster):        # 输出聚类结果
		print "\ngroup" + str(i) + ":"
		for word in group_result[i]:
			print word,
	print '\n'

	print "the k_means algorithm running success!"
	########4.后处理，提取出标签。
	"""
	选用簇中拥有最高 TextRank 分数的词语作为簇代表词。基于 TextRank 生成方法中同样的策略对词进行扩展
	但与代表词合并的词语必须出现在同一个聚类簇中
	"""
	#读取原始微博连成字符串
	fp_weibo = open('f://emotion/mysite/weibo_crawler/chinese_weibo.txt', 'r')
	weibo_list = []
	for content in fp_weibo.readlines():
		content = content.strip()
		weibo_list.append(content)
	fp_weibo.close()
	#抽取标签
	cluster_result_labels = []  # 存储最终的标签
	for i in range(n_cluster):
		labels = []   # 本组的标签
		max_score = max(word_score[word] for word in group_result[i])  # 本组中最大的权值
		max_word = score_word[max_score]  # 本组中权值最大的词
		for word in group_result[i]:
			str1 = word.decode('utf-8') + max_word.decode('utf-8')
			str2 = max_word.decode('utf-8') + word.decode('utf-8')  # 组成词对
			str1_count = 0   # str1出现的次数
			str2_count = 0   # str2出现的次数
			if word == max_word:
				continue
			for sent in weibo_list:
				str1_count += sent.count(str1)
				str2_count += sent.count(str2)
			if str1 == str2:  # 如果两个字符相等，则计数一个
				str2_count = 0
			if str1_count > 0:  # 如果出现次数大于两次，则表示该标签比较稳定，可以加入考虑
				labels.append((str1, word_score[word] + word_score[max_word]))  # 添加元组（词组，权值）
			if str2_count > 0:
				labels.append((str2, word_score[word] + word_score[max_word]))  # 添加元组（词组，权值）
		sorted_labels = sorted(labels, key=lambda w: w[1], reverse=True)   # 按照词组的权值排序
		if len(sorted_labels) > 0:
				cluster_result_labels.append(sorted_labels[0])  # 选取每组得分最高的
		else:
			cluster_result_labels.append((max_word, str(max_score)))
	for label in cluster_result_labels:
		print label[0], label[1]
	return list_group, cluster_result_labels



if __name__ == '__main__':
	start = time.clock()

	#预处理，调用Textrank函数抽取排名前200的名词，存储
	pre_handel()

	#2.kmeans聚类
	list_group, cluster_result_labels = kmeans_cluster()

	print "程序运行时间：" + str(time.clock() - start) + "s"
