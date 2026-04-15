from python_library.db.db import IDB
from python_library.db.db_factory import IDBFactory
from python_library.db.db_info_factory import IDBInfoFactory
from python_library.db.postgresql.postgresql_db import PostgresqlDB


class PostgresqlDBFactory(IDBFactory):
    def __init__(self, db_info_factory: IDBInfoFactory):
        super().__init__()
        self._db_info_factory = db_info_factory

    def create_db(self) -> IDB:
        db = PostgresqlDB()
        db.set_db_client(self._db_info_factory.create_db_client())
        return db
