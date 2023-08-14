import pandas as pd
import matplotlib.pyplot as plt
from EDASpecificationDescriptor import EDASpecificationDescriptor
from logutil import logutil


class IntColumnSpecificationDescriptor(EDASpecificationDescriptor):
    def __init__(self, df, int_cols, short_desc):
        self.logger = logutil().getlogger()
        self.logger.info("START / args ={short_desc:" + short_desc + "}")
        super().__init__(df, short_desc)
        self.int_cols = int_cols
        self.logger.info("END")

    def get_scatter(self):
        self.logger.info("START")
        for c in self.int_cols:
            if self._is_df_column(c):
                self._export_scatterplot(c)
            else:
                self.logger.warning(c + "is not dataframe columns.")
        self.logger.info("END")

    def get_dist(self):
        self.logger.info("START")
        for c in self.int_cols:
            if self._is_df_column(c):
                self._export_distplot(c)
            else:
                self.logger.warning(c + "is not dataframe columns.")
        self.logger.info("END")

    def _export_scatterplot(self, col):
        self.logger.info("START / args = {col:" + col + "}")
        if col == self.tgval:
            self.logger.warning("Target val '" + col +
                                "' is not applicable to scatter plot.")
            return
        plt.clf()
        plt.scatter(self.df[col], self.df[self.tgval])
        plt.xlabel(col)
        plt.ylabel(self.tgval)
        plt.savefig("EDA/" + self.short_desc + "_scatterplot_" + col +
                    ".png", format="png", dpi=300)
        self.logger.info("END")

    def _export_distplot(self, col):
        self.logger.info("START / args = {col:" + col + "}")
        plt.clf()
        plt.hist(self.df[col])
        plt.title(self.short_desc + "_" + col)
        plt.xlabel(col)
        plt.savefig("EDA/" + self.short_desc + "_distplot_" + col +
                    ".png", format="png", dpi=300)
        self.logger.info("END")

    def get_description(self):
        self.logger.info("START")
        for i, e in enumerate(self.int_cols):
            if not self._is_df_column(e):
                self.logger.warning(e + "is not in dataframe column.")
            else:
                self._describe_column_specification(e)
                self._export_scatterplot(e)
                self._expor_distplot(e)
        self.logger.info("END")


def main():
    print("IntColumnSpecificationDescriptor: main()")
    train = pd.read_csv("/data/train.csv")
    TrainColSpecDesc = IntColumnSpecificationDescriptor(train, "TRAIN")
    TrainColSpecDesc.get_description()


if __name__ == "__main__":
    main()
