#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 07:20:22 2023

@author: sakaitadayoshi
"""

from logutil import logutil
import pandas as pd
import numpy as np

class Predicting():
    def __init__(self, df, model):
        self.logger = logutil().getlogger()
        self.logger.info("START")
        self.df = df
        self.model = model
        self.logger.info("END")
    def get_predicted_result(self):
        self.logger.info("START")
        result = pd.DataFrame({"id" : self.df.index, "price" : np.exp(self.model.predict(self.df))})
        result = result.set_index("id")
        result.to_csv("../result/submit.csv", header=False)
        self.logger.info("END")
        return result

def main():
    print("main")

if __name__=='__main__':
    main()
