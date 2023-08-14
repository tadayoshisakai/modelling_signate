# numpy , pandas
import pandas as pd
# scikit-learn

from sklearn.model_selection import train_test_split

# 可視化用ライブラリ
import matplotlib.pyplot as plt
import seaborn as sns

import json
from logutil import logutil
from EDADescriptor import EDADescriptor
from DataSanitizer import DataSanitizer
from FeatureEngineer import FeatureEngineer
from Learning import Leaning
from Predicting import Predicting
from DataFrameHandler import DataFrameHandler


def main():
    logger = logutil().getlogger()
    logger.info("START")
    train = pd.read_csv("data/train.csv", index_col="id")
    test = pd.read_csv("data/test.csv", index_col="id")
    test["price"] = 1
    desc = EDADescriptor()
    # desc.get_traindata_description(train, "TRAIN")
    # desc.get_testdata_description(test, "TEST")
    handler = DataFrameHandler("TRAIN", "TEST")
    all = handler.concat_dataframe(train, test)
    # desc.get_testdata_description(all, "ALL")
    sanitizer = DataSanitizer(all, "ALL")
    all_san = sanitizer.get_sanitized_dataframe()
    train_san, test_san = handler.sprit_dataframe(all_san)
    # desc.get_traindata_description(train_san, "TRAIN(SAN)")
    # desc.get_testdata_description(test_san, "TEST(SAN)")
    engineer = FeatureEngineer(all_san, "ALL(SAN)")
    all_eng = engineer.get_engineered_dataframe()
    train_eng, test_eng = handler.sprit_dataframe_without_domain(all_eng)
    train_eng.to_csv("data/train_eng.csv")
    leaner = Leaning(train_eng, "TRAIN(ENG)")
    my_model = leaner.get_model()
    result_dataframe = pd.concat(
        [test, Predicting(test_eng, my_model).get_predicted_result()], axis=1)
    result_dataframe.to_csv("data/predictedresult.csv")
    logger.info("END")


if __name__ == '__main__':
    main()
