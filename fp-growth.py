import itertools
import argparse
import pandas as pd
import json

'''
FP-Growth FP means frequent pattern
the FP-Growth algorithm
Author:youngorc
'''

class treeNode:
    def __init__(self,namevalue,numOccur,parentNode):
        self.name=namevalue
        self.count=numOccur
        self.nodeLink=None
        self.parent=parentNode
        self.children={}

    def inc(self,numOccur):
        self.count+=numOccur

    def disp(self,ind=2):
        print(" "*ind,self.name," ",self.count)
        for child in self.children.values():
            child.disp(ind+2)

def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        if frozenset(trans) not in retDict.keys():
            retDict[frozenset(trans)] = 1
        else:
            retDict[frozenset(trans)] += 1
    return retDict


def createTree(dataSet,minSup=1):
    headerTable={}
    for trans,count in dataSet.items():
        for item in trans:
            headerTable[item]=headerTable.get(item,0)+dataSet[trans]

    for k in list(headerTable.keys()):
        headerTable[k]=[headerTable[k],None]
        if headerTable[k][0] < minSup:
            del(headerTable[k])

    freqItemSet=set(headerTable.keys())

    if len(freqItemSet) == 0:
        return None,None

    retTree=treeNode("Null Set",1,None)
    for trans,count in dataSet.items():
        localD={}
        for data in trans:
            if data in freqItemSet:
                localD[data]=headerTable[data][0]
        if len(localD)>0:
            orderItems=[v[0] for v in sorted(localD.items(),key=lambda x:x[1],reverse=True)]
            updateTree(orderItems,retTree,headerTable,count)
    return retTree,headerTable

def updateTree(orderItems,retTree,headerTable,count):
    node = orderItems[0]
    if node not in retTree.children:
        retTree.children[node]=treeNode(node,count,retTree)
        if headerTable[node][1] == None:
            headerTable[node][1] = retTree.children[node]
        else:
            updateHeader(headerTable[node][1],retTree.children[node])
    else:
        retTree.children[node].inc(count)

    if len(orderItems)>1:
        updateTree(orderItems[1:],retTree.children[node],headerTable,count)

def updateHeader(srcNode,targetNode):
    while srcNode.nodeLink != None:
        srcNode=srcNode.nodeLink
    srcNode.nodeLink=targetNode

def loadSimpDat():
    simpDat = [['h', 'r', 'p', 'z', 'j'],
               ['s', 'z', 'u', 'v', 't', 'w', 'x', 'y'],
               ['z'],
               ['s', 'r', 'o', 'x', 'n'],
               ['r', 'x', 'n', 'o', 's'],
               ['r', 'p', 'z', 't', 'x', 'y', 'q'],
               ['s', 'z', 'e', 'm', 't', 'x', 'y', 'q']]
    return simpDat


def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        if frozenset(trans) not in retDict.keys():
            retDict[frozenset(trans)] = 1
        else:
            retDict[frozenset(trans)] += 1
    return retDict

def ascendTree(leafNode,prefixPath):
    if leafNode.parent is not None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent,prefixPath)

def findPrefixPath(basePat,treeNode):
    condPats={}
    while treeNode is not None:
        prefixPath=[]
        ascendTree(treeNode,prefixPath)
        if len(prefixPath)>=1:
            condPats[frozenset(prefixPath)]=condPats.get(frozenset(prefixPath),0)+treeNode.count
        treeNode=treeNode.nodeLink
    return condPats

