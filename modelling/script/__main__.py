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
import logging
from EDASpecificationDescriptor import EDASpecificationDescriptor
from IntColumnSpecificationDescriptor import IntColumnSpecificationDescriptor
from ObjColumnSpecificationDescriptor import ObjColumnSpecificationDescriptor
from Preprocessing import DataSanitizer


def main():
    train = pd.read_csv("../data/train.csv")
    test = pd.read_csv("../data/test.csv")
    TrainIntColSpecDesc = IntColumnSpecificationDescriptor(train, "TRAIN")
    TrainIntColSpecDesc.get_description()
    TrainObjColSpecDesc = ObjColumnSpecificationDescriptor(train, "TRAIN")
    TrainObjColSpecDesc.get_description()
    train_san = DataSanitizer(train, "TRAIN(SAN)").get_sanitized_dataframe()
    TrainSanIntColSpecDesc = IntColumnSpecificationDescriptor(
        train_san, "TRAIN(SAN)")
    TrainSanIntColSpecDesc.get_description()
    TrainSanObjColSpecDesc = ObjColumnSpecificationDescriptor(
        train_san, "TRAIN(SAN)")
    TrainSanObjColSpecDesc.get_description()


if __name__ == '__main__':
    main()
