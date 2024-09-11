import _thread
import datetime
import re

import nltk
from nltk import data
from nltk.corpus import stopwords

fff=''''''
for i in range(20):
    path='D:\\YUAN JC\\#1#资讯管理学院\\2021-2022    大三图书馆学（上学期）\\科研训练\\科研训练txt\\2.industry report全文txt\\'
    filepath=path+('%d' % (i+1))+'.txt'
    with open(filepath,'r',encoding='utf-8')as f:
        str=f.read()
        text= re.sub('[\x00-\x1F\x7F-\x9F]', '', str)
        ff = re.sub('\. |, |\(|\)|\n|;|\?|\"', ' ', text)
        fff=fff+ff+' '
word=fff.lower().split(' ')
#nltk.download('stopwords')
str1=stopwords.words('english')
clean_word=word[:]

start1=datetime.datetime.now()
for w in word:
   if w=='' or (w in stopwords.words('english')):
        clean_word.remove(w)
end1=datetime.datetime.now()

print(len(clean_word))
print(len(word))




#freq=nltk.FreqDist(clean_word)
#for key,val in freq.items():
#    print(key,val)
global www
www=[]
def clean(list,num,s,lock):
    if num<=31:
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
    elif num==32:
        k=320000
        end=327261
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
for i in range(33):
    lock = _thread.allocate_lock()  # 分配锁对象
    lock.acquire()  # 获取锁对象
    locks.append(lock)

start2=datetime.datetime.now()
for i in range(33):
    _thread.start_new_thread( clean, (word,i,str1,locks[i]) )


for i in range(33):
    while(locks[i].locked()):
        pass

wordlist=[]
for i in range(33):
    for a in www[i]:
        wordlist.append(a)
end2=datetime.datetime.now()
print("第二个结束，时间："+repr((end2-start2).seconds))
freq=nltk.FreqDist(wordlist)
#for key,val in freq.items():
#   print(key,val)
print(len(clean_word))
print(len(wordlist))

