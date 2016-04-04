# -*- coding: utf-8 -*-
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import svm
from sklearn import cross_validation
from sklearn import metrics
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#加载数据向量模型
f = open("emotion_file/data_count.txt")
f.readline()   # 去掉首行
data = np.loadtxt(f)
#加载文本的分类标注
f1 = open("emotion_file/data_jixing.txt")
leibie = np.loadtxt(f1)


transformer = TfidfTransformer()
tfidf = transformer.fit_transform(data)
data1 = tfidf.toarray()

#将数据向量交叉分为训练集和测试集，5次交叉准确率即为scores
clf = svm.SVC(kernel='linear', C=1)
scores = cross_validation.cross_val_score(clf, data1, leibie, cv=5)  #5-fold cv,change metrics
print "scores", scores
f.close()
f1.close()
