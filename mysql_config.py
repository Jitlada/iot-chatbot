import yaml


class MysqlConfig:
    mysql_conf_file = ""

    def __init__(self):
        # self.mysql_conf_file = "/home/user01/petdy-iBeacon/toon-bot/database_config.yaml"
        # self.mysql_conf_file = "/home/user01/hr-ibeacon-checkin/toon-bot/database_config.yaml"
        self.mysql_conf_file = "/home/user01/ibeacon-dev/iot-chatbot/database_config.yaml"

    def showData(self):
        print("Testing")

    def callDBConfig(self):
        TAG = "callDBConfig"
        with open(self.mysql_conf_file) as my_config:
            # print(TAG, yaml.load(my_config, Loader=yaml.FullLoader))
            # return yaml.load(my_config, Loader=yaml.FullLoader)
            return yaml.safe_load(my_config)
