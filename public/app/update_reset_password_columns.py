"""
Add reset password columns to the parents table
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment variables
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    print("ERROR: DATABASE_URL environment variable not set.")
    sys.exit(1)

def add_reset_password_columns():
    """Add reset_password_token and reset_token_expires columns to parents table"""
    try:
        # Create database engine
        engine = create_engine(DATABASE_URL)
        
        # Connect to the database
        with engine.connect() as conn:
            # Check if columns already exist
            check_query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'parents' 
                AND column_name IN ('reset_password_token', 'reset_token_expires')
            """)
            
            existing_columns = [row[0] for row in conn.execute(check_query)]
            
            # Add reset_password_token column if it doesn't exist
            if 'reset_password_token' not in existing_columns:
                print("Adding reset_password_token column to parents table...")
                conn.execute(text("""
                    ALTER TABLE parents 
                    ADD COLUMN reset_password_token VARCHAR(256)
                """))
            else:
                print("Column reset_password_token already exists.")
            
            # Add reset_token_expires column if it doesn't exist
            if 'reset_token_expires' not in existing_columns:
                print("Adding reset_token_expires column to parents table...")
                conn.execute(text("""
                    ALTER TABLE parents 
                    ADD COLUMN reset_token_expires TIMESTAMP
                """))
            else:
                print("Column reset_token_expires already exists.")
            
            # Commit the transaction
            conn.commit()
            
            print("Database schema update completed successfully.")
            
    except Exception as e:
        print(f"ERROR: Failed to update database schema: {e}")
        sys.exit(1)

if __name__ == "__main__":
    add_reset_password_columns()