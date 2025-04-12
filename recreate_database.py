"""
Simple script to recreate the PostgreSQL database.
This is useful if the database connection is failing due to SSL issues.
"""
import os
import time
from dotenv import load_dotenv
import sqlalchemy as sa
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

# Get database connection details from environment variables
database_url = os.environ.get("DATABASE_URL")

if not database_url or not database_url.startswith('postgresql'):
    print("ERROR: This script is for PostgreSQL databases only.")
    print(f"Current DATABASE_URL: {database_url}")
    exit(1)

print(f"Attempting to reconnect to PostgreSQL database...")

# Try different SSL modes
ssl_modes = ["require", "prefer", "allow", "disable"]

for ssl_mode in ssl_modes:
    try:
        print(f"Trying with sslmode={ssl_mode}...")
        
        # Create engine with specific SSL mode
        engine = create_engine(
            database_url,
            echo=True,
            connect_args={
                "options": "-c timezone=utc",
                "sslmode": ssl_mode
            }
        )
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print(f"Connection successful with sslmode={ssl_mode}!")
            print("Database is available.")
            
            # Create a test table to verify write access
            try:
                conn.execute(text("CREATE TABLE IF NOT EXISTS connection_test (id SERIAL PRIMARY KEY, test_time TIMESTAMP DEFAULT NOW())"))
                conn.execute(text("INSERT INTO connection_test (test_time) VALUES (NOW())"))
                conn.commit()
                print("Write access confirmed.")
            except Exception as e:
                print(f"Warning: Could not write to database: {str(e)}")
            
            break
    except Exception as e:
        print(f"Connection failed with sslmode={ssl_mode}: {str(e)}")
        if ssl_mode != ssl_modes[-1]:
            print("Trying next SSL mode...")
            time.sleep(1)  # Short delay before next attempt
        else:
            print("All SSL modes failed. Please check your database configuration.")
            exit(1)

print("\nTo update your application, add the following to your SQLALCHEMY_ENGINE_OPTIONS:")
print(f"""{{
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "connect_args": {{
        "options": "-c timezone=utc",
        "sslmode": "{ssl_mode}"
    }}
}}""")

print("\nDatabase connection test completed successfully!")