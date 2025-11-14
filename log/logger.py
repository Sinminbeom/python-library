import logging
import logging.config
import os

# from config.project_config import ProjectConfig
from singleton.singleton import Singleton


class Logger(Singleton):
    def __init__(self):
        # TODO : LINUX, WINDOWS
        conf_path = os.path.join(os.path.dirname(__file__), "../../../", "logging.conf")
        # conf_path = os.path.join(os.path.dirname(__file__), '../../../', 'logging_windows.conf')
        conf_path = os.path.abspath(conf_path)
        logging.config.fileConfig(conf_path)

        # project_name = ProjectConfig.instance().project_name
        self.logger = logging.getLogger("test")
