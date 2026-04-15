from typing import Optional

from python_library.logger.base_conf_logger import BaseConfLogger


class AccessLogger(BaseConfLogger):
    def event(
        self,
        ts: str,
        client_ip: str,
        method: str,
        path: str,
        status: int,
        latency_ms: int,
        user_agent: Optional[str] = None,
        trace_id: Optional[str] = None,
        query: Optional[str] = None,
        host: Optional[str] = None,
        referer: Optional[str] = None,
    ) -> None:
        ctx = {
            k: v
            for k, v in {
                "timestamp": ts,
                "client_ip": client_ip,
                "method": method,
                "path": path,
                "status_code": status,
                "latency_ms": latency_ms,
                "user_agent": user_agent,
                "trace_id": trace_id,
                "query": query,
                "host": host,
                "referer": referer,
            }.items()
            if v is not None
        }
        self._logger.info("access_log", extra={"ctx": ctx})
