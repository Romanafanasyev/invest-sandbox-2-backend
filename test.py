from sqlalchemy import create_engine

# Replace these variables with your database connection details
POSTGRES_USER = 'postgres'
POSTGRES_PASSWORD = 'qwe'
POSTGRES_DB = 'invest'
POSTGRES_HOST = 'localhost'
POSTGRES_PORT = '5432'


# Database URL format for SQLAlchemy
DB_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'

try:
    engine = create_engine(DB_URL)
    connection = engine.connect()
    print("Connected to the database!")
    connection.close()
except Exception as e:
    print("Failed to connect to the database:", str(e))
