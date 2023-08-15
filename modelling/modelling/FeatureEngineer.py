import pandas as pd
import numpy as np
from logutil import logutil


class FeatureEngineer():
    def __init__(self, df, short_desc):
        self.logger = logutil().getlogger()
        self.logger.info("START")
        self.df = df
        self.short_desc = short_desc
        self.logger.info("END")

    def get_engineered_dataframe(self):
        self.logger.info("START")
        self._to_log(["price"])
        self._to_string(["year"])
        self._onehot_encoding(["region", "year", "manufacturer", "condition", "cylinders", "fuel",
                              "title_status", "transmission", "drive", "size", "type", "paint_color"])
        self._drop_columns(["state", "region", "year", "manufacturer", "condition", "cylinders", "fuel",
                            "title_status", "transmission", "drive", "size", "type", "paint_color"])
        self.df.to_csv("data/featureengineereddataframe_" +
                       self.short_desc + ".csv")
        self.logger.info("END")
        return self.df

    def _to_string(self, cols):
        self.logger.info("START / args = {cols:[" + ",".join(cols) + "]}")
        for col in cols:
            self.df[col] = self.df[col].astype(str)
        self.logger.info("END")

    def _to_log(self, cols):
        self.logger.info("START / args = {cols:[" + ",".join(cols) + "]}")
        for col in cols:
            self.df.loc[self.df[self.df[col].notna()].index, col] = np.log(
                self.df.loc[self.df[self.df[col].notna()].index, col])
            # print(self.df)
            # self.df[col] = np.log(self.df[col])
        self.logger.info("END")

    def _onehot_encoding(self, cols):
        self.logger.info("START")
        ohdf = pd.get_dummies(self.df[cols])
        self.df = pd.concat([self.df, ohdf], axis=1)
        self.logger.info("END")

    def _drop_columns(self, cols):
        self.logger.info("START / args = {cols:[" + ",".join(cols) + "]}")
        for col in cols:
            self.df = self.df.drop(col, axis=1)
        self.logger.info("END")


def main():
    all_san = pd.read_csv("data/sanitizeddataframe_ALL.csv", index_col="id")
    engineer = FeatureEngineer(all_san, "ALL(SAN)")
    all_eng = engineer.get_engineered_dataframe()
    # print(all_eng.head())


if __name__ == '__main__':
    main()
