from IntColumnSpecificationDescriptor import IntColumnSpecificationDescriptor
from ObjColumnSpecificationDescriptor import ObjColumnSpecificationDescriptor
from logutil import logutil


class EDADescriptor():
    def __init__(self):
        self.logger = logutil().getlogger()
        self.logger.info("START")
        self.train_int_cols = ["price", "year", "odometer"]
        self.train_obj_cols = ["region", "manufacturer", "condition", "cylinders", "fuel",
                               "title_status", "transmission", "drive", "size", "paint_color", "state"]
        self.test_int_cols = ["year", "odometer"]
        self.test_obj_cols = ["region", "manufacturer", "condition", "cylinders", "fuel",
                              "title_status", "transmission", "drive", "size", "paint_color", "state"]

        self.logger.info("END")

    def get_traindata_description(self, df, short_desc):
        self.logger.info("START / args = {short_desc:" + short_desc + "}")
        intdesc = IntColumnSpecificationDescriptor(
            df, self.train_int_cols, short_desc)
        intdesc.get_scatter()
        intdesc.get_dist()
        objdesc = ObjColumnSpecificationDescriptor(
            df, self.train_obj_cols, short_desc)
        objdesc.get_detail()
        objdesc.get_boxplot()
        objdesc.get_valuecount()
        self.logger.info("END")

    def get_testdata_description(self, df, short_desc):
        self.logger.info("START / args = {short_desc:" + short_desc + "}")
        intdesc = IntColumnSpecificationDescriptor(
            df, self.test_int_cols, short_desc)
        # intdesc.get_scatter()
        intdesc.get_dist()
        objdesc = ObjColumnSpecificationDescriptor(
            df, self.test_obj_cols, short_desc)
        # objdesc.get_detail()
        # objdesc.get_boxplot()
        objdesc.get_valuecount()
        self.logger.info("END")


def main():
    logger = logutil().getlogger()
    logger.info("Called as main function.")


if __name__ == "__main__":
    main()