def countSet(condPattBases,minSup,basePat):
    freqList={}
    result = {}
    for trans,count in condPattBases.items():
        for data in trans:
            freqList[data] = freqList.get(data,0)+count
    freqList=dict(sorted(freqList.items(),key=lambda x:x[1],reverse=True))

    for k in list(freqList.keys()):
        if freqList[k]<minSup:
            del(freqList[k])

    result[basePat] = freqList[basePat]
    ln=len(freqList)
    if ln==1:
        return result
    else:
        for eleNum in range(2,ln+1):
            tmp = {}
            iter=list(itertools.combinations(freqList,eleNum))
            for ele in iter:
                for key in condPattBases.keys():
                    if set(key)>=set(ele):
                        tmp[ele]=tmp.get(ele,0)+condPattBases[key]
                    else:
                        tmp[ele]=tmp.get(ele,0)+0
                if tmp[ele]<minSup:
                    del(tmp[ele])
                else:
                    result[ele]=tmp[ele]
    return result


def mineTree(headerTable,minSup):
    bigL = [v[0] for v in sorted(headerTable.items(),key=lambda p: p[1][0],reverse=True)]
    result={}
    for basePat in bigL:
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        cSet=countSet(condPattBases,minSup,basePat)
        # if cSet == {}:
        #     pass
        # else:
        print("输出频繁项集:",cSet)
        for key in cSet:
            result[key] = cSet[key]
    return sorted(result.items(),key=lambda x:x[1],reverse=True)


# def findData(target,result):
#     output={}
#     for i in result:
#         if target in i:
#             output[i]=result[i]
#     return output


# def main(dataSet,minSup,bigL=[]):
#     '''
#
#     :param minSup: 最小支持度，在所有数据中希望元素出现的最低的频次
#     :param dataSet: 需要提取的原始数据，数据格式为list:[[list1],[list2],[list3]]
#     :param bigL: 需要查找的元素列表，可自行制定元素列表，如：['a','b']，为空即dataSet提取后按照支持度从小到大排列组成list，
#     :return: 字典格式，字典的keys为需要查找的元素列表，字典的values值为字典，其中的key为频繁项集，value为频繁项集与查找元素组成的集合在原始数据中出现的频次。
#             如{'s': {'x': 3, 'z': 2, ('x', 'z'): 2}} 则s为查找的元素，[s,x]在原始数据中出现频次为3，[s,z]在原始数据中出现频次为2，[s,x,z]在原始数据中出现频次为2。
#
#     '''
#     initSet=createInitSet(dataSet)
#     myFPtree,headerTable=createTree(initSet,minSup)
#     myFPtree.disp()
#     result=mineTree(headerTable,minSup,bigL)
#     return result


def loadExcelData(file,sep=" "):
    df=pd.read_excel(file)
    df_tmp=df.iloc[:,0].apply(lambda x:x.split(sep))
    df_list=df_tmp.tolist()
    return df_list



if __name__ == "__main__":
    #     :param minSup: 最小支持度，在所有数据中希望元素出现的最低的频次
    #     :param dataSet: 需要提取的原始数据，数据格式为list:[[list1],[list2],[list3]]
    #     :param bigL: 需要查找的元素列表，可自行制定元素列表，如：['a','b']，为空即dataSet提取后按照支持度从小到大排列组成list，
    #     :return: 字典格式，字典的keys为需要查找的元素列表，字典的values值为字典，其中的key为频繁项集，value为频繁项集与查找元素组成的集合在原始数据中出现的频次。
    #             如{'s': {'x': 3, 'z': 2, ('x', 'z'): 2}} 则s为查找的元素，[s,x]在原始数据中出现频次为3，[s,z]在原始数据中出现频次为2，[s,x,z]在原始数据中出现频次为2。
    file=r'F:\《机器学习实战》完整资源\test\test.xlsx'
    minSup=7
    dataSet=loadExcelData(file)
    # dataSet = loadSimpDat()
    initSet=createInitSet(dataSet)
    myFPtree,headerTable=createTree(initSet,minSup)
    myFPtree.disp()
    result=mineTree(headerTable,minSup)
    # with open('test.json','w',encoding="utf-8") as f:
    #     json.dump(str(result),f,ensure_ascii=False)
    f=open('test.txt','a',encoding="utf-8")
    for r in result:
        f.write(str(r)+'\n')
    f.close()