#coding:utf-8
__author__ = "guoxingyu"  

import numpy 
import os  
import sys
import copy  
from sklearn import feature_extraction  
from sklearn.feature_extraction.text import TfidfTransformer  
from sklearn.feature_extraction.text import CountVectorizer

if __name__ == "__main__":
	# 读取新闻内容 
	newsDict = {} # 存放新闻id映射
	newsfile = open("./newsInfo")
	lines = newsfile.readlines()
	corpus = []
	m = 0
	for line in lines:
		if line == '\n':
			pass
		else:
			line = line.strip()
			corpus.append(line.split("/")[1])
			newsDict[m] = line.split("/")[0]
			m += 1
	newsNum = m

	# 读取用户分词信息
	userDict = {} # 存放用户已经读过的文章id
	userName =[]  # 存放用户id

	userfile = open('./userInfo','r')
	lines = userfile.readlines()
	k = 0 
	for line in lines:
		if line == '\n':
			pass
		else:
			line = line.strip()
			corpus.append(line.split("/")[1])
			userHaveReadedNews = list(line.split("/")[2].split('-'))
			userName.append(line.split("/")[0])
			userDict[str(userName[k])] = userHaveReadedNews
			k += 1
	userNum = k

	# 计算tf-idf
	vectorizer = CountVectorizer()
	transformer = TfidfTransformer()
	tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
	word = vectorizer.get_feature_names()
	weight = tfidf.toarray()


	# for i in range(len(weight)):
	# 	print u"======这里输出第",i,u"类文本的词语tf-idf权重======="
	# 	for j in range(len(word)):
	# 		print word[j],weight[i][j]

	# SimMaxtrix = (tfidf * tfidf.T).A
	# print SimMaxtrix[1,2] # 第二篇和第三篇文章的关系
	# print SimMaxtrix


	#计算相似度,完成推荐
	SimMaxtrix = (tfidf * tfidf.T).A
	with open("newsrecommend.txt","w") as f:
		for i in range(newsNum, newsNum + userNum):
			recommendDict = {}
			result = userName[i - newsNum] + ","
			for j in range(newsNum):
				if newsDict[j] in userDict[userName[i - newsNum]]:
					pass
				else:
					recommendDict[newsDict[j]] = SimMaxtrix[i][j]
			recommendlist = sorted(recommendDict.items(), key = lambda item : item[1], reverse = True)
			for k in range(10):
				result += recommendlist[k][0]+'='+str(recommendlist[k][1])[0:4]+" "
			f.write(result+'\n')
	f.close()

	print "newsrecommend have done"


	## 方法二
	# userfile = open('./user/000000_0','r')
	# lines = userfile.readlines()
	# for line in lines:
	# 	if line == '\n':
	# 		pass
	# 	else:
	# 		userDict = {}
	# 		newcorpus = copy.deepcopy(corpus)
	# 		line = line.strip()
	# 		newcorpus.append(line.split("/")[1])
	# 		userHaveReadedNews = list(line.split("/")[2].split('-'))
	# 		userName = line.split("/")[0]
	# 		userDict[str(userName)] = userHaveReadedNews
	# 		userNum = 1

	# 		vectorizer = CountVectorizer()
	# 		transformer = TfidfTransformer()
	# 		tfidf = transformer.fit_transform(vectorizer.fit_transform(newcorpus))
	# 		word = vectorizer.get_feature_names()
	# 		weight = tfidf.toarray()

	# 		SimMaxtrix = (tfidf * tfidf.T).A
	# 		with open("newsrecommend.txt","a") as f:
	# 			for i in range(newsNum, newsNum + userNum):
	# 				recommendDict = {}
	# 				result = userName + ","
	# 				for j in range(newsNum):
	# 					if newsDict[j] in userDict[userName]:
	# 						pass
	# 					else:
	# 						recommendDict[newsDict[j]] = SimMaxtrix[i][j]
	# 				recommendlist = sorted(recommendDict.items(), key = lambda item : item[1], reverse = True)
	# 				for k in range(5):
	# 					result += recommendlist[k][0]+'='+str(recommendlist[k][1])[0:4]+" "
	# 				f.write(result+'\n')
	# 		f.close()







