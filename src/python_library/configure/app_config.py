from typing import Any, List, Optional

from python_library.configure.config_utils import ConfigUtils
from python_library.singleton.singleton import Singleton


class AppConfig(Singleton):
    DELIM_CHAR = "|"
    CONFIG_PATH: Optional[str] = None

    def __init__(self):
        self.config = self.__pre_treatment()

    @classmethod
    def set_config(cls, config_path: str):
        """
        설정 파일 경로를 바꾸고, config 를 다시 로드하고 싶을 때 사용.
        """
        cls.CONFIG_PATH = config_path
        cls.config = cls.__pre_treatment()

    @classmethod
    def __pre_treatment(cls) -> dict:
        config = ConfigUtils.config_parser(config_file=cls.CONFIG_PATH)
        tmp_config = dict()
        for key, value in config.items():
            tmp = value
            if value[0] == "[":
                tmp = tmp[1:]
            if value[-1] == "]":
                tmp = tmp[0:-1]

            value = list(s.strip() for s in tmp.split(cls.DELIM_CHAR))

            if len(value) == 1:
                tmp_config[key] = value[0]
            else:
                tmp_config[key] = value

        return tmp_config

    def __get_config_from_title(self, _title) -> dict:
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
