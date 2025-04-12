import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables
load_dotenv()

# Get database connection details from environment variables
db_url = os.environ.get('DATABASE_URL')

if not db_url:
    print("Error: DATABASE_URL environment variable is not set.")
    sys.exit(1)

try:
    # Create database engine
    engine = create_engine(db_url)
    
    # Create a connection
    with engine.connect() as conn:
        # Check if the column already exists
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT 1 
                FROM information_schema.columns 
                WHERE table_name = 'parents' 
                AND column_name = 'display_name'
            );
        """))
        column_exists = result.scalar()
        
        if column_exists:
            print("The 'display_name' column already exists in the 'parents' table.")
        else:
            # Add display_name column
            conn.execute(text("""
                ALTER TABLE parents 
                ADD COLUMN display_name VARCHAR(128);
            """))
            conn.commit()
            print("Successfully added 'display_name' column to 'parents' table.")
        
        print("Database update completed successfully!")
        
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)