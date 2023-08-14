import pandas as pd
from EDASpecificationDescriptor import EDASpecificationDescriptor
import matplotlib.pyplot as plt
import seaborn as sns
from logutil import logutil


class ObjColumnSpecificationDescriptor(EDASpecificationDescriptor):
    def __init__(self, df, obj_cols, short_desc):
        self.logger = logutil().getlogger()
        self.logger.info("START / args = {short_desc:" + short_desc + "}")
        super().__init__(df, short_desc)
        self.obj_cols = obj_cols
        self.logger.info("END")

    def get_detail(self):
        self.logger.info("START")
        for c in self.obj_cols:
            if self._is_df_column(c):
                self._describe_cat_specification_detail(c)
            else:
                self.logger.warning(c + "is not dataframe columns.")
        self.logger.info("END")

    def get_boxplot(self):
        self.logger.info("START")
        for c in self.obj_cols:
            if self._is_df_column(c):
                self._export_box_plot(c)
            else:
                self.logger.warning(c + "is not dataframe columns.")
        self.logger.info("END")

    def get_valuecount(self):
        self.logger.info("START")
        for c in self.obj_cols:
            if self._is_df_column(c):
                self._export_valuecount(c)
            else:
                self.logger.warning(c + "is not dataframe columns.")
        self.logger.info("END")

    def _export_valuecount(self, col):
        self.logger.info("START / args = {col:" + col + "}")
        result = self.df[col].value_counts(dropna=False)
        result.to_csv("EDA/" + self.short_desc + "_valuecount(" + str(
            self.df[col].dtype) + ")_" + col + ".txt", sep="\t")
        self.logger.info("END")

    def _describe_cat_specification_detail(self, col):
        self.logger.info("START / args = {col:" + col + "}")
        result = pd.DataFrame()
        for i, e in enumerate(self.df[col].unique()):
            desc = self.df[self.tgval][self.df[col] == e].describe()
            desc.name = e
            result = pd.concat([result, desc], axis=1)
        result.T.to_csv("EDA/" + self.short_desc + "_description(" + str(
            self.df[self.tgval].dtype) + ")_" + self.tgval + "(" + col + ").txt", sep="\t")
        self.logger.info("END")

    def _export_box_plot(self, col):
        self.logger.info("START / args = {col:" + col + "}")
        if len(self.df[col].unique()) > 40:
            self.logger.warning("pd.Series[" + col + "] category too much.")
            return
        plt.clf()
        if len(self.df[col].unique()) > 15:
            sns.set(font_scale=0.2)
        elif len(self.df[col].unique()) > 6:
            sns.set(font_scale=0.5)
        else:
            sns.set(font_scale=1)
        sns.boxplot(x=col, y=self.tgval, data=self.df, palette='pastel')
        plt.savefig("EDA/" + self.short_desc + "_boxplot_" + col +
                    ".png", format="png", dpi=300)
        self.logger.info("END")

    def get_description(self):
        self.logger.info("START")
        for i, e in enumerate(self.obj_cols):
            if not self._is_df_column(e):
                self.logger.warning(
                    "column " + e + " is not in dataframe column.")
            else:
                self._describe_column_specification(e)
                self._describe_cat_specification_detail(e)
                self._box_plot(e)
        self.logger.info("END")


def main():
    print("IntColumnSpecificationDescriptor: main()")
    train = pd.read_csv("data/train.csv")
    TrainColSpecDesc = ObjColumnSpecificationDescriptor(train, "TRAIN")
    TrainColSpecDesc.get_description()


if __name__ == "__main__":
    main()
