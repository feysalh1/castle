"""
Database migration script to add Firebase Storage fields to the Photo model.
"""
import os
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the app and models
from app import app, db
from models import Photo

def add_firebase_storage_fields():
    """Add Firebase Storage columns to the Photo table if they don't exist"""
    with app.app_context():
        # Check if columns exist
        columns = [c.name for c in Photo.__table__.columns]
        
        if 'storage_type' not in columns:
            logger.info("Adding 'storage_type' column to Photo table")
            try:
                db.engine.execute('ALTER TABLE photos ADD COLUMN storage_type VARCHAR(20) DEFAULT \'local\' NOT NULL')
                logger.info("Added 'storage_type' column successfully")
            except Exception as e:
                logger.error(f"Error adding 'storage_type' column: {e}")

        if 'firebase_storage_path' not in columns:
            logger.info("Adding 'firebase_storage_path' column to Photo table")
            try:
                db.engine.execute('ALTER TABLE photos ADD COLUMN firebase_storage_path VARCHAR(256)')
                logger.info("Added 'firebase_storage_path' column successfully")
            except Exception as e:
                logger.error(f"Error adding 'firebase_storage_path' column: {e}")

        if 'firebase_thumbnail_path' not in columns:
            logger.info("Adding 'firebase_thumbnail_path' column to Photo table")
            try:
                db.engine.execute('ALTER TABLE photos ADD COLUMN firebase_thumbnail_path VARCHAR(256)')
                logger.info("Added 'firebase_thumbnail_path' column successfully")
            except Exception as e:
                logger.error(f"Error adding 'firebase_thumbnail_path' column: {e}")

        if 'firebase_url' not in columns:
            logger.info("Adding 'firebase_url' column to Photo table")
            try:
                db.engine.execute('ALTER TABLE photos ADD COLUMN firebase_url VARCHAR(512)')
                logger.info("Added 'firebase_url' column successfully")
            except Exception as e:
                logger.error(f"Error adding 'firebase_url' column: {e}")

        if 'firebase_thumbnail_url' not in columns:
            logger.info("Adding 'firebase_thumbnail_url' column to Photo table")
            try:
                db.engine.execute('ALTER TABLE photos ADD COLUMN firebase_thumbnail_url VARCHAR(512)')
                logger.info("Added 'firebase_thumbnail_url' column successfully")
            except Exception as e:
                logger.error(f"Error adding 'firebase_thumbnail_url' column: {e}")

if __name__ == "__main__":
    logger.info("Starting Firebase Storage fields migration...")
    add_firebase_storage_fields()
    logger.info("Migration completed.")