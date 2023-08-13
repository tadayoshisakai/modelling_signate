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
from logutil import logutil


class Leaning():
    def __init__(self, df, dataset):
        self.logger = logutil().getlogger()
        self.logger.info("START")
        self.dataset = dataset
        self.df = df
        self.lasso_params = {"alpha" : [0.0001, 0.0003, 0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0, 30.0, 100.0, 300.0, 1000.0]}
        self.logger.info("END")
    def _lasso_reg(self,a):
        self.logger.info("START / args = {alpha:" + str(a) + "}")
        lasso = Lasso(alpha=a) 
        pipeline = make_pipeline(StandardScaler(), lasso)
        pipeline.fit(self.dataset["train_x"],self.dataset["train_y"])
        train_rmse = np.sqrt(mean_squared_error(self.dataset["train_y"], pipeline.predict(self.dataset["train_x"])))
        test_rmse = np.sqrt(mean_squared_error(self.dataset["test_y"], pipeline.predict(self.dataset["test_x"])))
        self.logger.info("END")
        return train_rmse, test_rmse
    def lasso_tuning(self):
        self.logger.info("START")
        result = pd.DataFrame(columns=["train_rmse","test_rmse"])
        for i, alpha in enumerate(self.lasso_params["alpha"]):
            result.loc[alpha] = self._lasso_reg(alpha)
        print(result)
        plt.clf()
        plt.figure()
        plt.plot(np.log10(result.index), result["train_rmse"], label = "train")
        plt.plot(np.log10(result.index), result["test_rmse"], label = "test")
        plt.ylabel("rmse")
        plt.xlabel("alpha")
        plt.legend()
        plt.savefig("../figure/lasso_rmse.png", format="png", dpi=300)
        self.logger.info("END")
    def get_model(self):
        lasso = Lasso(alpha=0.001)
        pipeline = make_pipeline(StandardScaler(),lasso)
        pipeline.fit(self.df.drop("price", axis = 1), self.df["price"])
        result = pd.DataFrame(index=self.df.drop("price",axis = 1).columns)
        result.loc[:, "coef"] = lasso.coef_
        result.to_csv("../result/lasso_coef.csv")
        return pipeline

def main():
    logger = logutil().getlogger()
    logger.info("START")
    logger.info("END")