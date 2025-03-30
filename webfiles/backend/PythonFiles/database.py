import psycopg2
from contextlib import contextmanager

DATABASE_URL = "postgresql://postgres:MarineCorps1371!!@localhost/schemastoredb"


def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()  # Use the default cursor (not RealDictCursor)
    try:
        yield cursor, conn  # Yield both cursor and conn
    finally:
        cursor.close()  # Ensure cursor is closed after use
        conn.close()  # Ensure connection is closed after use