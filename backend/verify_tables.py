"""Verify database tables were created."""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect

load_dotenv()

database_url = os.environ.get('DATABASE_URL')

if not database_url:
    print("ERROR: DATABASE_URL not set")
    exit(1)

try:
    engine = create_engine(database_url)
    inspector = inspect(engine)

    tables = inspector.get_table_names()

    print(f"Found {len(tables)} tables in database:")
    for table in sorted(tables):
        print(f"  - {table}")

    expected_tables = ['users', 'analyses', 'monthly_reports', 'chat_messages', 'daily_logs', 'alembic_version']
    missing = [t for t in expected_tables if t not in tables]

    if missing:
        print(f"\nMissing tables: {missing}")
    else:
        print("\n✓ All expected tables exist!")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
