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

    def _sanitize_region(self):
        self._drop_column("region")

    def _sanitize_state(self):
        self._drop_column("state")

    def _sanitize_manufacturer(self):
        self._transform_category(
            "manufacturer", "../config/transformmap_manufacturer.csv")

    def _outlier_exception(self, q):
        init_size = self.df.shape
        print("DataSanitizer._outlier_exception(): Initialize")
        self.df = self.df.query(q)
        print("DataSanitizer._outlier_exception(): Query(" + q + ")-> " +
              str(init_size[0] - self.df.shape[0]) + "row removed.")

    def _drop_column(self, col):
        self.df = self.df.drop(col, axis=1)

    def _transform_category(self, col, map_path):
        transform_map = pd.read_csv(map_path, encoding='shift-jis')
        print(transform_map.head())

    def get_sanitized_dataframe(self):
        self._sanitize_year()
        self._sanitize_odometer()
        self._sanitize_region()
        self._sanitize_state()
        self._sanitize_manufacturer()
        return self.df


def main():
    print("Preprocessing: main()")
    df = pd.read_csv("../data/train.csv")
    DataSanitizer(df, "TRAIN(SAN)").get_sanitized_dataframe()


if __name__ == "__main__":
    main()
