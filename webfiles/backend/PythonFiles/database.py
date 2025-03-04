import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional

#connection
DATABASE_URL = "postgresql://postgres:password@localhost/schemadb"

def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    tuple_cursor = conn.cursor()
    try:
        yield cursor, tuple_cursor, conn
    finally:
        cursor.close()
        tuple_cursor.close()
        conn.close()