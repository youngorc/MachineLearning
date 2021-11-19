import numpy as np

def load_data_set():
    """
    创建数据集,都是假的 fake data set
    :return: 单词列表posting_list, 所属类别class_vec
    """
    posting_list = [
        ['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
        ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
        ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
        ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
        ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
        ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    class_vec = [0, 1, 0, 1, 0, 1]  # 1 is 侮辱性的文字, 0 is not
    return posting_list, class_vec

def create_vocab_list(data_set):
    vocab_list=set()
    for words in data_set:
        vocab_list = vocab_list | set(words)
    return list(vocab_list)

def set_2_vec(vocab_list,input_list):
    result=[0] * len(vocab_list)
    for word in vocab_list:
        if word in input_list:
            result[vocab_list.index(word)]=1
    return result

def trainnb(train_mat,train_category):
    n=len(train_mat)
    m=len(train_mat[0])
    pos_abusive=np.sum(train_category)/n
    p0num=np.ones(m)
    p1num=np.ones(m)
    p0num_all=2.0
    p1num_all=2.0
    for i in range(n):
        if train_category[i]==1:
            p1num+=train_mat[i]
            p1num_all+=np.sum(train_mat[i])
        else:
            p0num+=train_mat[i]
            p0num_all+=np.sum(train_mat[i])
    p0vec=np.log(p0num/p0num_all)
    p1vec=np.log(p1num/p1num_all)
    return p0vec,p1vec,pos_abusive

def classifyNB(vec2classify,p0vec,p1vec,pos_abusive):
    p1=np.sum(vec2classify*p1vec) + np.log(pos_abusive)
    p0=np.sum(vec2classify*p0vec) + np.log(1-pos_abusive)
    if p1>p0:
        return 1
    else:
        return 0


