#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 07:20:22 2023

@author: sakaitadayoshi
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Lasso
from sklearn.pipeline import make_pipeline
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from logutil import logutil
import itertools


class Leaning():
    def __init__(self, df, short_desc):
        self.logger = logutil().getlogger()
        self.logger.info("START")
        self.short_desc = short_desc
        self.df = df
        self.lasso_params = {
            "alpha": [0.001, 0.01, 0.1]}
        # "alpha": [0.00001, 0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]
        self.logger.info("END")

    def _split_dataframe(self):
        self.train_x, self.test_x, self.train_y, self.test_y = train_test_split(
            self.df.drop("price", axis=1), self.df["price"], test_size=0.3, random_state=0)

    def _lasso_reg(self, a):
        # self.logger.info("START / args = {alpha:" + str(a) + "}")
        lasso = Lasso(alpha=a)
        pipeline = make_pipeline(StandardScaler(), lasso)
        pipeline.fit(self.train_x, self.train_y)
        train_rmse = np.sqrt(mean_squared_error(
            self.train_y, pipeline.predict(self.train_x)))
        test_rmse = np.sqrt(mean_squared_error(
            self.test_y, pipeline.predict(self.test_x)))
        # self.logger.info("END")
        return train_rmse, test_rmse

    def lasso_tuning(self):
        self.logger.info("START")
        result = pd.DataFrame(columns=["train_rmse", "test_rmse"])
        for i, alpha in enumerate(self.lasso_params["alpha"]):
            result.loc[alpha] = self._lasso_reg(alpha)
        print(result)
        plt.clf()
        plt.figure()
        plt.plot(np.log10(result.index), result["train_rmse"], label="train")
        plt.plot(np.log10(result.index), result["test_rmse"], label="test")
        plt.ylabel("rmse")
        plt.xlabel("alpha")
        plt.legend()
        plt.savefig("../figure/lasso_rmse.png", format="png", dpi=300)
        self.logger.info("END")

    def get_model(self):
        lasso = Lasso(alpha=0.001)
        pipeline = make_pipeline(StandardScaler(), lasso)
        pipeline.fit(self.df.drop(
            "price", axis=1), self.df["price"])
        result = pd.DataFrame(index=self.df.drop("price", axis=1).columns)
        result.loc[:, "coef"] = lasso.coef_
        result.to_csv("result/lasso_coef.csv")
        return pipeline

    def exhaustive_lasso_tuning(self):
        self._split_dataframe()
        init_train_x = self.train_x
        init_train_y = self.train_y
        init_test_x = self.test_x
        init_test_y = self.test_y
        xcols = self.df.drop("price", axis=1).columns
        origin_cols = ["region", "year", "manufacturer", "condition", "cylinders", "fuel",
                       "odometer", "title_status", "transmission", "drive", "size", "type", "paint_color"]
        patterndf = pd.DataFrame(index=["name"], columns=origin_cols)
        resultdf = pd.DataFrame(
            columns=["pattern", "alpha", "train_rmse", "test_rmse"])
        conbination_arr = []
        for n in range(1, len(origin_cols)+1):
            for conb in itertools.combinations(origin_cols, n):
                conbination_arr.append(list(conb))
        for i, conb in enumerate(conbination_arr):
            # if i == 100:
            #     print("break")
            #     break
            pattern_name = 'PATT{:007}'.format(i + 1)
            print(pattern_name)
            patterndf.loc[pattern_name, conb] = True
            dfcols = []
            for col in conb:
                # print("col:" + col)
                for c in xcols:
                    # print("c:" + c)
                    if c.startswith(col):
                        dfcols.append(c)
            # print(dfcols)
            self.train_x = init_train_x.loc[:, dfcols]
            # print(self.train_x.head())
            self.test_x = init_test_x.loc[:, dfcols]
            for j, a in enumerate(self.lasso_params["alpha"]):
                train_rmse, test_rmse = self._lasso_reg(a)
                resultdf.loc[i*(len(self.lasso_params["alpha"])) +
                             j, "pattern"] = pattern_name
                resultdf.loc[i *
                             (len(self.lasso_params["alpha"])) + j, "alpha"] = a
                resultdf.loc[i*(len(self.lasso_params["alpha"])) +
                             j, "train_rmse"] = train_rmse
                resultdf.loc[i*(len(self.lasso_params["alpha"])) +
                             j, "test_rmse"] = test_rmse
        print(resultdf)
        resultdf.to_csv("result/exhaustive_lasso_tuning_result.csv")
        patterndf.to_csv("result/exhaustive_lasso_tuning_pattern.csv")
        # print(patterndf)
        # print(str(len(conbination_arr)))


def main():
    logger = logutil().getlogger()
    logger.info("START")
    verification = pd.read_csv("data/train_eng.csv", index_col="id")
    # print(verification)
    leaner = Leaning(verification, "VERIFY")
    leaner.exhaustive_lasso_tuning()
    logger.info("END")


if __name__ == "__main__":
    main()
