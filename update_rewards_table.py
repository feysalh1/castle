"""
Script to update the Rewards table to add missing columns.
"""
import os
import logging
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get database URL from environment
DATABASE_URL = os.environ.get('DATABASE_URL')

def update_rewards_table():
    """Add missing columns to Rewards table"""
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # Check if columns exist
        result = conn.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'rewards'
        """))
        existing_columns = [row[0] for row in result]
        
        # Add missing columns
        missing_columns = []
        if 'source_type' not in existing_columns:
            missing_columns.append("ALTER TABLE rewards ADD COLUMN source_type VARCHAR(32)")
            logger.info("Need to add source_type column")
            
        if 'source_id' not in existing_columns:
            missing_columns.append("ALTER TABLE rewards ADD COLUMN source_id VARCHAR(64)")
            logger.info("Need to add source_id column")
            
        if 'achievement_level' not in existing_columns:
            missing_columns.append("ALTER TABLE rewards ADD COLUMN achievement_level VARCHAR(32)")
            logger.info("Need to add achievement_level column")
            
        if 'points_value' not in existing_columns:
            missing_columns.append("ALTER TABLE rewards ADD COLUMN points_value INTEGER DEFAULT 1")
            logger.info("Need to add points_value column")
            
        if 'showcase_priority' not in existing_columns:
            missing_columns.append("ALTER TABLE rewards ADD COLUMN showcase_priority INTEGER DEFAULT 0")
            logger.info("Need to add showcase_priority column")
        
        # Execute ALTER TABLE statements
        for alter_statement in missing_columns:
            logger.info(f"Executing: {alter_statement}")
            conn.execute(text(alter_statement))
            
        # Commit the transaction
        conn.commit()
        
        logger.info("Rewards table update complete")

if __name__ == "__main__":
    logger.info("Starting Rewards table update")
    update_rewards_table()
    logger.info("Rewards table update script completed")