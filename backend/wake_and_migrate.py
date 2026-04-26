"""Wake up Neon database and run migrations."""
import os
import time
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import subprocess

load_dotenv()

database_url = os.environ.get('DATABASE_URL')

if not database_url:
    print("❌ ERROR: DATABASE_URL not set in .env")
    exit(1)

print("🔄 Attempting to connect to Neon database...")
print("   (This will wake up the database if it's sleeping)")

try:
    # Create engine with longer timeout
    engine = create_engine(
        database_url,
        connect_args={
            'connect_timeout': 60,  # 60 second timeout
            'options': '-c statement_timeout=60000'
        },
        pool_pre_ping=True
    )

    print("🔌 Connecting to database...")
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        print("✅ Database connection successful!")
        print(f"   Result: {result.fetchone()}")

        # Check if tables exist
        check_tables = connection.execute(text("""
            SELECT tablename FROM pg_tables
            WHERE schemaname = 'public'
            ORDER BY tablename
        """))
        existing_tables = [row[0] for row in check_tables]

        if existing_tables:
            print(f"\n📊 Found {len(existing_tables)} existing tables:")
            for table in existing_tables:
                print(f"   - {table}")
        else:
            print("\n📊 No tables found yet (need to run migration)")

    # Now run the migration
    print("\n🚀 Running Alembic migration...")
    result = subprocess.run(
        ['venv/bin/alembic', 'upgrade', 'head'],
        capture_output=True,
        text=True,
        timeout=120
    )

    if result.returncode == 0:
        print("✅ Migration completed successfully!")
        print(result.stdout)
    else:
        print("❌ Migration failed:")
        print(result.stderr)
        exit(1)

    # Verify tables were created
    print("\n🔍 Verifying tables...")
    with engine.connect() as connection:
        check_tables = connection.execute(text("""
            SELECT tablename FROM pg_tables
            WHERE schemaname = 'public'
            ORDER BY tablename
        """))
        tables = [row[0] for row in check_tables]

        print(f"\n✅ Found {len(tables)} tables:")
        for table in tables:
            print(f"   ✓ {table}")

        expected = ['users', 'analyses', 'monthly_reports', 'chat_messages', 'daily_logs', 'alembic_version']
        missing = [t for t in expected if t not in tables]

        if missing:
            print(f"\n⚠️  Missing tables: {missing}")
        else:
            print("\n🎉 All tables created successfully!")

except Exception as e:
    print(f"❌ Error: {e}")
    print("\n💡 Troubleshooting tips:")
    print("1. Check your Neon dashboard - is the database running?")
    print("2. Verify DATABASE_URL in .env is correct")
    print("3. Make sure your Neon database hasn't been deleted")
    print("4. Try running this script again (it will wake up sleeping database)")
    import traceback
    traceback.print_exc()
    exit(1)
