import psycopg2
from psycopg2.extras import RealDictCursor 
from psycopg2 import extras
from typing import Optional

#connection
DATABASE_URL = "postgresql://postgres@localhost/schemadb"

def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor(cursor_factory=extras.DictCursor)
    #tuple_cursor = conn.cursor()
    try:
        yield cursor #, tuple_cursor
    finally:
        cursor.close()
        #tuple_cursor.close()
        conn.close()