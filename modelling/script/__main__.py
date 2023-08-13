# numpy , pandas
import numpy as np
import pandas as pd
# scikit-learn

from sklearn.model_selection import train_test_split

# 可視化用ライブラリ
import matplotlib.pyplot as plt
import seaborn as sns

import json
from logutil import logutil
from EDASpecificationDescriptor import EDASpecificationDescriptor
from IntColumnSpecificationDescriptor import IntColumnSpecificationDescriptor
from ObjColumnSpecificationDescriptor import ObjColumnSpecificationDescriptor
from DataSanitizer import DataSanitizer
from Preprocessing import Preprocessing
from Learning import Leaning
from Predicting import Predicting

def main():
    logger = logutil().getlogger()
    logger.info("START")
    train = pd.read_csv("../data/train.csv",index_col='id')
    TrainIntColSpecDesc = IntColumnSpecificationDescriptor(train, "TRAIN")
    TrainIntColSpecDesc.get_description()
    TrainObjColSpecDesc = ObjColumnSpecificationDescriptor(train, "TRAIN")
    TrainObjColSpecDesc.get_description()
    train_san = DataSanitizer(train, "TRAIN").get_sanitized_dataframe()
    TrainSanIntColSpecDesc = IntColumnSpecificationDescriptor(
        train_san, "TRAIN(SAN)")
    TrainSanIntColSpecDesc.get_description()
    TrainSanObjColSpecDesc = ObjColumnSpecificationDescriptor(
        train_san, "TRAIN(SAN)")
    TrainSanObjColSpecDesc.get_description()
    train_data_set = Preprocessing(train_san,"TRAIN(SAN)").get_preprocessed_dataset()
    train_dataframe = Preprocessing(train_san,"TRAIN(SAN)").get_preprocessed_dataframe()
    learning = Leaning(train_dataframe, train_data_set)
    learning.lasso_tuning()
    model = learning.get_model()

    test = pd.read_csv("../data/test.csv",  index_col='id')
    # TestIntColSpecDesc = IntColumnSpecificationDescriptor(test, "TEST")
    # TestIntColSpecDesc.get_description()
    # TestObjColSpecDesc = ObjColumnSpecificationDescriptor(test, "TEST")
    # TestObjColSpecDesc.get_description()
    test_san = DataSanitizer(test, "TEST(SAN)").get_test_dataframe()
    # TestSanIntColSpecDesc = IntColumnSpecificationDescriptor(test_san, "TEST(SAN)")
    # TestSanIntColSpecDesc.get_description()
    # TestSanObjColSpecDesc = ObjColumnSpecificationDescriptor(test_san, "TEST(SAN)")
    # TestSanObjColSpecDesc.get_description()
    test_dataframe = Preprocessing(test_san, "TEST(SAN)").get_preprocessed_dataframe()
    result_dataframe = pd.concat([test,Predicting(test_dataframe, model).get_predicted_result()], axis = 1)
    result_dataframe.to_csv("../data/result.csv")
    ResultIntColSpecDesc = IntColumnSpecificationDescriptor(result_dataframe, "TEST")
    ResultIntColSpecDesc.get_description()
    ResultObjColSpecDesc = ObjColumnSpecificationDescriptor(result_dataframe, "TEST")
    ResultObjColSpecDesc.get_description()
    result_san = DataSanitizer(result_dataframe, "TRAIN").get_sanitized_dataframe()
    ResultSanIntColSpecDesc = IntColumnSpecificationDescriptor(
        result_san, "Result(SAN)")
    ResultSanIntColSpecDesc.get_description()
    ResultSanObjColSpecDesc = ObjColumnSpecificationDescriptor(
        result_san, "Result(SAN)")
    ResultSanObjColSpecDesc.get_description()    

    
    logger.info("END")


if __name__ == '__main__':
    main()
