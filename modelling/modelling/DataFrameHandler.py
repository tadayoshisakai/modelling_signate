from logutil import logutil
import pandas as pd


class DataFrameHandler():
    def __init__(self, domain1, domain2):
        self.domain1 = domain1
        self.domain2 = domain2

    def concat_dataframe(self, df1, df2):
        df1["domain"] = self.domain1
        df2["domain"] = self.domain2
        df = pd.concat([df1, df2])
        # df = df.reset_index()
        return df

    def sprit_dataframe(self, df):
        df1 = df.query('domain == "' + self.domain1 + '"')
        # df1 = df1.reset_index()
        df2 = df.query('domain == "' + self.domain2 + '"')
        # df2 = df2.reset_index()
        return df1, df2

    def sprit_dataframe_without_domain(self, df):
        df1 = df.query('domain == "' + self.domain1 + '"')
        df1 = df1.drop("domain", axis=1)
        # df1 = df1.reset_index()
        df2 = df.query('domain == "' + self.domain2 + '"')
        df2 = df2.drop("domain", axis=1)
        # df2 = df2.reset_index()
        return df1, df2


def main():
    logger = logutil().getlogger()
    logger.info("Called as main function.")
    train = pd.read_csv("data/train.csv")
    test = pd.read_csv("data/test.csv")
    handler = DataFrameHandler("TRAIN", "TEST")
    all = handler.concat_dataframe(train, test)
    print(all)
    train, test = handler.sprit_dataframe(all)
    print(train)
    print(test)


if __name__ == "__main__":
    main()
