"""
Database schema update script for Children's Castle application.
This script will add new fields to existing tables.
"""

import os
import sys
from datetime import datetime
from sqlalchemy import create_engine, MetaData, Table, Column, Boolean, Integer, String, Float, Date
from sqlalchemy.ext.declarative import declarative_base

# Setup connection to database
db_url = os.environ.get('DATABASE_URL')
if not db_url:
    print("DATABASE_URL environment variable not found. Please set it before running this script.")
    sys.exit(1)

engine = create_engine(db_url)
metadata = MetaData()
metadata.reflect(bind=engine)

# Check if the tables exist
if 'progress' not in metadata.tables or 'sessions' not in metadata.tables:
    print("Required tables not found in database. Make sure the database is properly initialized.")
    sys.exit(1)

# Get reference to the existing tables
progress_table = metadata.tables['progress']
sessions_table = metadata.tables['sessions']

# Define new columns to add to Progress table
progress_columns = [
    Column('is_favorite', Boolean, default=False),
    Column('engagement_rating', Integer),
    Column('access_count', Integer, default=1),
    Column('last_session_duration', Integer),
    Column('average_session_time', Float),
    Column('streak_count', Integer, default=0),
    Column('last_streak_date', Date),
    Column('error_count', Integer, default=0),
    Column('last_error', String(256))
]

# Define new columns to add to Session table (if needed)
session_columns = [
    Column('ip_address', String(45)),
    Column('user_agent', String(255)),
    Column('device_type', String(32))
]

def add_columns(engine, table_name, columns):
    """Add columns to a table if they don't already exist"""
    conn = engine.connect()
    
    for column in columns:
        column_name = column.name
        
        # Check if column already exists
        if column_name not in metadata.tables[table_name].columns:
            print(f"Adding column '{column_name}' to table '{table_name}'")
            
            # Determine the appropriate SQL type for the column
            if isinstance(column.type, Boolean):
                type_name = "BOOLEAN"
                default_value = "DEFAULT FALSE" if column.default is not None and not column.default.is_callable else ""
            elif isinstance(column.type, Integer):
                type_name = "INTEGER"
                default_value = f"DEFAULT {column.default.arg}" if column.default is not None and not column.default.is_callable else ""
            elif isinstance(column.type, Float):
                type_name = "FLOAT"
                default_value = f"DEFAULT {column.default.arg}" if column.default is not None and not column.default.is_callable else ""
            elif isinstance(column.type, Date):
                type_name = "DATE"
                default_value = ""
            else:  # String or other
                length = getattr(column.type, 'length', None)
                type_name = f"VARCHAR({length})" if length else "TEXT"
                default_value = ""
            
            # Generate and execute the ALTER TABLE statement
            sql = f"ALTER TABLE {table_name} ADD COLUMN IF NOT EXISTS {column_name} {type_name} {default_value}"
            try:
                from sqlalchemy.sql import text
                conn.execute(text(sql))
                conn.commit()
            except Exception as e:
                print(f"Error adding column '{column_name}': {e}")
        else:
            print(f"Column '{column_name}' already exists in table '{table_name}'")
    
    conn.close()

def main():
    """Main function to update the database schema"""
    print("Starting database schema update...")
    
    try:
        # Add new columns to Progress table
        add_columns(engine, 'progress', progress_columns)
        
        # Add new columns to Session table
        add_columns(engine, 'sessions', session_columns)
        
        print("Database schema update completed successfully!")
    except Exception as e:
        print(f"Error updating database schema: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()