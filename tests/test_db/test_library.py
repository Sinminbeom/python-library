from psycopg import connect

from python_library.db.db_row import DBRow
from typing import List

conn_str = "postgresql://127.0.0.1:15432/data_lake?sslmode=require&connect_timeout=3"

user_name = "your-user-name"
password = "your-password"


def test_psycopg_query():
    db_rows: List[DBRow] = list()

    conn = connect(conn_str, user=user_name, password=password)

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM member;")

        if cursor.description is None:
            return db_rows

        column_names = [desc[0] for desc in cursor.description]

        rows = cursor.fetchall()

        for row in rows:
            db_row = DBRow()
            for column_index in range(len(row)):
                db_row.push(column_names[column_index], row[column_index])
            db_rows.append(db_row)

    pass
