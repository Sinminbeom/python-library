from typing import Any, List

from configure.config_utils import ConfigUtils
from singleton.singleton import Singleton

# TODO : LINUX, WINDOWS
CONFIG_PATH = "application.conf"
# CONFIG_PATH = (
#     "C:\\Users\\shinminbeom\\dev\\source\\local\\data-collector\\application_windows.conf"
# )


class ConfigManager(Singleton):
    DELIM_CHAR = "|"

    def __init__(self):
        self.config = self.__pre_treatment()

    def set_config_path(self, config_path: str):
        self.config_path = config_path

    def __pre_treatment(self):
        config = ConfigUtils.config_parser(config_file=CONFIG_PATH)
        tmp_config = dict()
        for key, value in config.items():
            tmp = value
            if value[0] == "[":
                tmp = tmp[1:]
            if value[-1] == "]":
                tmp = tmp[0:-1]

            value = list(s.strip() for s in tmp.split(ConfigManager.DELIM_CHAR))

            if len(value) == 1:
                tmp_config[key] = value[0]
            else:
                tmp_config[key] = value

        return tmp_config

    def __get_config_from_title(self, _title):
        new_config = dict()
        for k, v in self.config.items():
            if k[0] == _title or k[0] == "COMMON":
                new_config[k[1]] = v

        return new_config

    def get_config(self, title1=None, title2=None) -> Any:
        if title1 is None:
            return self.config
        elif title1 is not None and title2 is None:
            return self.__get_config_from_title(title1)
        elif title1 is not None and title2 is not None:
            return self.get_value(title1, title2)

    def get_value(self, _title1, _title2) -> str | List[str]:
        return self.get_config(_title1)[_title2.lower()]
