import psycopg2
from psycopg2.extras import RealDictCursor
from typing import Optional

#connection
DATABASE_URL = "postgresql://postgres:password@localhost/schemadb"

def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor(cursor_factory=RealDictCursor)
    try:
        yield cursor, conn
    finally:
        cursor.close()
        conn.close()