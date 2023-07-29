import pandas as pd
from EDASpecificationDescriptor import EDASpecificationDescriptor


def main():
    print("IntColumnSpecificationDescriptor: main()")
    train = pd.read_csv("../data/train.csv")
    TrainColSpecDesc = IntColumnSpecificationDescriptor(train, "TRAIN")
    TrainColSpecDesc.test()


class IntColumnSpecificationDescriptor(EDASpecificationDescriptor):
    def __init__(self, df, short_desc):
        print("IntColumnSpecificationDescriptor: __init__()")
        super().__init__(df, short_desc)
        self.int_cols = ["price", "odometer", "year"]

    def test(self):
        for i, e in enumerate(self.int_cols):
            self._describe_column_specification(e)


if __name__ == "__main__":
    main()
