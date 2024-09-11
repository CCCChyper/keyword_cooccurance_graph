import string
import threading

import nltk
import numpy as np
import re

#with open('语料.txt') as f:
#    X_raw = f.readlines()


#X = [list(sentence) for sentence in X_raw]  # 拆词
#regex = re.compile(u'[\u4e00-\u9fa5]')
#X = [[word for word in sentence if regex.match(word) is not None] for sentence in X]
# X=[[word for word in sentence if word not in stops] for sentence in X] # 停词
#X = [' '.join(sentence) for sentence in X]
from nltk.corpus import stopwords


def str_clean(str):
    str2 = re.sub('[\x00-\x1F\x7F-\x9F]', '', str)
    punctuation_map = dict((ord(char), None) for char in string.punctuation)
    without_punctuation = str2.translate(punctuation_map)
    return without_punctuation

filetxt=[] #全文内容
for i in range(20):
    filename='D:\\YUAN JC\#1#资讯管理学院\\2021-2022    大三图书馆学（上学期）\\科研训练\\科研训练txt\\2.industry report全文txt\\'+('%d' % (i+1))+'.txt'
    with open(filename,'r',encoding='utf-8')as f:
        read=f.read()
        filestr=str_clean(read)
        filetxt.append(filestr)

wordlist=filetxt[1].split(' ')
X=filetxt

from sklearn.feature_extraction import text

max_n_gram = 3
count_vectorizer = text.CountVectorizer(ngram_range=[1, max_n_gram],
                                        )

count_vectorizer.fit(X)

X_cnt_vec = count_vectorizer.transform(X)

X_cnt_vec.toarray().sum(axis=0)

# 每个 feature 是什么（文本）
feature_names = count_vectorizer.get_feature_names()

# 每个feature含多少词（n-gram）
feature_len = np.array([feature_name.count(' ') + 1 for feature_name in feature_names])

# 全部语料中，每个feature出现多少次
feature_cnt = X_cnt_vec.toarray().sum(axis=0)

# 每种长度的词，在全部语料中出现多少次
feature_toal = {i: feature_cnt[feature_len == i].sum() for i in range(1, max_n_gram + 1)}
print(feature_toal)
print(len(feature_names))
print(len(feature_len))
print(len(feature_cnt))
a=0
for fc in feature_cnt:
   a=a+fc
print(a)

global res
res=[]

class myThread (threading.Thread):
    def __init__(self, threadID, name, start0, stop):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.start0= start0
        self.stop=stop
    def run(self):
        print ("开启线程： " + self.name)
        print(self.start0)
        # 获取锁，用于线程同步
        cal_pmi(self.start0,self.stop)
        # 释放锁，开启下一个线程


def cal_pmi(start,stop):
    res=[]
    for idx in range(start,stop):
        if feature_len[idx] == 1:
            continue
        feature_name_split = feature_names[idx].split(' ')
        p_x_y = feature_cnt[idx] / feature_toal[feature_len[idx]]  # 一个词出现的次数
        # p_x_y = feature_cnt[idx]
        px_multiply_py = 0
        for i in range(1, feature_len[idx]):
            part_left = ' '.join(feature_name_split[:i])
            part_right = ' '.join(feature_name_split[i:])
            idx_left = feature_names.index(part_left)
            idx_right = feature_names.index(part_right)
            if part_left in feature_names and part_right in feature_names:
                px_multiply_py_ = feature_cnt[idx_left] * feature_cnt[idx_right] / feature_toal[feature_len[idx_left]] / \
                            feature_toal[feature_len[idx_right]]
                    # px_multiply_py_ = feature_cnt[idx_left] * feature_cnt[idx_right]
                if px_multiply_py_ > px_multiply_py:
                    px_multiply_py = px_multiply_py_
        #print(idx)
        #threadLock.acquire()
        res.append([feature_names[idx], p_x_y / px_multiply_py])
        #threadLock.release()

threadLock = threading.Lock()
threads = []

for i in range(16):
    if i==16:
        resres = myThread(i, '%d' % i, i * 10000, len(feature_len)-1)
        threads.append(resres)
    else:
        resres = myThread(i,'%d'% i, i * 10000, i*10000+10000)
        threads.append(resres)


for t in threads:
    t.start()


for t in threads:
    t.join()
    print(t)



import collections

# 取上一步的结果，这里应当卡域值，但作为演示就取top20
possible_new_words = sorted(res, key=lambda x: x[1], reverse=True)[:200]


def cal_entropy(cnt):
    # 计算熵
    freq = np.array(list(cnt.values()))
    prob = freq / freq.sum()
    return -(prob * np.log2(prob)).sum()


new_word = []
for word in possible_new_words:
    regex_left = re.compile(r'[\S]* {word}'.format(word=word[0]))
    regex_right = re.compile(r'{word} [\S]*'.format(word=word[0]))
    print(word)
    # 遍历语料，找到左字和右字（用空格分割的一个基础单元，字或词或英语单词）
    cnt_left, cnt_right = collections.Counter(), collections.Counter()
    for x in X:
        cnt_left.update(collections.Counter(regex_left.findall(x)))
        cnt_right.update(collections.Counter(regex_right.findall(x)))

    left_entropy, right_entropy = cal_entropy(cnt_left), cal_entropy(cnt_right)
    if left_entropy > 1 and right_entropy > 1:
        new_word.append(word)

print(new_word)