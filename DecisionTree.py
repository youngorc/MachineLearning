#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@Time    : 2024/6/26 22:17
@Author  : YourName
@File    : DecisionTree.py
@Desc    : 
"""


import numpy as np
import math
import os
import pandas as pd
pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

def create_DataSet():
    """
    Desc:
        创建数据集
    Args:
        无需传入参数
    Returns:
        返回数据集和对应的label标签
    """
    # dataSet 前两列是特征，最后一列对应的是每条数据对应的分类标签
    dataSet = [[1, 1, 'yes'],
               [1, 1, 'yes'],
               [1, 0, 'no'],
               [0, 1, 'no'],
               [0, 1, 'no']]
    df = pd.DataFrame(columns=['nosurfing','flippers','Labels'],data=dataSet)
    # dataSet = [['yes'],
    #         ['yes'],
    #         ['no'],
    #         ['no'],
    #         ['no']]
    # labels  露出水面   脚蹼，注意: 这里的labels是写的 dataSet 中特征的含义，并不是对应的分类标签或者说目标变量
    labels = ['no surfacing', 'flippers']
    # 返回
    return df, labels


def load_lenses_data():
    tDir = r'E:\机器学习及数据分析\机器学习\机器学习实战\machinelearninginaction3x-master\Ch03'
    os.chdir(tDir)
    file = 'lenses.txt'
    with open(file) as fp:
        contentTmp = fp.readlines()
    content = [t.strip().split("\t") for t in contentTmp]
    columns =  ['age', 'prescript', 'astigmatic', 'tearRate','Labels']
    df = pd.DataFrame(content,columns=columns)
    labels = df.iloc[:,-1].unique().tolist()
    return df,labels


def cal_shannon_ent(dataSet):
    num = len(dataSet)
    shannonEnt = 0.0
    labelCounts = {}
    for feature in dataSet.iloc[:,-1]:
        currentLabel = feature
        if currentLabel not in labelCounts:
            labelCounts[currentLabel] = 1
        else:
            labelCounts[currentLabel] += 1
    for label in labelCounts:
        prob = float(labelCounts[label]/num)
        shannonEnt += -prob * math.log(prob,2)
    return shannonEnt



def split_DataSet(dataSet, column, value):
    colTmp = [col for col in dataSet.columns if col!=column]
    retDataSet = dataSet.loc[dataSet[column]==value,colTmp]
    return retDataSet

def choose_best_feature_to_split(dataSet):
    shannonEnt = cal_shannon_ent(dataSet)
    attributes = [col for col in dataSet.columns.to_list()[:-1]]
    attrSE = {}
    for attribute in attributes:
        subSE = 0
        values = dataSet[attribute].unique().tolist()
        for value in values:
            retDataSet = split_DataSet(dataSet,attribute,value)
            subPro = len(retDataSet)/len(dataSet)
            retSE = cal_shannon_ent(retDataSet)
            subSE = subSE + subPro*retSE
        SEGain = subSE - shannonEnt
        attrSE[attribute] = SEGain
    bestAtt = sorted(attrSE.items(),key=lambda x:x[1])[0][0]
    attValues = dataSet[bestAtt].unique().tolist()
    return bestAtt,attValues

def create_tree(dataSet):
    result = {}
    bestFea, feaValues = choose_best_feature_to_split(dataSet)
    for value in feaValues:
        colTmp = [col for col in dataSet.columns if col != bestFea]
        dataTmp = dataSet.loc[dataSet[bestFea]==value,colTmp]
        keyName = "".join([bestFea, "(", str(value), ")"])
        if len(dataTmp.iloc[:,-1].value_counts()) == 1 or len(dataTmp.columns) == 1:
            result[keyName] = dataTmp.iloc[:,-1].value_counts().index[0]
        else:
            subDataSet = split_DataSet(dataSet,bestFea,value)
            result[keyName] = create_tree(subDataSet)
    return result




def test_data_handle(data):
    columns = data.columns.tolist()
    data['tmp'] = ''
    for column in columns:
        data[column] = data[column].apply(lambda x:"".join([column, "(", str(x), ")"]))
        data['tmp'] = data[['tmp',column]].apply(lambda x:";".join([x['tmp'],x[column]]),axis=1)
    data['tmp'] = data['tmp'].str.split(";").str[1:]
    data['Labels'] = data['tmp'].apply(lambda x:get_test_label(x,tree2))


def get_test_label(x,tree):
    for y in x:
        if y in tree:
            result = tree[y]
            if isinstance(result,str):
                return result
            else:
                x = [i for i in x if i!=y]
                tree = tree[y]
                result = get_test_label(x,tree)
                return result



if __name__ =="__main__":
    dataSet,labels = create_DataSet()
    tree1 = create_tree(dataSet)
    print(tree1)
    print("test 2")
    dataSet2,labels2 = load_lenses_data()
    tree2 = create_tree(dataSet2)
    print(tree2)

