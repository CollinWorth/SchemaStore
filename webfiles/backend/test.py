import psycopg2

DATABASE_URL = "postgresql://postgres:@localhost:5432/SchemaDB"

try:
    #connect to postgre server
    conn = pycopg2.connect(DATABASE_URL)

    cursor = conn.cursor()

    cursor.execute("SELECT version();")
    db_version = cursor.ftchone()

    print(f"Connected to the database")

    cursor.close()
    conn.close()

except Exception as error:
    print(f"Error while connecting to postgre server")

