import pandas as pd
import matplotlib.pyplot as plt
from EDASpecificationDescriptor import EDASpecificationDescriptor


class IntColumnSpecificationDescriptor(EDASpecificationDescriptor):
    def __init__(self, df, short_desc):
        print("IntColumnSpecificationDescriptor: __init__()")
        super().__init__(df, short_desc)
        self.int_cols = ["price", "odometer", "year"]

    def _export_scatterplot(self, col):
        print("IntColumnSpecificationDescriptor: _export_scatterplot()")
        if col == self.tgval:
            print("IntColumnSpecificationDescriptor._export_scatterplot(): Target Val not applicable to scatter plot.")
            return
        plt.clf()
        plt.scatter(self.df[col], self.df[self.tgval])
        plt.xlabel(col)
        plt.ylabel(self.tgval)
        plt.savefig("../EDA/" + self.short_desc + "_scatterplot_" + col +
                    ".png", format="png", dpi=300)

    def _expor_distplot(self, col):
        print("IntColumnSpecificationDescriptor: _export_distplot()")
        plt.clf()
        plt.hist(self.df[col])
        plt.title(self.short_desc + "_" + col)
        plt.xlabel(col)
        plt.savefig("../EDA/" + self.short_desc + "_distplot_" + col +
                    ".png", format="png", dpi=300)
        # if df[e].dtype == 'object':
        #     RANGE = [0, df[tgval].max()]
        #     for cat in df[e].dropna().unique():
        #         plt.clf()
        #         plt.hist(df[tgval][df[e] == cat], range=RANGE)
        #         plt.title(datadesc + "_" + e + "_" + cat)
        #         plt.xlabel(tgval)
        #         plt.savefig("../figure/distPlot_" + datadesc + "_" + tgval + "(" +
        #                     e + "=" + cat + ").png", format="png", dpi=300)

    def get_description(self):
        for i, e in enumerate(self.int_cols):
            if not self._is_df_column(e):
                print(e + " is not in self.df columns.")
            else:
                self._describe_column_specification(e)
                self._export_scatterplot(e)
                self._expor_distplot(e)


def main():
    print("IntColumnSpecificationDescriptor: main()")
    train = pd.read_csv("../data/train.csv")
    TrainColSpecDesc = IntColumnSpecificationDescriptor(train, "TRAIN")
    TrainColSpecDesc.get_description()


if __name__ == "__main__":
    main()
