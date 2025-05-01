import psycopg2

DATABASE_URL = "postgresql://postgres:E};jF>5aetk5V@budgetbridge-db.c9e0iuy0kl1n.us-east-2.rds.amazonaws.com/budgetbridge"


def get_db():
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()  # Use the default cursor (not RealDictCursor)
    try:
        yield cursor, conn  # Yield both cursor and conn
    finally:
        cursor.close()  # Ensure cursor is closed after use
        conn.close()  # Ensure connection is closed after use