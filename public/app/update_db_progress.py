"""
Database update script to add missing columns to the Progress table.
"""

import os
from app import app, db
from models import Progress

# Run this script to add missing columns to the Progress table
def add_missing_columns():
    """Add missing columns to the Progress table"""
    print("Adding missing columns to Progress table...")
    
    with app.app_context():
        from sqlalchemy import text
        
        # Check if completion_history column exists
        conn = db.engine.connect()
        result = conn.execute(text(
            "SELECT column_name FROM information_schema.columns "
            "WHERE table_name='progress' AND column_name='completion_history'"
        ))
        column_exists = result.fetchone() is not None
        conn.close()
        
        if not column_exists:
            print("Adding completion_history column...")
            conn = db.engine.connect()
            conn.execute(text(
                "ALTER TABLE progress ADD COLUMN completion_history VARCHAR(1024) DEFAULT '[]'"
            ))
            conn.commit()
            conn.close()
            print("completion_history column added.")
        else:
            print("completion_history column already exists.")
        
        # Check and add other potentially missing columns
        columns_to_check = [
            ('pages_read', 'INTEGER DEFAULT 0'),
            ('score', 'INTEGER'),
            ('difficulty_level', 'VARCHAR(32)'),
            ('is_favorite', 'BOOLEAN DEFAULT FALSE'),
            ('engagement_rating', 'INTEGER'),
            ('access_count', 'INTEGER DEFAULT 1'),
            ('last_session_duration', 'INTEGER'),
            ('average_session_time', 'FLOAT'),
            ('streak_count', 'INTEGER DEFAULT 0'),
            ('last_streak_date', 'DATE'),
            ('error_count', 'INTEGER DEFAULT 0'),
            ('last_error', 'VARCHAR(256)')
        ]
        
        for column_name, column_type in columns_to_check:
            conn = db.engine.connect()
            result = conn.execute(text(
                f"SELECT column_name FROM information_schema.columns "
                f"WHERE table_name='progress' AND column_name='{column_name}'"
            ))
            column_exists = result.fetchone() is not None
            conn.close()
            
            if not column_exists:
                print(f"Adding {column_name} column...")
                conn = db.engine.connect()
                conn.execute(text(
                    f"ALTER TABLE progress ADD COLUMN {column_name} {column_type}"
                ))
                conn.commit()
                conn.close()
                print(f"{column_name} column added.")
            else:
                print(f"{column_name} column already exists.")
    
    print("Database update completed.")

if __name__ == "__main__":
    add_missing_columns()