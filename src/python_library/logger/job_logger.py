import logging
import sys
from enum import Enum
from typing import Optional

from python_library.logger.json_formatter import JsonFormatter


class JobStatus(str, Enum):
    STARTED = "STARTED"
    DONE = "DONE"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


class JobLogger:
    def __init__(self, service: str, job_run_id: Optional[str] = None):
        base_ctx = {k: v for k, v in {"job_run_id": job_run_id}.items() if v is not None}

        inner = logging.getLogger(service)
        inner.setLevel(logging.DEBUG)
        inner.handlers.clear()
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        inner.addHandler(handler)
        inner.propagate = False

        class _Adapter(logging.LoggerAdapter):
            def process(self, msg: str, kwargs: dict) -> tuple:
                call_ctx: dict = kwargs.pop("ctx", {})
                kwargs.setdefault("extra", {})["ctx"] = {**base_ctx, **call_ctx}
                return msg, kwargs

        self._adapter = _Adapter(inner, {})

    def _build_ctx(self, step: Optional[str], status: Optional[str], extra: dict) -> dict:
        conflict = JsonFormatter.RESERVED_KEYS & extra.keys()
        if conflict:
            raise ValueError(f"Reserved keys cannot be used in extra: {conflict}")
        return {k: v for k, v in {"step": step, "status": status, **extra}.items() if v is not None}

    def info(self, msg: str, step: Optional[str] = None, status: Optional[JobStatus] = None, exc_info: bool = False, **extra) -> None:
        self._adapter.info(msg, exc_info=exc_info, ctx=self._build_ctx(step, status, extra))

    def debug(self, msg: str, step: Optional[str] = None, status: Optional[JobStatus] = None, exc_info: bool = False, **extra) -> None:
        self._adapter.debug(msg, exc_info=exc_info, ctx=self._build_ctx(step, status, extra))

    def warning(self, msg: str, step: Optional[str] = None, status: Optional[JobStatus] = None, exc_info: bool = False, **extra) -> None:
        self._adapter.warning(msg, exc_info=exc_info, ctx=self._build_ctx(step, status, extra))

    def error(self, msg: str, step: Optional[str] = None, status: Optional[JobStatus] = None, exc_info: bool = False, **extra) -> None:
        self._adapter.error(msg, exc_info=exc_info, ctx=self._build_ctx(step, status, extra))

    def critical(self, msg: str, step: Optional[str] = None, status: Optional[JobStatus] = None, exc_info: bool = False, **extra) -> None:
        self._adapter.critical(msg, exc_info=exc_info, ctx=self._build_ctx(step, status, extra))
