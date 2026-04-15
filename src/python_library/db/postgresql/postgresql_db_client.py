from typing import Optional, List, cast, Callable, Any
from psycopg import connect, Connection

from python_library.db.db_client import IDBClient
from python_library.db.db_row import IDBRow, DBRow


class PostgresqlDBClient(IDBClient):
    def __init__(self, url: str, user_name: str, password: str) -> None:
        super().__init__()
        self._url = url
        self._user_name = user_name
        self._password = password

        self._conn: Optional[Connection] = None

    def connect(self) -> None:
        self._conn = connect(self._url, user=self._user_name, password=self._password)
        pass

    def disconnect(self) -> None:
        self._conn.close()
        self._conn = None
        pass

    def execute_query(self, sql: str, params: tuple | None = None) -> List[IDBRow]:
        db_rows: List[IDBRow] = list()

        try:
            with self._conn.cursor() as cursor:
                cast(Callable[..., Any], cursor.execute)(sql, params)

                if cursor.description is None:
                    return db_rows

                column_names = [desc.name for desc in cursor.description]

                rows = cursor.fetchall()
                for row in rows:
                    db_row = DBRow()
                    for i, value in enumerate(row):
                        db_row.push(column_names[i], value)
                    db_rows.append(db_row)

            return db_rows
        except Exception as e:
            raise e

    def execute_update(self, sql: str, params: tuple | None = None) -> None:
        with self._conn.cursor() as cursor:
            cast(Callable[..., Any], cursor.execute)(sql, params)
        pass

    def commit(self) -> None:
        try:
            self._conn.commit()
        except Exception as e:
            raise e

    def rollback(self) -> None:
        try:
            self._conn.rollback()
        except Exception as e:
            raise e
