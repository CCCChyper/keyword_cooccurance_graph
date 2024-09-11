import _thread
import csv
import datetime
import operator
import re

import nltk
from nltk import data, WordNetLemmatizer
from nltk.corpus import stopwords
nltk.download()
fff=''''''
for i in range(20):
    path='D:\\YUAN JC\\#1#资讯管理学院\\2021-2022    大三图书馆学（上学期）\\科研训练\科研训练txt\\2.industry report全文txt\\'
    filepath=path+('%d' % (i+1))+'.txt'
    with open(filepath,'r',encoding='utf-8')as f:
        str=f.read()
        text= re.sub('[\x00-\x1F\x7F-\x9F]', '', str)
        ff = re.sub('\.|, |\(|\)|\n|;|\?|\|--"', ' ', text)
        fff=fff+ff+' '
word=fff.lower().split(' ')
#nltk.download('stopwords')
str1=stopwords.words('english')
print(len(word))
global www
www=[]
def clean(list,num,s,lock):

    if num<=11:
        k=10000*num
        w=[]
        for n in range(k,k+10000):
            w.append(list[n])
        cw=w[:]
        for c in w:
            if c == '' or (c in s):
                cw.remove(c)
        www.append(cw)
        lock.release()
    elif num==12:
        k=120000
        end=120242
        w = []
        for n in range(k, end):
            w.append(list[n])
        cw = w[:]
        for c in w:
            if c == '' or (c in s):
                cw.remove(c)
        www.append(cw)
        lock.release()
locks=[]
for i in range(13):
    lock = _thread.allocate_lock()  # 分配锁对象
    lock.acquire()  # 获取锁对象
    locks.append(lock)

start2=datetime.datetime.now()
for i in range(13):
    _thread.start_new_thread( clean, (word,i,str1,locks[i]) )


for i in range(13):
    while(locks[i].locked()):
        pass

word0=[]
for i in range(13):
    for a in www[i]:
        word0.append(a)
end2=datetime.datetime.now()

print(len(word0))

tag=nltk.pos_tag(word0)
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return nltk.corpus.wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return nltk.corpus.wordnet.VERB
    elif treebank_tag.startswith('N'):
        return nltk.corpus.wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return nltk.corpus.wordnet.ADV
lmtzr=WordNetLemmatizer()
wordlist=[]
for t in tag:
    pos=get_wordnet_pos(t[1])
    try:
        new_word=lmtzr.lemmatize(t[0],pos)
        wordlist.append(new_word)
    except:
        pass

print(len(wordlist))



#freq=nltk.FreqDist(clean_word)
#for key,val in freq.items():
#    print(key,val)


freq=nltk.FreqDist(wordlist)
finalList=[]
for key,val in sorted(freq.items(),key=operator.itemgetter(1),reverse=True):
    list=[]
    list.append(key)
    list.append(repr(val))
    finalList.append(list)

with open('D:\\wordcount.csv','w',newline='',encoding='utf-8-sig')as csv_file:
    writer=csv.writer(csv_file)
    for row in finalList:
        writer.writerow(row)
print(repr((end2-start2).seconds))
print(finalList)

