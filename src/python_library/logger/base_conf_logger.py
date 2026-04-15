import logging
import logging.config
from typing import Optional

from python_library.singleton.singleton import Singleton


class BaseConfLogger(Singleton):
    CONFIG_PATH: Optional[str] = None
    NAME: Optional[str] = None

    def __init__(self):
        cls = self.__class__
        if cls is BaseConfLogger:
            raise TypeError("BaseConfLogger cannot be instantiated directly.")
        if cls.CONFIG_PATH is None or cls.NAME is None:
            raise RuntimeError(
                f"{cls.__name__} configuration is not set. Call {cls.__name__}.set_config()."
            )

        with open(cls.CONFIG_PATH, "r", encoding="utf-8") as f:
            logging.config.fileConfig(f)
        self._logger = logging.getLogger(cls.NAME)

    @classmethod
    def set_config(cls, conf_path: str, name: str) -> None:
        cls.CONFIG_PATH = conf_path
        cls.NAME = name
