# -*- coding: utf-8 -*-
__author__ = 'Bai Chenjia'
"""
基于哈尔滨工业大学同义词词林扩展版
计算首先构建词典，随后计算词语相似度
计算词语相似度的方法参照论文《基于同义词词林的词语相似度计算方法》
"""
import sys
import time
import math
reload(sys)
sys.setdefaultencoding("utf-8")


"""
1.对同义词词林扩展版词典进行处理
	以词———编号的形式存储，并写入文件。
	由于该词典构建速度过慢，因此在使用时直接从文件读取而不运行该函数。
	注意，该函数运行写入文件后今后不再运行。
"""
def build_word_number():
	#######第一步，首先读取原始的词典
	fp_dict = open("hit_corpus/hit_synonym.txt", 'r')
	raw_dict = []   # 原始的词典
	for content in fp_dict.readlines():
		content = content.strip()
		raw_dict.append(content)
	fp_dict.close()
	#######第二步，生成字典一（编号————词）
	number_word_dic = {}   # 编号——词 构成的字典
	for content in raw_dict:
		word_list = list(content.split(' '))  # 按空格分割，第一个元素为编号，之后的元素是词语
		number_word_dic[word_list[0]] = []  # 新增键，值列表暂时赋值为空
		for word in word_list[1:]:
			word = word.decode("utf-8")
			number_word_dic[word_list[0]].append(word)   # 逐一新增值构成一个列表
	#######第三步，生成字典二（词————编号）
	word_number_dic = {}  # 词——编号 构成的字典
	for number in number_word_dic.keys():
		for word in number_word_dic[number]:
			if word not in word_number_dic.keys():   # 如果词典还没有包含这个键（单词）
				word_number_dic[word] = []
				word_number_dic[word].append(number)   # 新建构造单词———编号的键值对
			else:                   # 如果已经包含该键则对值的列表进行添加
				#print number
				word_number_dic[word].append(number)  # 添加到以该单词为键的值列表中
	#######第三步，将生成的字典二写入文件
	fp_word_number = open('f://emotion/mysite/Label_extract/hit_corpus/word_number.txt', 'w+')
	for word in word_number_dic.keys():
		fp_word_number.write(word)
		fp_word_number.write(' ')
		for number in word_number_dic[word]:
			fp_word_number.write(number)
			fp_word_number.write(' ')
		fp_word_number.write('\n')
	fp_word_number.close()


"""
2.从文件中读取上一个函数生成的（词———编号）词典，并返回该词典
"""
def load_word_number():
	fp_dict = open('f://emotion/mysite/Label_extract/hit_corpus/word_number.txt', 'r')
	word_number_dict = {}  # 词————编号 词典
	for content in fp_dict.readlines():
		content = content.strip()
		word_list = list(content.split(' '))  # 按空格分割，第一个元素为词，之后的元素是编号
		word_number_dict[word_list[0].decode("utf-8")] = []   # 新增键，值列表暂时赋值为空
		for number in word_list[1:]:
			word_number_dict[word_list[0].decode("utf-8")].append(number)   # 逐一新增值构成一个列表
	#for number in word_number_dict[u'克']:
	#	print number
	print "build word_number dict success..."
	return word_number_dict



