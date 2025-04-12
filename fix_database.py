"""
Script to fix database connection issues in Replit environment.
This script will:
1. Check if DATABASE_URL is set and valid
2. Test database connection with different SSL modes
3. Update the main.py file with the correct SSL mode
"""
import os
import time
import re
from dotenv import load_dotenv
import sqlalchemy as sa
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

# Get database connection details from environment variables
database_url = os.environ.get("DATABASE_URL")

print("🔍 Database Connection Fixer 🔍")
print("==============================")

if not database_url:
    print("❌ ERROR: DATABASE_URL environment variable is not set.")
    exit(1)

if not database_url.startswith('postgresql'):
    print(f"❌ ERROR: This script is for PostgreSQL databases only.")
    print(f"Current DATABASE_URL: {database_url}")
    exit(1)

print(f"✅ DATABASE_URL is set and is a PostgreSQL connection.")
print("🔄 Attempting to connect to PostgreSQL database...")

# Try different SSL modes
ssl_modes = ["require", "prefer", "allow", "disable"]
working_ssl_mode = None

for ssl_mode in ssl_modes:
    try:
        print(f"🔄 Trying with sslmode={ssl_mode}...")
        
        # Create engine with specific SSL mode
        engine = create_engine(
            database_url,
            connect_args={
                "options": "-c timezone=utc",
                "sslmode": ssl_mode
            }
        )
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print(f"✅ Connection successful with sslmode={ssl_mode}!")
            
            # Create a test table to verify write access
            try:
                conn.execute(text("CREATE TABLE IF NOT EXISTS connection_test (id SERIAL PRIMARY KEY, test_time TIMESTAMP DEFAULT NOW())"))
                conn.execute(text("INSERT INTO connection_test (test_time) VALUES (NOW())"))
                conn.commit()
                print("✅ Write access confirmed.")
                working_ssl_mode = ssl_mode
                break
            except Exception as e:
                print(f"⚠️ Warning: Could not write to database: {str(e)}")
                working_ssl_mode = ssl_mode
                break
    except Exception as e:
        print(f"❌ Connection failed with sslmode={ssl_mode}: {str(e)}")
        if ssl_mode != ssl_modes[-1]:
            print("⏳ Trying next SSL mode...")
            time.sleep(1)  # Short delay before next attempt
        else:
            print("❌ All SSL modes failed. Please check your database configuration.")
            exit(1)

if working_ssl_mode:
    print(f"\n✅ Found working SSL mode: {working_ssl_mode}")
    
    # Update main.py with the correct SSL mode
    try:
        with open('main.py', 'r') as file:
            content = file.read()
        
        # Define the pattern to find the SQLALCHEMY_ENGINE_OPTIONS configuration
        pattern = r'app\.config\["SQLALCHEMY_ENGINE_OPTIONS"\]\s*=\s*{[^}]*}'
        
        # Define the replacement with the correct SSL mode
        replacement = f'''app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {{
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "connect_args": {{
        "options": "-c timezone=utc",
        "sslmode": "{working_ssl_mode}"
    }} if database_url and database_url.startswith('postgresql') else {{}}
}}'''
        
        # Replace the pattern with the new configuration
        if re.search(pattern, content):
            new_content = re.sub(pattern, replacement, content)
            with open('main.py', 'w') as file:
                file.write(new_content)
            print("✅ Updated main.py with the correct SSL mode configuration.")
        else:
            print("❌ Could not find SQLALCHEMY_ENGINE_OPTIONS in main.py to update.")
    except Exception as e:
        print(f"❌ Error updating main.py: {str(e)}")

print("\n🚀 Database connection fix completed!")
print("Please restart your application for the changes to take effect.")