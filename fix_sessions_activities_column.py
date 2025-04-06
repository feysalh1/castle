"""
Fix the sessions table activities column to be TEXT instead of VARCHAR(1024)
"""

import os
import logging
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def fix_sessions_activities_column():
    """Alter the sessions table to change activities column to TEXT type"""
    # Get database URL from environment
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        logger.error("DATABASE_URL environment variable not set")
        return False
    
    try:
        # Create engine and connect to the database
        engine = create_engine(db_url)
        
        with engine.connect() as conn:
            # Check if the sessions table exists
            result = conn.execute(text(
                "SELECT EXISTS (SELECT FROM information_schema.tables "
                "WHERE table_name = 'sessions')"
            ))
            if not result.scalar():
                logger.error("Sessions table does not exist")
                return False
            
            # Alter the activities column to TEXT type
            conn.execute(text(
                "ALTER TABLE sessions ALTER COLUMN activities TYPE TEXT"
            ))
            
            # Commit the transaction
            conn.commit()
            
            logger.info("Successfully altered sessions.activities column to TEXT type")
            return True
    except Exception as e:
        logger.error(f"Error altering sessions.activities column: {str(e)}")
        return False

if __name__ == "__main__":
    fix_sessions_activities_column()