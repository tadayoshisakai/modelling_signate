import pandas as pd
from EDASpecificationDescriptor import EDASpecificationDescriptor


def main():
    print("IntColumnSpecificationDescriptor: main()")
    train = pd.read_csv("../data/train.csv")
    TrainColSpecDesc = ObjColumnSpecificationDescriptor(train, "TRAIN")
    TrainColSpecDesc.test()


class ObjColumnSpecificationDescriptor(EDASpecificationDescriptor):
    def __init__(self, df, short_desc):
        print("ObjColumnSpecificationDescriptor: __init__()")
        super().__init__(df, short_desc)
        self.obj_cols = ["type"]

    def _describe_cat_specification_detail(self, col):
        print("ObjColumnSpecificationDescriptor: _describe_specification_detail()")
        result = pd.DataFrame()
        for i, e in enumerate(self.df[col].unique()):
            desc = self.df[self.tgval][self.df[col] == e].describe()
            desc.name = e
            result = pd.concat([result, desc], axis=1)
        print(result.head())
        print(result.T)
        result.T.to_csv("../EDA/" + self.short_desc + "_description(" + str(
            self.df[self.tgval].dtype) + ")_" + self.tgval + "(" + col + ").txt", sep="\t")

    def test(self):
        for i, e in enumerate(self.obj_cols):
            self._describe_column_specification(e)
            self._describe_cat_specification_detail(e)


if __name__ == "__main__":
    main()
