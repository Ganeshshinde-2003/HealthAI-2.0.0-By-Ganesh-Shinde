"""Test database connection."""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

database_url = os.environ.get('DATABASE_URL')
print(f"Database URL exists: {database_url is not None}")

if database_url:
    try:
        engine = create_engine(database_url)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("Database connection successful!")
            print(f"Result: {result.fetchone()}")
    except Exception as e:
        print(f"Database connection failed: {e}")
else:
    print("DATABASE_URL not set in environment")
