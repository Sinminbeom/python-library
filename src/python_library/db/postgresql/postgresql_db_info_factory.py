from python_library.db.db_client import IDBClient
from python_library.db.db_info_factory import IDBInfoFactory
from python_library.db.postgresql.postgresql_db_client import PostgresqlDBClient


class PostgresqlDBInfoFactory(IDBInfoFactory):
    def __init__(self, url: str, user_name: str, password: str):
        super().__init__()
        self._url = url
        self._user_name = user_name
        self._password = password

    def create_db_client(self) -> IDBClient:
        db_client = PostgresqlDBClient(self._url, self._user_name, self._password)
        return db_client
