from python_library.logger.base_conf_logger import BaseConfLogger


class AppLogger(BaseConfLogger):
    def info(self, msg: object, exc_info: bool = False) -> None:
        self._logger.info(msg, exc_info=exc_info)

    def debug(self, msg: object, exc_info: bool = False) -> None:
        self._logger.debug(msg, exc_info=exc_info)

    def warning(self, msg: object, exc_info: bool = False) -> None:
        self._logger.warning(msg, exc_info=exc_info)

    def error(self, msg: object, exc_info: bool = False) -> None:
        self._logger.error(msg, exc_info=exc_info)

    def exception(self, msg: object, exc: BaseException | None = None) -> None:
        self._logger.exception(msg, exc_info=exc)

    def critical(self, msg: object, exc_info: bool = False) -> None:
        self._logger.critical(msg, exc_info=exc_info)
