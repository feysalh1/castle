"""
Add firebase_uid column to parents table for Firebase Authentication.
"""
from app import app, db
from sqlalchemy import text

def add_firebase_uid_column():
    """Add firebase_uid column to parents table."""
    print("Adding firebase_uid column to parents table...")
    
    with app.app_context():
        # Check if column already exists
        with db.engine.connect() as conn:
            result = conn.execute(text(
                "SELECT column_name FROM information_schema.columns "
                "WHERE table_name='parents' AND column_name='firebase_uid'"
            )).fetchone()
            
            if result is None:
                # Add the column
                conn.execute(text(
                    "ALTER TABLE parents ADD COLUMN firebase_uid VARCHAR(128) UNIQUE"
                ))
                conn.commit()
                print("firebase_uid column added successfully")
            else:
                print("firebase_uid column already exists")
            
            # Make password_hash nullable (for Firebase auth)
            conn.execute(text(
                "ALTER TABLE parents ALTER COLUMN password_hash DROP NOT NULL"
            ))
            conn.commit()
            print("Made password_hash column nullable")

if __name__ == "__main__":
    add_firebase_uid_column()