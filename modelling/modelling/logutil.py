import yaml
from logging import config, getLogger


class logutil():
    def __init__(self):
        config.dictConfig(yaml.safe_load(
            open("config/logconfig.yaml").read()))
        self.logger = getLogger("modellingLogger")

    def getlogger(self):
        return self.logger


def main():
    logger = logutil().getlogger()
    logger.info("START")


if __name__ == "__main__":
    main()
