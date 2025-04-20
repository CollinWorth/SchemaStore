import psycopg2
from psycopg2.extras import RealDictCursor 

DATABASE_URL = "postgresql://postgres:postgres@localhost/schemastoredb"

def get_db():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        print("Database connection successful!")  
        yield cursor
    except Exception as e:
        print(f"Database connection failed: {e}")  
    finally:
        cursor.close()
        conn.close()