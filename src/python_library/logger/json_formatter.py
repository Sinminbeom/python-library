import json
import logging
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    RESERVED_KEYS = frozenset({"timestamp", "level", "logger", "thread_id", "message"})

    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc)
            .strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
            + "Z",
            "level": record.levelname,
            "logger": record.name,
            "thread_id": record.thread,
            "message": record.getMessage(),
        }

        if ctx := getattr(record, "ctx", None):
            payload.update(ctx)

        if record.exc_info:
            payload["exc_info"] = self.formatException(record.exc_info)

        return json.dumps(payload, ensure_ascii=False)
