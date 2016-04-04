#coding=utf-8
import jieba
import sys
from sklearn import svm
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import cross_validation
reload(sys)
sys.setdefaultencoding('utf-8')


#根据用户输入的句子返回该句子所包含的各种词组成的向量
def Class_handel(data):

	########################################################首先读取词典转为List
	#反向词典
	f_neg_a = open('f://emotion/mysite/weibo_emotion/hownet/dic/neg_a.txt')
	f_neg_b = open('f://emotion/mysite/weibo_emotion/hownet/dic/neg_b.txt')
	f_neg_d = open('f://emotion/mysite/weibo_emotion/hownet/dic/neg_d.txt')
	f_neg_i = open('f://emotion/mysite/weibo_emotion/hownet/dic/neg_i.txt')
	f_neg_l = open('f://emotion/mysite/weibo_emotion/hownet/dic/neg_l.txt')
	f_neg_n = open('f://emotion/mysite/weibo_emotion/hownet/dic/neg_n.txt')
	f_neg_v = open('f://emotion/mysite/weibo_emotion/hownet/dic/neg_v.txt')
	f_neg_z = open('f://emotion/mysite/weibo_emotion/hownet/dic/neg_z.txt')

	#正向词典
	f_pos_a = open('f://emotion/mysite/weibo_emotion/hownet/dic/pos_a.txt')
	f_pos_b = open('f://emotion/mysite/weibo_emotion/hownet/dic/pos_a.txt')
	f_pos_d = open('f://emotion/mysite/weibo_emotion/hownet/dic/pos_d.txt')
	f_pos_i = open('f://emotion/mysite/weibo_emotion/hownet/dic/pos_i.txt')
	f_pos_l = open('f://emotion/mysite/weibo_emotion/hownet/dic/pos_l.txt')
	f_pos_n = open('f://emotion/mysite/weibo_emotion/hownet/dic/pos_n.txt')
	f_pos_v = open('f://emotion/mysite/weibo_emotion/hownet/dic/pos_v.txt')
	f_pos_z = open('f://emotion/mysite/weibo_emotion/hownet/dic/pos_v.txt')

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
	f_but = open('f://emotion/mysite/weibo_emotion/hownet/dic/but.txt')
	f_but_text = f_but.read()
	f_but.close()
	f_but_list = f_but_text.split('\n')   # 读取词库的词，编码，转为list

	##################################构造否定词列表
	f_no = open('f://emotion/mysite/weibo_emotion/hownet/dic/no.txt')
	f_no_text = f_no.read()
	f_no.close()
	f_no_list = f_no_text.split('\n')   # 读取词库的词，编码，转为list
############################################################词典构建完毕

	neg_n_count, neg_v_count, neg_a_count, neg_d_count, neg_l_count, neg_i_count = 0, 0, 0, 0, 0, 0
	pos_n_count, pos_v_count, pos_a_count, pos_d_count, pos_l_count, pos_i_count = 0, 0, 0, 0, 0, 0
	neg_b_count, neg_z_count, pos_b_count, pos_z_count = 0, 0, 0, 0
	but_count = 0   # 转折词
	no_count = 0    # 否定词

	f_seg_list = list(jieba.cut(data, cut_all=False))
	#print f_seg_list
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

	word_list = []
	word_list.append(neg_a_count)
	word_list.append(neg_b_count)
	word_list.append(neg_d_count)
	word_list.append(neg_i_count)
	word_list.append(neg_l_count)
	word_list.append(neg_n_count)
	word_list.append(neg_v_count)
	word_list.append(neg_z_count)
	word_list.append(pos_a_count)
	word_list.append(pos_b_count)
	word_list.append(pos_d_count)
	word_list.append(pos_i_count)
	word_list.append(pos_l_count)
	word_list.append(pos_n_count)
	word_list.append(pos_v_count)
	word_list.append(pos_z_count)
	word_list.append(but_count)
	word_list.append(no_count)
	return word_list   # 返回向量


#根据在datahandel.py中已经处理好的大量向量几何训练模型
def Training_model():
	#加载原始数据生成的向量集
	f = open("f://emotion/mysite/weibo_emotion/emotion_file/data_count.txt")   # 大量语料的向量组成的库
	f.readline()   # 去除首行
	data = np.loadtxt(f)
	#加载文本的分类标注
	f1 = open("f://emotion/mysite/weibo_emotion/emotion_file/data_jixing.txt")
	leibie = np.loadtxt(f1)
	f.close()
	f1.close()

	#TF-IDF处理
	transformer = TfidfTransformer()
	tfidf = transformer.fit_transform(data)
	data1 = tfidf.toarray()

	#SVM分类器分类
	clf = svm.SVC()   # class
	clf.fit(data1, leibie)    # training the svc model
	return clf


def test_data():
	#输入要测试的文字 ，例如输入“我不高兴”
	content = raw_input("input:")
	print "提取特征向量化..."
	ceshi = Class_handel(content)  # 调用Class_handel生成向量返回
	print "\n训练模型..."
	clf = Training_model()  # 调用Training_model训练模型返回
	result = clf.predict(ceshi)    # 根据模型，对自己输入的句子生成的向量进行预测
	#print result
	if result == np.array([1]):
		print "这句话是正面的"
	if result == np.array([2]):   # 二元分类
		print "这句话是反面的"

def test_file():
	f_test = open("f://emotion/mysite/weibo_crawler/chinese_weibo.txt", "r")
	f_testres = open("f://emotion/mysite/weibo_emotion/emotion_file/test_result.txt", "w")
	print "training model..."
	clf = Training_model()   # 模型
	lines = f_test.readlines()
	i = 1
	for line in lines:
		print "Handing number " + str(i) + " weibo..."
		i += 1
		line_handel = Class_handel(line)   # 生成向量返回
		#print line_handel
		line_result = clf.predict(line_handel)  # 预测
		if line_result == np.array([1]):  # 判断正负极性
			f_testres.write(line.strip())
			f_testres.write("is")
			f_testres.write(str(line_handel))
			f_testres.write("is")
			f_testres.write("正面情感 \n")
		if line_result == np.array([2]):
			f_testres.write(line.strip())
			f_testres.write("is")
			f_testres.write(str(line_handel))
			f_testres.write("is")
			f_testres.write("负面情感 \n")
	print "running success！"
	f_test.close()
	f_testres.close()

if __name__ == '__main__':
	#test_data()   # 根据用户输入测试
	test_file()   # 文本测试