"""
3.对同义词词林扩展版词典进行处理
	构建（嵌套词典）并返回，与上一个词典不同，该词典构建速度非常快
"""
def build_nested_dict():
	#######第一步，读取原始词典，生成字典一（编号————词）
	fp_dict = open("f://emotion/mysite/Label_extract/hit_corpus/hit_synonym.txt", 'r')
	raw_dict = []   # 原始的词典
	for content in fp_dict.readlines():
		content = content.strip()
		raw_dict.append(content)
	fp_dict.close()
	number_word_dic = {}   # 编号——词 构成的字典
	for content in raw_dict:
		word_list = list(content.split(' '))  # 按空格分割，第一个元素为编号，之后的元素是词语
		number_word_dic[word_list[0]] = []  # 新增键，值列表暂时赋值为空
		for word in word_list[1:]:
			word = word.decode("utf-8")
			number_word_dic[word_list[0]].append(word)   # 逐一新增值构成一个列表
	######第二步，读取词典，生成嵌套词典
	nested_dict = {}  # 初始化嵌套字典
	for number in number_word_dic.keys():
		level1 = number[0]    # 第一层
		level2 = number[1]    # 第二层
		level3 = number[2:4]  # 第三层
		level4 = number[4]    # 第四层
		level5 = number[5:7]  # 第五层
		level6 = number[7]    # 第六层
		if level1 not in nested_dict.keys():  # 如果从level1开始就不存在
			nested_dict[level1] = {}  # 从第一层字典开始构建
			nested_dict[level1][level2] = {}
			nested_dict[level1][level2][level3] = {}
			nested_dict[level1][level2][level3][level4] = {}
			nested_dict[level1][level2][level3][level4][level5] = {}
			nested_dict[level1][level2][level3][level4][level5][level6] = []
			for word in number_word_dic[number]:
				nested_dict[level1][level2][level3][level4][level5][level6].append(word)  # 构建完毕
		else:           # level1已经存在，从level2开始不存在
			if level2 not in nested_dict[level1].keys():
				nested_dict[level1][level2] = {}   # 从第二层字典开始构建
				nested_dict[level1][level2][level3] = {}
				nested_dict[level1][level2][level3][level4] = {}
				nested_dict[level1][level2][level3][level4][level5] = {}
				nested_dict[level1][level2][level3][level4][level5][level6] = []
				for word in number_word_dic[number]:
					nested_dict[level1][level2][level3][level4][level5][level6].append(word)  # 构建完毕
			else:      # level1和level2已经存在，从level3开始不存在
				if level3 not in nested_dict[level1][level2].keys():
					nested_dict[level1][level2][level3] = {}   # 从第三层字典开始构建
					nested_dict[level1][level2][level3][level4] = {}
					nested_dict[level1][level2][level3][level4][level5] = {}
					nested_dict[level1][level2][level3][level4][level5][level6] = []
					for word in number_word_dic[number]:
						nested_dict[level1][level2][level3][level4][level5][level6].append(word)  # 构建完毕
				else:   # level1,level2,level3已经存在，从level4开始不存在
					if level4 not in nested_dict[level1][level2][level3].keys():
						nested_dict[level1][level2][level3][level4] = {}
						nested_dict[level1][level2][level3][level4][level5] = {}
						nested_dict[level1][level2][level3][level4][level5][level6] = []
						for word in number_word_dic[number]:
							nested_dict[level1][level2][level3][level4][level5][level6].append(word)  # 构建完毕
					else:  # level1,level2,level3,level4已经存在，从level5开始不存在
						if level5 not in nested_dict[level1][level2][level3][level4].keys():
							nested_dict[level1][level2][level3][level4][level5] = {}
							nested_dict[level1][level2][level3][level4][level5][level6] = []
							for word in number_word_dic[number]:
								nested_dict[level1][level2][level3][level4][level5][level6].append(word)  # 构建完毕
						else:  # level1,level2,level3,level4已经存在，从level6开始不存在
							if level6 not in nested_dict[level1][level2][level3][level4][level5].keys():
								nested_dict[level1][level2][level3][level4][level5][level6] = []
								for word in number_word_dic[number]:
									nested_dict[level1][level2][level3][level4][level5][level6].append(word)  # 构建完毕
							else:  # 已经存在该编号，表明是在同义词词林中同一行的单词
								for word in number_word_dic[number]:
									nested_dict[level1][level2][level3][level4][level5][level6].append(word)  # 构建完毕

	#for word in nested_dict['A']['a']['01']['B']['01']['=']:
	#	print word
	print "build nested dict success..."
	return nested_dict


"""
4.计算词语相似度
	输入是两个词，输出是两个词之间的相似度
	方法参照论文《基于同义词词林的词语相似度计算方法》
"""

#读取生成的 （词————编号） 词典，并返回该词典
word_number_dict = load_word_number()
#对同义词词林扩展版词典进行处理，构建嵌套词典并返回
nested_dict = build_nested_dict()

