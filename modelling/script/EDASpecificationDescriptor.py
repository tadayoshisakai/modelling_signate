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


def main():
    print("EDASpecificationDescriptor: main()")


class EDASpecificationDescriptor:
    def __init__(self, df, short_desc):
        print("EDASpecificationDescriptor: __init__()")
        self.df = df
        self.short_desc = short_desc
        self.tgval = "price"
        self.cols = self.df.columns
        self._describe_columns_overview()

    def _describe_column_specification(self, col):
        print("EDASpecificationDescriptor: _describe_specification()")
        result = self.df[col].describe(percentiles=[.25, .5, .75, .95])
        result.to_csv("../EDA/" + self.short_desc +
                      "_description(" + str(self.df[col].dtype) + ")_" + col + ".txt", sep="\t")
        return result

    def _describe_columns_overview(self):
        mylist = []
        for i, e in enumerate(self.cols):
            tmp_list = []
            if self.df[e].dtype == 'int64':
                tmp_list.append("Type:" + str(self.df[e].dtype))
                tmp_list.append("Column Name:" + e)
                tmp_list.append("min:" + str(self.df[e].min()))
                tmp_list.append("MAX:" + str(self.df[e].max()))
                tmp_list.append("mean:" + str(round(self.df[e].mean(), 2)))
                tmp_list.append("median:" + str(self.df[e].median()))
                tmp_list.append("null:" + str(self.df[e].isnull().sum()))
            else:
                tmp_list.append("Type:" + str(self.df[e].dtype))
                tmp_list.append("Column Name:" + e)
                tmp_list.append("Data variation:" +
                                str(len(self.df[e].unique())))
                tmp_list.append("mode:" + str(self.df[e].mode()[0]))
                tmp_list.append("null:" + str(self.df[e].isnull().sum()))
            mylist.append("    ".join(tmp_list))
        mylist.append(
            "size:" + str(self.df.shape[0]) + ", " + str(self.df.shape[1]))
        print("\n".join(mylist))
        f = open('../EDA/' + self.short_desc +
                 '_overview.txt', 'w')
        f.write("\n".join(mylist))
        f.close()

    def _is_df_column(self, col):
        if col in self.df.columns:
            return True
        else:
            return False

    def _traindata_test(self):
        print("EDASpecificationDescriptor: _traindata_test()")
        df = pd.read_csv("../data/train.csv")


if __name__ == "__main__":
    main()
