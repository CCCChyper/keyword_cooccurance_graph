import re
import string
import sklearn
import nltk
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

#nltk.download('punkt')
punctuation_map=dict((ord(char),None) for char in string.punctuation)
text=[]
wordnum=[]
s=nltk.stem.SnowballStemmer('english')
stopw=stopwords.words('english')
for i in range(20):
    path='D:\\YUAN JC\\#1#资讯管理学院\\2021-2022    大三图书馆学（上学期）\\科研训练\科研训练txt\\2.industry report全文txt\\'
    filepath=path+('%d' % (i+1))+'.txt'
    with open(filepath,'r',encoding='utf-8')as f:
        str=f.read()
        str2= re.sub('[\x00-\x1F\x7F-\x9F]', '', str)
        without_punctuation=str2.translate(punctuation_map)
        lower_text = without_punctuation.lower()
        tokens=nltk.word_tokenize(lower_text)
        without_stopwords=[w for w in tokens if not w in stopw]
        wordnum.append(len(without_stopwords))
        tt=' '.join(without_stopwords)
        text.append(tt)

vectorizer=CountVectorizer()
transformer=TfidfTransformer(norm=None,smooth_idf=False)
X=vectorizer.fit_transform(text)
tfidf=transformer.fit_transform(X)


word=vectorizer.get_feature_names()
weight=tfidf.toarray()

dictlist=[]
for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
   # print(u"-------这里输出第", i, u"类文本的词语tf-idf权重------")
    worddict = dict()
    for j in range(len(word)):
           worddict[word[j]]=(weight[i][j])/wordnum[i]
    dictlist.append(worddict)

j=0
for dl in dictlist:
    j+=1
    L=sorted(dl.items(),key=lambda item:item[1],reverse=True)
    L=L[:15]
    print(u"-------这里输出第", j, u"类文本tf-idf权重前10的词语------")
    print(L)

clf=KMeans(n_clusters=10)
a=clf.fit(weight)

print(clf.cluster_centers_)
# 每个样本所属的簇
print(clf.labels_)
i = 1
while i <= len(clf.labels_):
    print(i, clf.labels_[i - 1])
    i = i + 1

# 用来评估簇的个数是否合适，距离越小说明簇分的越好，选取临界点的簇个数
print(clf.inertia_)

print(len(word))