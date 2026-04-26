"""
Create database tables using SQLAlchemy db.create_all()
This is simpler than running migrations and works even with slow connections.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import app and db
from app import create_app
from app.extensions import db
from app.models import User, Analysis, MonthlyReport, ChatMessage, DailyLog

print("🔄 Creating HealthAI database tables...")
print("=" * 60)

# Create Flask app
app = create_app('development')

# Create all tables
with app.app_context():
    try:
        print("\n📊 Creating tables in database...")
        db.create_all()
        print("✅ All tables created successfully!")

        # List all tables
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        print(f"\n📋 Created {len(tables)} tables:")
        for table in sorted(tables):
            print(f"   ✓ {table}")

        # Create alembic_version table if it doesn't exist
        if 'alembic_version' not in tables:
            print("\n📝 Creating alembic_version table for migration tracking...")
            db.session.execute(db.text("""
                CREATE TABLE IF NOT EXISTS alembic_version (
                    version_num VARCHAR(32) NOT NULL PRIMARY KEY
                );
            """))
            db.session.execute(db.text("""
                INSERT INTO alembic_version (version_num) VALUES ('a8943dee2b30')
                ON CONFLICT (version_num) DO NOTHING;
            """))
            db.session.commit()
            print("   ✓ alembic_version")

        print("\n🎉 Database setup complete!")
        print("=" * 60)
        print("\n✅ Your database is ready to use!")
        print("\nYou can now:")
        print("  1. Start your Flask backend: python run.py")
        print("  2. Use the API endpoints to save/retrieve data")
        print("  3. Run verify_tables.py to double-check")

    except Exception as e:
        print(f"\n❌ Error creating tables: {e}")
        print("\n💡 Troubleshooting:")
        print("  1. Check DATABASE_URL in .env is correct")
        print("  2. Verify your Neon database is active")
        print("  3. Try using Neon SQL Editor instead (see create_tables.sql)")
        import traceback
        traceback.print_exc()
        sys.exit(1)
