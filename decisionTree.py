import operator
from math import log
import numpy as np
import pandas as pd
import pickle

'''dataSet是pd.DataFrame'''

def calShannonEnt(dataSet):
    '''计算熵'''
    numEntries=len(dataSet)
    labelCounts=dict(dataSet.iloc[:,-1].value_counts())
    shannonEnt=0.0
    for key in labelCounts:
        prob=float(labelCounts[key]/numEntries)
        shannonEnt-=prob*log(prob,2)
    return shannonEnt

def splitDataSet(dataSet,axis,value):
    '''根据特征以及特征值，筛选子数据'''
    retDataSet=pd.DataFrame()
    retDataSet=dataSet[dataSet.loc[:,axis]==value].drop(columns=axis)
    return retDataSet

def chooseBestFeatureToSplit(dataSet):
    '''通过计算数据的信息增益率，返回最佳的特征'''
    numfeatures=len(dataSet.iloc[0,:])-1
    features=dataSet.columns
    baseEntropy=calShannonEnt(dataSet)
    bestInfoGain=0.0
    bestFeature=features[0]
    for feature in features:
        values=dataSet.loc[:,feature].unique()
        newEntropy=0
        for value in values:
            subDataSet=splitDataSet(dataSet,feature,value)
            prob=float(len(subDataSet)/len(dataSet))
            newEntropy+=prob * calShannonEnt(subDataSet)
            # print(newEntropy)
        infoGain=baseEntropy-newEntropy
        infoGainRate=infoGain/baseEntropy if baseEntropy !=0 else 0
        if (infoGainRate>bestInfoGain):
            bestInfoGain=infoGainRate
            bestFeature=feature
        return bestFeature

# def majorityCnt(classList):
#     classCount={}
#     for vote in classList:
#         classCount[vote]=classCount.get(vote,0)+1
#     sortedClassCount=sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
#     return sortedClassCount[0][0]

def createTree(dataSet):
    classList=dataSet.iloc[:,-1].value_counts(ascending=False)
    cls=classList.index[0]
    if classList[0]== len(dataSet) or len(dataSet.columns)==1 :
        return cls
    bestFeature=chooseBestFeatureToSplit(dataSet)
    myTree={bestFeature:{}}
    univals=dataSet.loc[:,bestFeature].unique()
    for val in univals:
        subDataSet=splitDataSet(dataSet,bestFeature,val)
        myTree[bestFeature][val]=createTree(subDataSet)
    return myTree

def classify(inputTree,testData):
    feature=list(inputTree)[0]
    classLabel=inputTree[feature][testData[feature]]
    if isinstance(classLabel, dict):
        testData=testData.drop(feature)
        classLabel=classify(classLabel,testData)
    return classLabel

if __name__ == "__main__":
    dataSet =pd.DataFrame([[1, 1,"男" ,'yes'],
           [1, 1, "男" ,'yes'],
           [1, 0, "女" ,'no'],
           [0, 1, "女" ,'yes'],
           [0, 1, "男" ,'no']],columns=["color","age","sex","label"])
    inputTree=createTree(dataSet)




