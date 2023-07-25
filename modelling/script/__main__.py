# numpy , pandas
import numpy as np 
import pandas as pd
# scikit-learn
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Lasso
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
# 可視化用ライブラリ
import matplotlib.pyplot as plt
import seaborn as sns

import json




def main():
    trainDataFrame = pd.read_csv("../data/train.csv")
    testDataFrame = pd.read_csv("../data/test.csv")
    describeColumnSpecification(trainDataFrame,"train")
    describeColumnSpecification(testDataFrame,"test")
    print("End")


def describeColumnSpecification(df,dataDescription="None"):
    col = df.columns
    reportDF=pd.DataFrame(columns=['column','type','min','max','mean','median','variation','mode'])
    #reportDF = pd.DataFrame()
    for i, e in enumerate(col):
        tmpDict = {}
        if df[e].dtype=='int64':
            tmpDict["type"]=df[e].dtype
            tmpDict['column']=e
            tmpDict['min']=df[e].min()
            tmpDict['max']=df[e].max()
            tmpDict['mean']=round(df[e].mean(),2)
            tmpDict['median']=df[e].median()
        else:
            tmpDict["type"]=df[e].dtype
            tmpDict['column']=e
            tmpDict['variation']=len(df[e].unique())
            tmpDict['mode']=df[e].mode()[0]
        reportDF = reportDF.append(tmpDict,ignore_index=True)
    reportDF.to_csv("../result/" + dataDescription + "_columnSpecification.csv")   
 

if __name__=='__main__':
    main()
