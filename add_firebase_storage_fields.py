"""
Database migration script to add Firebase Storage fields to the Photo model.
"""
import os
import sys
import logging
import sqlalchemy
from sqlalchemy import inspect, text

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def add_firebase_storage_fields():
    """Add Firebase Storage columns to the Photo table if they don't exist"""
    # Get the database URL from environment variable
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        logger.error("DATABASE_URL environment variable not set")
        return
        
    logger.info(f"Connecting to database: {database_url}")
    
    # Connect to the database directly
    engine = sqlalchemy.create_engine(database_url)
    conn = engine.connect()
    
    try:
        # Check if the columns already exist
        inspector = inspect(engine)
        columns = [column['name'] for column in inspector.get_columns('photos')]
        
        # Add each column if it doesn't exist
        if 'storage_type' not in columns:
            logger.info("Adding 'storage_type' column to photos table")
            try:
                conn.execute(text("ALTER TABLE photos ADD COLUMN storage_type VARCHAR(20) DEFAULT 'local' NOT NULL"))
                logger.info("Added 'storage_type' column successfully")
            except Exception as e:
                logger.error(f"Error adding 'storage_type' column: {e}")
        else:
            logger.info("'storage_type' column already exists")
        
        if 'firebase_storage_path' not in columns:
            logger.info("Adding 'firebase_storage_path' column to photos table")
            try:
                conn.execute(text("ALTER TABLE photos ADD COLUMN firebase_storage_path VARCHAR(256)"))
                logger.info("Added 'firebase_storage_path' column successfully")
            except Exception as e:
                logger.error(f"Error adding 'firebase_storage_path' column: {e}")
        else:
            logger.info("'firebase_storage_path' column already exists")
            
        if 'firebase_thumbnail_path' not in columns:
            logger.info("Adding 'firebase_thumbnail_path' column to photos table")
            try:
                conn.execute(text("ALTER TABLE photos ADD COLUMN firebase_thumbnail_path VARCHAR(256)"))
                logger.info("Added 'firebase_thumbnail_path' column successfully")
            except Exception as e:
                logger.error(f"Error adding 'firebase_thumbnail_path' column: {e}")
        else:
            logger.info("'firebase_thumbnail_path' column already exists")
        
        if 'firebase_url' not in columns:
            logger.info("Adding 'firebase_url' column to photos table")
            try:
                conn.execute(text("ALTER TABLE photos ADD COLUMN firebase_url VARCHAR(512)"))
                logger.info("Added 'firebase_url' column successfully")
            except Exception as e:
                logger.error(f"Error adding 'firebase_url' column: {e}")
        else:
            logger.info("'firebase_url' column already exists")
        
        if 'firebase_thumbnail_url' not in columns:
            logger.info("Adding 'firebase_thumbnail_url' column to photos table")
            try:
                conn.execute(text("ALTER TABLE photos ADD COLUMN firebase_thumbnail_url VARCHAR(512)"))
                logger.info("Added 'firebase_thumbnail_url' column successfully")
            except Exception as e:
                logger.error(f"Error adding 'firebase_thumbnail_url' column: {e}")
        else:
            logger.info("'firebase_thumbnail_url' column already exists")
            
    finally:
        # Make sure the connection is closed
        conn.close()
        engine.dispose()

if __name__ == "__main__":
    logger.info("Starting Firebase Storage fields migration...")
    add_firebase_storage_fields()
    logger.info("Migration completed.")