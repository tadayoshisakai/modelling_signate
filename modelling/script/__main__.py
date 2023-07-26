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
import Preprocessing as prepro


def main():
    traindataframe = pd.read_csv("../data/train.csv")
    testdataframe = pd.read_csv("../data/test.csv")
    desc = DataDescriptor()
    desc.test(traindataframe, testdataframe)


class DataDescriptor:
    def __init__(self):
        print("DataDescriptor().__init__(): Initialize")

    def describe_column_specification(self, df, datadesc="data"):
        col = df.columns
        mylist = []
        for i, e in enumerate(col):
            tmp_list = []
            if df[e].dtype == 'int64':
                tmp_list.append("Type:" + str(df[e].dtype))
                tmp_list.append("Column Name:" + e)
                tmp_list.append("min:" + str(df[e].min()))
                tmp_list.append("MAX:" + str(df[e].max()))
                tmp_list.append("mean:" + str(round(df[e].mean(), 2)))
                tmp_list.append("median:" + str(df[e].median()))
            else:
                tmp_list.append("Type:" + str(df[e].dtype))
                tmp_list.append("Column Name:" + e)
                tmp_list.append("Data variation:" + str(len(df[e].unique())))
                tmp_list.append("mode:" + str(df[e].mode()[0]))
            mylist.append("    ".join(tmp_list))
        print("\n".join(mylist))
        f = open('../result/' + datadesc +
                 '_columnSpecification.txt', 'w')
        f.write("\n".join(mylist))
        f.close()

    def scatter_plot_multi(self, df, col, tgval, datadesc="data"):
        print("DataDescriptor().scatter_plot_multi(): Initialize")
        if not self._is_df_columns(df, col):
            print("DataDescriptor().scatter_plot_multi(): elem in col is not valid")
            return
        for i, e in enumerate(col):
            plt.clf()
            plt.scatter(df[e], df[tgval])
            plt.xlabel(e)
            plt.ylabel(tgval)
            plt.savefig("../figure/scatterPlot_" + datadesc + "_" + e +
                        ".png", format="png", dpi=300)
            # plt.show()

    def dist_plot_multi(self, df, col, tgval, datadesc="data"):
        print("DataDescriptor().dist_plot_multi(): Initialize")
        if not self._is_df_columns(df, col):
            print("DataDescriptor().dist_plot_multi(): elem in col is not valid")
            return
        for i, e in enumerate(col):
            if df[e].dtype == 'object':
                RANGE = [0, df[tgval].max()]
                for cat in df[e].unique():
                    plt.clf()
                    plt.hist(df[tgval][df[e] == cat], range=RANGE)
                    plt.title(datadesc + "_" + e + "_" + cat)
                    plt.xlabel(tgval)
                    plt.savefig("../figure/distPlot_" + datadesc + "_" + tgval + "(" +
                                e + "=" + cat + ").png", format="png", dpi=300)
            elif df[e].dtype == 'int':
                plt.clf()
                plt.hist(df[e])
                plt.title(datadesc + "_" + e)
                plt.xlabel(e)
                plt.savefig("../figure/distPlot_" + datadesc +
                            "_" + e + ".png", format="png", dpi=300)

    def box_plot_multi(self, df, col, tgval, datadesc="data"):
        print("DataDescriptor().box_plot_multi(): Initialize")
        if not self._is_df_columns(df, col):
            print("DataDescriptor().box_plot_multi(): elem in col is not valid")
            return

        for i, e in enumerate(col):
            plt.clf()
            if len(df[e].unique()) > 6:
                sns.set(font_scale=0.5)
                print(e)
            else:
                sns.set(font_scale=1)
            sns.boxplot(x=e, y=tgval, data=df, palette='pastel')
            plt.savefig("../figure/boxPlot_" + datadesc + "_" + e +
                        ".png", format="png", dpi=300)
            # plt.show()

    def _is_df_columns(self, df, col):
        print("DataDescriptor()._is_df_columns(): Initialize")
        result = True
        for i, e in enumerate(col):
            if not e in df.columns:
                result = False
        print("DataDescriptor()._is_df_columns(): return result=" + str(result))
        return result

    def test(self, train, test):
        self.describe_column_specification(train, "train")
        self.describe_column_specification(test, "test")
        self.scatter_plot_multi(
            train, ['odometer', 'year'], "price", "train")
        self.box_plot_multi(
            train, ['condition', 'cylinders', 'fuel', 'title_status', 'transmission', 'drive', 'size', 'type', 'paint_color'], "price", "train")
        self.dist_plot_multi(
            train, ['price', 'odometer', 'condition'], "price", "train")


if __name__ == '__main__':
    main()
