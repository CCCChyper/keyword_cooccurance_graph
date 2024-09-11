import re

import gensim
from gensim.models import word2vec

sentence=[]
for i in range(677):
    path='D:\\YUAN JC\\#top1#资讯管理学院\\2021-2022    大三图书馆学（上学期）\\科研训练\科研训练txt\\3.smart libraties全文txt\\'
    filepath=path+('%d' % (i+1))+'.txt'
    with open(filepath,'r',encoding='utf-8')as f:
        str=f.read()
        text= re.sub('[\x00-\x1F\x7F-\x9F]', '', str)
        ff = re.sub('\. |, |\(|\)|\n', ' ', text)
        word=ff.split(' ')
        sentence.append(word)
print(sentence)

#model=gensim.models.Word2Vec(sentence,sg=1,window=5,min_count=5,negative=3,sample=0.001,hs=1)
#model.save("第一个模型")

m=gensim.models.Word2Vec.load("第一个模型")

w=m.wv.most_similar('April',topn=10)
print(w)