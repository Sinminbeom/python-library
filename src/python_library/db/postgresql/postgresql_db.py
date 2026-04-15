from typing import Optional, List

from python_library.db.db import IDB
from python_library.db.db_client import IDBClient
from python_library.db.db_row import IDBRow


class PostgresqlDB(IDB):
    def __init__(self):
        super().__init__()
        self._db_client: Optional[IDBClient] = None

    def connect(self) -> None:
        self._db_client.connect()
        pass

    def disconnect(self) -> None:
        self._db_client.disconnect()
        pass

    def execute_query(self, sql: str, params: tuple | None = None) -> List[IDBRow]:
        return self._db_client.execute_query(sql, params)

    def execute_update(self, sql: str, params: tuple | None = None) -> None:
        self._db_client.execute_update(sql, params)
        pass

    def commit(self) -> None:
        self._db_client.commit()
        pass

    def rollback(self) -> None:
        self._db_client.rollback()
        pass

    def set_db_client(self, db_client: IDBClient) -> None:
        self._db_client = db_client
        pass
