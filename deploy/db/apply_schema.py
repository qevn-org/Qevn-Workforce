import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("ERROR: DATABASE_URL not found in environment or .env file.")
    sys.exit(1)

# Ensure DATABASE_URL is psycopg2 compatible
if DATABASE_URL.startswith("postgresql://") and not DATABASE_URL.startswith("postgresql+psycopg2://"):
    # SQLAlchemy v2 needs psycopg2 driver explicitly or implicitly
    pass

print(f"Connecting to database...")

try:
    engine = create_engine(DATABASE_URL)
    
    # Read schema file
    schema_path = os.path.join(os.path.dirname(__file__), "init.sql")
    if not os.path.exists(schema_path):
        # Check relative to cwd
        schema_path = "deploy/db/init.sql"
        
    print(f"Reading schema from {schema_path}...")
    with open(schema_path, "r", encoding="utf-8") as f:
        sql_commands = f.read()

    # PostgreSQL can execute multi-statement SQL strings using text()
    print("Applying database schema to Railway PostgreSQL...")
    with engine.connect() as connection:
        with connection.begin():
            # Split commands by semicolon or execute all at once
            # execute() can run multiple statements at once in PostgreSQL
            connection.execute(text(sql_commands))
            
    print("SUCCESS: Database schema applied successfully to Railway PostgreSQL!")
except Exception as e:
    print(f"ERROR: Failed to apply schema: {str(e)}")
    sys.exit(1)
