#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
@Time    : 2021/11/19 0019 9:30
@Author  : youngorc
@FileName: Kmeans.py
@Software: PyCharm
@GitHub:https://github.com/youngorc
'''

import os
import pandas as pd
import numpy as np
import random




def loadData(file):
    df=pd.read_csv(open(file),sep="\t",names=["col1","col2"])
    return np.array(df)

def distCal(vecRow,centroid):
    return ((vecRow-centroid)**2).sum()

def randCentChoose(vec,k):
    vecIndex=range(len(vec))
    randIndex=random.sample(vecIndex,k)
    return vec[randIndex]

def kMeans(vec,k):
    m=len(vec)
    centroid=randCentChoose(vec,k)
    distVec=np.zeros(shape=(m,k))
    minIdx=np.zeros(m)
    centroidChanged=True
    while centroidChanged:
        for i in range(m):
            for j in range(k):
                distVec[i,j]=distCal(vec[i],centroid[j])
        minCentroidIdx=distVec.argmin(axis=1)
        for cent in range(k):
            centroid[cent]=vec[minCentroidIdx==cent].mean(axis=0)
        if (minIdx==minCentroidIdx).all():
            centroidChanged=False
        else:
            minIdx=minCentroidIdx
            centroidChanged=True
    return centroid,minCentroidIdx

if __name__ == "__main__":
    file = r'G:\机器学习\机器学习实战\machinelearninginaction3x-master\Ch10\testSet.txt'
    vec=loadData(file)
    centroid,minCentroidIdx=kMeans(vec,3)