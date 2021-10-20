import numpy as np
import operator
import os
import pandas as pd

def createDataSet():
    group=np.array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels=["A","A","B","B"]
    return group,labels

def classify0(inX,dataSet,labels,k):
    distances=(((inX-dataSet)**2).sum(axis=1))**0.5
    sortedDis=distances.argsort()
    classCount={}
    for i in range(k):
        voteLabel=labels[sortedDis[i]]
        classCount[voteLabel]=classCount.get(voteLabel,0)+1
    sortedClassCount=sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]

def file2mat(filename):
    df = pd.read_csv(open(filename), sep="\t",
                     header=None)
    returnMat=np.array(df.iloc[:,:3])
    classLabelVector=np.array(df.iloc[:,3])
    return returnMat,classLabelVector

def autoNorm(dataSet):
    dataSet_mean=dataSet.mean(axis=0)
    dataSet_std=dataSet.std(axis=0)
    normDataSet=(dataSet-dataSet_mean)/dataSet_std
    return normDataSet,dataSet_mean,dataSet_std

def datingClassTest():
    testRatio=0.1
    datingDataMat,datingLabels=file2mat(r"G:\机器学习实战\《机器学习实战》完整资源\machinelearninginaction3x-master\Ch02\datingTestSet2.txt")
    normMat,train_mean,train_std=autoNorm(datingDataMat)
    m=normMat.shape[0]
    numTestvecs=int(m*testRatio)
    errorCount=0
    for i in range(numTestvecs):
        classifyerResult=classify0(normMat[i],normMat[numTestvecs:],datingLabels[numTestvecs:],k=3)
        print("the classifier came back with {},the real answer is :{}".format(classifyerResult,datingLabels[i]))
        errorCount+=classifyerResult!=datingLabels[i]
    print("the total error rate is {:.4f}%".format(errorCount/numTestvecs * 100 ))
    print("numTestVecs=", numTestvecs)
    print(errorCount)

def classifyPerson():
    resultList=["not at all","in small doses","in large doses"]
    playGameTime=float(input("玩游戏时间:"))
    income=float(input("每年收入:"))
    iceCream=float(input("每年吃的冰淇淋数目:"))
    datingDataMat, datingLabels = file2mat(
        r"G:\机器学习实战\《机器学习实战》完整资源\machinelearninginaction3x-master\Ch02\datingTestSet2.txt")
    normMat, train_mean, train_std = autoNorm(datingDataMat)
    input_array=np.array([[playGameTime,income,iceCream]])
    inputNorm=(input_array-train_mean)/train_std
    result=classify0(inputNorm,normMat,datingLabels,k=3)
    print("You will propably like this person {}".format(resultList[result-1]))

classifyPerson()

def img2vector(filename):
    df = pd.read_csv(open(filename), header=None)
    Vect=np.zeros([32,32])
    for i in range(32):
        for j in range(32):
            Vect[i,j]=float(df.iloc[i].str[j])
    returnVect=Vect.reshape(1,-1)
    return returnVect


def handwritingclassify():
    dirName=r"G:\机器学习\机器学习实战\machinelearninginaction3x-master\Ch02\trainingDigits"
    files=os.listdir(dirName)
    for file in files:
        label=file.split("_")[0]
