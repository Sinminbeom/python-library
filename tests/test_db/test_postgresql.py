from datetime import datetime

from python_library.db.postgresql.postgresql_db_factory import PostgresqlDBFactory
from python_library.db.postgresql.postgresql_db_info_factory import PostgresqlDBInfoFactory


def test_execute_query():
    url = "postgresql://127.0.0.1:15432/data_lake?sslmode=require"
    user_name = "your-user-name"
    password = "your-password"
    db_factory = PostgresqlDBFactory(PostgresqlDBInfoFactory(url, user_name, password))
    db = db_factory.create_db()
    db.connect()
    db_rows = db.execute_query("select * from batch")
    for row in db_rows:
        print(row.get_as("update_time", datetime))
        print(row)
    pass


def test_execute_update():
    url = "postgresql://127.0.0.1:15432/data_lake?sslmode=require"
    user_name = "your-user-name"
    password = "your-password"
    db_factory = PostgresqlDBFactory(PostgresqlDBInfoFactory(url, user_name, password))
    db = db_factory.create_db()
    db.connect()
    # db.execute_update("update project set remarks = 'test2' where id = 2")
    db.execute_update("update project set remarks = 'test3' where id = %s", (2,))
    db.commit()


def test_execute_query_with_params():
    url = "postgresql://127.0.0.1:15432/data_lake?sslmode=require"
    user_name = "your-user-name"
    password = "your-password"
    db_factory = PostgresqlDBFactory(PostgresqlDBInfoFactory(url, user_name, password))
    db = db_factory.create_db()
    db.connect()
    db_rows = db.execute_query("select * from resource where name = %s", ("lcms",))
    for row in db_rows:
        print(row)
    pass