def cal_similarity(word1, word2):  # 注意这里word1和word2都是unicode表示形式
	###############词典构建工作结束，开始算法的主体部分
	a, b, c, d, e, f = 0.65, 0.8, 0.9, 0.96, 0.5, 0.1  # 算法所需要的参数
	similarity_result = []  # 存储各个义项计算结果的集合
	if word1 in word_number_dict.keys() and word2 in word_number_dict.keys():  # 如果同义词词林中有这两个词
		for number1 in word_number_dict[word1]:
			for number2 in word_number_dict[word2]:   # 对单词的每个义项进行计算，循环进行
				result = 0.0  # 存储本次计算的结果
				word1_level, word2_level = [], []     # 存储第一个词和第二个词的层次
				# 存储第一个单词的层次
				word1_level.append(number1[0])    # 第一层
				word1_level.append(number1[1])    # 第二层
				word1_level.append(number1[2:4])  # 第三层
				word1_level.append(number1[4])    # 第四层
				word1_level.append(number1[5:7])  # 第五层
				word1_level.append(number1[7])    # 第六层
				# 存储第二个单词的层次
				word2_level.append(number2[0])    # 第一层
				word2_level.append(number2[1])    # 第二层
				word2_level.append(number2[2:4])  # 第三层
				word2_level.append(number2[4])    # 第四层
				word2_level.append(number2[5:7])  # 第五层
				word2_level.append(number2[7])    # 第六层
				if word1_level[0] == word2_level[0]:  # 如果第一层相同
					if word1_level[1] == word2_level[1]:  # 如果第二层相同
						if word1_level[2] == word2_level[2]:  # 如果第三层相同
							if word1_level[3] == word2_level[3]:  # 如果第四层相同
								if word1_level[4] == word2_level[4]:  # 如果第五层相同
									if word1_level[5] == word2_level[5] and word1_level[5] == '=':
										result = 1.0
									elif word1_level[5] == word2_level[5] and word1_level[5] == '#':
										result = e
								else:
									n = len(nested_dict[word1_level[0]][word1_level[1]][word1_level[2]][word1_level[3]].keys())  # 第四层分支层的节点总数
									k = abs(int(word1_level[4]) - int(word2_level[4]))  # 第五层分支间的距离
									result = float(1 * 1 * 1 * 1 * d * math.cos(math.radians(n)) * (n - k + 1)/n)
							else:  # 1,2,3相同，4开始不同
								n = len(nested_dict[word1_level[0]][word1_level[1]][word1_level[2]].keys())  # 第三层分支层的节点总数
								k = abs(ord(word1_level[3]) - ord(word2_level[3]))  # 第四层分支间的距离
								result = float(1 * 1 * 1 * c * math.cos(math.radians(n)) * (n - k + 1)/n)
						else:  # 1,2相同，3开始不同
							n = len(nested_dict[word1_level[0]][word1_level[1]].keys())  # 第二层分支层的节点总数
							k = abs(int(word1_level[2]) - int(word2_level[2]))  # 第三层分支间的距离
							result = float(1 * 1 * b * math.cos(math.radians(n)) * (n - k + 1)/n)
					else:  # 1相同，2开始不同
						n = len(nested_dict[word1_level[0]].keys())  # 第一次分支层的节点总数
						k = abs(ord(word1_level[1]) - ord(word2_level[1]))  # 第二层分支间的距离
						result = float(1 * a * math.cos(math.radians(n)) * (n - k + 1)/n)
				else:  # 1开始不同
					result = float(f)
				similarity_result.append(result)   # 在结果列表中添加值
		similarity = max(similarity_result)
		#print word1 + ' ' + word2 + ' : ' + str(similarity)
		return similarity
	else:  # 同义词词林中没有该词
		similarity = '0.1'
		return similarity


# 该函数为了验收时显示词典而写，并无其他作用。
def read_hit_corpus():
	word_number_list = []
	for word in word_number_dict.keys():
		str_numbers = ""
		for number in word_number_dict[word]:
			str_numbers += str(number)
			str_numbers += ' '
		word_number_list.append((word, str_numbers))
	word_number_list = word_number_list[:1000]
	#for word, numbers in word_number_list:
	#	print word, numbers
	return word_number_list  # 只返回1000个词作为显示



if __name__ == '__main__':
	start = time.clock()

	#对同义词词林扩展版词典进行处理,以（词———编号）的形式存储，并写入文件。注意，该函数运行写入文件后今后不再运行。
	#build_word_number()

	#1.读取上一个函数生成的 （词————编号） 词典，并返回该词典
	#word_number_dict = load_word_number()

	#2.对同义词词林扩展版词典进行处理，构建嵌套词典并返回
	#nested_dict = build_nested_dict()

	#3.计算两个词语之间的词语相似度，上面计算得到的两个词典作为参数
	sim_result = cal_similarity(u'人民', u'市民')  # 测试：人民，国民，群众，党群，良民，同志，市民
	print "语义相似度：", sim_result

	#read_hit_corpus()

	print "程序运行时间：" + str(time.clock() - start) + "s"

