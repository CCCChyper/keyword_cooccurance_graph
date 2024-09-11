import csv
import re
import string
import sklearn
import nltk
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

#nltk.download('punkt')
punctuation_map=dict((ord(char),None) for char in string.punctuation)
text=[]
wordnum=[]
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
lmtzr=WordNetLemmatizer()


for i in range(677):
    path='D:\\YUAN JC\\#top1#资讯管理学院\\2021-2022    大三图书馆学（上学期）\\科研训练\科研训练txt\\3.smart libraties全文txt\\'
    filepath=path+('%d' % (i+1))+'.txt'
    with open(filepath,'r',encoding='utf-8')as f:
        str=f.read()
        str2= re.sub('[\x00-\x1F\x7F-\x9F]', '', str)
        without_punctuation=str2.translate(punctuation_map)
        lower_text = without_punctuation.lower()
        tokens=nltk.word_tokenize(lower_text)
        tag = nltk.pos_tag(tokens)
        wordlist = []
        for t in tag:
            pos = get_wordnet_pos(t[1])
            try:
                new_word = lmtzr.lemmatize(t[0], pos)
                wordlist.append(new_word)
            except:
                pass
        without_stopwords=[w for w in wordlist if not w in stopw]
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
    L=L[:20]
    print(u"-------这里输出第", j, u"类文本tf-idf权重前10的词语------")
    print(L)
def sortDictValue(dict, is_reverse, num):
    '''
    将字典按照value排序
    :param dict: 待排序的字典
    :param is_reverse: 是否按照倒序排序
    :return s: 符合csv逗号分隔格式的字符串
    :param num: 筛选次数
    '''
    # 对字典的值进行倒序排序,items()将字典的每个键值对转化为一个元组,key输入的是函数,item[1]表示元组的第二个元素,reverse为真表示倒序
    tups = sorted(dict.items(), key=lambda item: item[1], reverse=is_reverse)
    s = ''
    for tup in tups:  # 合并成csv需要的逗号分隔格式
        if tup[1]>num:
            s = s + tup[0] + ',' + repr(tup[1]) + '\n'
    return s
def build_matrix(co_words_list, is_reverse):
    '''
    根据共同列表,构建共现矩阵(存储到字典中),并将该字典按照权值排序
    :param co_words_list: 共同列表
    :param is_reverse: 排序是否倒序
    :return node_str: 三元组形式的节点字符串(且符合csv逗号分隔格式)
    :return edge_str: 三元组形式的边字符串(且符合csv逗号分隔格式)
    '''
    node_dict = {}  # 节点字典,包含节点名+节点权值(频数)
    edge_dict = {}  # 边字典,包含起点+目标点+边权值(频数)
    # 第1层循环,遍历整表的每行信息
    for row_words in co_words_list:
        L = sorted(row_words.items(), key=lambda item: item[1], reverse=True)
        L = L[:10]
        keyrow = ''
        for l in L:
            keyrow = keyrow + l[0] + ' '
        row_words_list =keyrow.strip().split(' ') # 依据','分割每行,存储到列表中
        # 第2层循环
        for index, pre_wo in enumerate(row_words_list): # 使用enumerate()以获取遍历次数index
            # 统计单个词出现的频次
            if pre_wo not in node_dict:
                node_dict[pre_wo] = 1
            else:
                node_dict[pre_wo] += 1
            # 若遍历到倒数第一个元素,则无需记录关系,结束循环即可
            if pre_wo == row_words_list[-1]:
                break
            connect_list = row_words_list[index+1:]
            # 第3层循环,遍历当前行词后面所有的词,以统计两两词出现的频次
            for next_wo in connect_list:
                A, B = pre_wo, next_wo
                # 固定两两词的顺序
                # 仅计算上半个矩阵
                if A==B:
                    continue
                if A>B:
                    A, B = B, A
                key = A+','+B  # 格式化为逗号分隔A,B形式,作为字典的键
                # 若该关系不在字典中,则初始化为1,表示词间的共同出现次数
                if key not in edge_dict:
                    edge_dict[key] = 1
                else:
                    edge_dict[key] += 1
    # 对得到的字典按照value进行排序
    node_str = sortDictValue(node_dict, is_reverse,1)  # 节点
    edge_str = sortDictValue(edge_dict, is_reverse,)   # 边
    return node_str, edge_str



node_str, edge_str = build_matrix(dictlist, is_reverse=True)

with open('D:\\YUAN JC\#top1#资讯管理学院\\2021-2022    大三图书馆学（上学期）\\科研训练\\node3.csv','w',encoding='utf-8-sig')as csv:
    csv.write("Label,weight\r")
    csv.write(node_str)

with open('D:\\YUAN JC\#top1#资讯管理学院\\2021-2022    大三图书馆学（上学期）\\科研训练\\edge3.csv','w',encoding='utf-8-sig')as csv:
    csv.write("Source,Target,Weight\r")
    csv.write(edge_str)

