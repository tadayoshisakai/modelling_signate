import pandas as pd
from sklearn.model_selection import train_test_split
from logutil import logutil


class Preprocessing():
    def __init__(self,df,short_desc):
        self.logger = logutil().getlogger()
        self.logger.info("START / args = {short_desc:" + short_desc + "}")
        self.df = df
        self.short_desc = short_desc
        self.tgval = "price"
        self.logger.info("END")
    def _int_to_string(self,cols):
        self.logger.info("START / args = {cols:[" + ",".join(cols) + "]}")
        num2str_list = ['MSSubClass','YrSold','MoSold']
        for col in cols:
            self.df[col] = self.df[col].astype(str)
        self.logger.info("END")        

    def _onehot_encoding(self):
        self.logger.info("START")
        self.df = pd.get_dummies(self.df)
        self.logger.info("END")

    def _split_dataframe(self):
        self.train_x, self.test_x, self.train_y, self.test_y = train_test_split(self.df.drop(self.tgval, axis=1), self.df[self.tgval], test_size=0.3, random_state=0)


    def get_preprocessed_dataset(self):
        self.logger.info("START")
        #self._int_to_string(["year"])
        self._onehot_encoding()
        self._split_dataframe()
        self.logger.info("END")
        dataset = {"train_x": self.train_x, "train_y": self.train_y, "test_x": self.test_x, "test_y": self.test_y}
        return dataset
    
    def get_preprocessed_dataframe(self):
        self.logger.info("START")
        #self._int_to_string(["year"])
        self._onehot_encoding()
        self.logger.info("END")
        return self.df

def main():
    train = pd.read_csv("../data/train.csv")    
    prepro = Preprocessing(train,"TRAIN_SAN")
    test = prepro.get_preprocessed_dataframe()
    print(test.head())


if __name__=='__main__':
    main()