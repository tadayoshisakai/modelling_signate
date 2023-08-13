#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 07:20:22 2023

@author: sakaitadayoshi[]
"""
import pandas as pd
import numpy as np
from logutil import logutil


class DataSanitizer():
    def __init__(self, df, short_desc):
        self.logger = logutil().getlogger()
        self.logger.info("START / args = {short_desc:" + short_desc + "}")
        self.df = df
        self.short_desc = short_desc
        self.dfsize = df.shape
        self.logger.info("END")

    def _sanitize_year(self):
        self.logger.info("START")
        if self.short_desc == "TRAIN":
            self._outlier_exception("year < 2050")
        self.logger.info("END")

    def _sanitize_odometer(self):
        self.logger.info("START")
        if self.short_desc == "TRAIN":
            self._outlier_exception("odometer > 0 & odometer < 500000")
        self.logger.info("END")

    def _sanitize_region(self):
        self.logger.info("START")
        self._drop_column("region")
        self.logger.info("END")

    def _sanitize_state(self):
        self.logger.info("START")
        self._drop_column("state")
        self.logger.info("END")

    def _sanitize_manufacturer(self):
        self.logger.info("START")
        self._transform_category(
            "manufacturer", "../config/transformmap_manufacturer.txt")
        # if self.short_desc == "TRAIN":
        #     self._drop_few("manufacturer")
        self.logger.info("END")

    def _sanitize_condition(self):
        self.logger.info("START")
        self._transform_category(
            "condition", "../config/transformmap_condition.txt")
        self.logger.info("END")

    def _sanitize_cylinders(self):
        self.logger.info("START")
        self._transform_category(
            "cylinders", "../config/transformmap_cylinders.txt")
        self.logger.info("END")

    def _sanitize_size(self):
        self.logger.info("START")
        self._transform_category(
            "size", "../config/transformmap_size.txt")
        self.logger.info("END")

    def _sanitize_title_status(self):
        self.logger.info("START")
        self._transform_category(
            "title_status", "../config/transformmap_title_status.txt")
        if self.short_desc == "TRAIN":
            self._drop_nan("title_status")
        self.logger.info("END")

    def _sanitize_type(self):
        self.logger.info("START")
        if self.short_desc == "TRAIN":
            self._drop_nan("type")
        self.logger.info("END")

    def _sanitize_price(self):
        self.logger.info("START")
        if not "price" in self.df.columns:
            self.logger.warning("price is not in dataframe column.")
        else:
            self._to_log("price")
        self.logger.info("END")

    def _outlier_exception(self, q):
        self.logger.info("START / args = {q:" + q + "}")
        init_size = self.df.shape
        self.df = self.df.query(q)
        self.logger.info("Querying(" + q + ")-> " +
                         str(init_size[0] - self.df.shape[0]) + "row removed.")
        self.logger.info("END")

    def _drop_column(self, col):
        self.logger.info("START / args = {col:" + col + "}")
        self.df = self.df.drop(col, axis=1)
        self.logger.info("END")

    def _drop_nan(self, col):
        self.logger.info("START / args = {col:" + col + "}")
        initial_size = self.df.shape
        self.df = self.df[self.df[col].isnull() != True]
        self.logger.info(
            str(initial_size[0]-self.df.shape[0]) + " row removed.")
        self.logger.info("END")

    def _drop_few(self, col):
        self.logger.info("START / args = {col:" + col + "}")
        init_size = self.df.shape
        count = self.df[col].value_counts()
        rem_list = []
        for c in count.index:
            if count[c]>20:
                rem_list.append(c)
        #print(rem_list)
        q = "manufacturer in " + str(rem_list)
        self.df = self.df.query(q)
        self.logger.info("Querying(" + q + ")-> " +
                         str(init_size[0] - self.df.shape[0]) + "row removed.")
        self.logger.info("END")

    def _transform_category(self, col, map_path):
        self.logger.info(
            "START / args = {col:" + col + ",map_path:" + map_path + "}")
        transform_map = pd.read_csv(map_path)
        for name, items in transform_map.iterrows():
            self.df[col] = self.df[col].mask(
                self.df[col] == items['from'], items['to'])
        self.logger.info("END")

    def _to_log(self, col):
        self.logger.info("START / args = {col:" + col + "}")
        self.df[col] = np.log(self.df[col])
        self.logger.info("END")

    def get_sanitized_dataframe(self):
        self.logger.info("START")
        self._sanitize_year()
        self._sanitize_odometer()
        self._sanitize_region()
        self._sanitize_state()
        self._sanitize_manufacturer()
        self._sanitize_condition()
        self._sanitize_cylinders()
        self._sanitize_size()
        self._sanitize_title_status()
        self._sanitize_type()
        self._sanitize_price()
        self.logger.info("END")
        return self.df
    def get_test_dataframe(self):
        self.logger.info("START")
        #self._sanitize_year()
        #self._sanitize_odometer()
        self._sanitize_region()
        self._sanitize_state()
        self._sanitize_manufacturer()
        self._sanitize_condition()
        self._sanitize_cylinders()
        self._sanitize_size()
        self._sanitize_title_status()
        self._sanitize_type()
        self._sanitize_price()
        self.logger.info("END")
        return self.df


def main():
    print("Preprocessing: main()")
    df = pd.read_csv("../data/train.csv")
    DataSanitizer(df, "TRAIN").get_sanitized_dataframe()


if __name__ == "__main__":
    main()
