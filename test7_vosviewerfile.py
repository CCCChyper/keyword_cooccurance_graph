import re
import string

import matplotlib.pyplot as plt
import nltk
import wordcloud
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords

text=''''''
s=nltk.stem.SnowballStemmer('english')
stopw=stopwords.words('english')


def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return nltk.corpus.wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return nltk.corpus.wordnet.VERB
    elif treebank_tag.startswith('N'):
        return nltk.corpus.wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return nltk.corpus.wordnet.ADV
punctuation_map = dict((ord(char), None) for char in string.punctuation)
lmtzr=WordNetLemmatizer()
for j in range(171):
    k='%d' % (j+1)
    file='D:\\YUAN JC\\#top1#资讯管理学院\\2021-2022    大三图书馆学（上学期）\\科研训练\科研训练txt\\4.system librarian全文txt\\'+k+'.txt'
    with open(file,'r',encoding='utf-8')as r:
        str=r.read()
    str2 = re.sub('[\x00-\x1F\x7F-\x9F]', '', str)
    without_punctuation = str2.translate(punctuation_map)
    lower_text = without_punctuation.lower()
    tokens = nltk.word_tokenize(lower_text)
    tag = nltk.pos_tag(tokens)
    wordlist = []
    for t in tag:
        pos = get_wordnet_pos(t[1])
        try:
            new_word = lmtzr.lemmatize(t[0], pos)
            wordlist.append(new_word)
        except:
            pass
    without_stopwords = [w for w in wordlist if not w in stopw]
    tt = ' '.join(without_stopwords)
    text=text+tt+'\n'

with open('C:\\Users\\yjc_2\\Desktop\\vosviewerfile.txt','w',encoding='utf-8')as f:
    f.write(text)