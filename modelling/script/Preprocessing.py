#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 07:20:22 2023

@author: sakaitadayoshi[]
"""
import pandas as pd


class DataSanitizer():
    def __init__(self, df, short_desc):
        print("DataSanitizer: __init__()")
        self.df = df
        self.short_desc = short_desc
        self.dfsize = df.shape

    def _sanitize_year(self):
        self._outlier_exception("year < 2050")

    def _sanitize_odometer(self):
        self._outlier_exception("odometer > 0 & odometer < 500000")

    def _outlier_exception(self, q):
        init_size = self.df.shape
        print("DataSanitizer._outlier_exception(): Initialize")
        self.df = self.df.query(q)
        print("DataSanitizer._outlier_exception(): Query(" + q + ")-> " +
              str(init_size[0] - self.df.shape[0]) + "row removed.")

    def get_sanitized_dataframe(self):
        self._sanitize_year()
        self._sanitize_odometer()
        return self.df


def main():
    print("Preprocessing: main()")
    df = pd.read_csv("../data/train.csv")
    DataSanitizer(df, "TRAIN(SAN)").get_sanitized_dataframe()


if __name__ == "__main__":
    main()
