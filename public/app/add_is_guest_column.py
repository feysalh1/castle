"""
Add is_guest column to the parents table
"""
from app import app, db

def add_is_guest_column():
    """Add is_guest column to the parents table"""
    with app.app_context():
        # Using raw SQL for direct column addition
        try:
            db.session.execute(db.text("ALTER TABLE parents ADD COLUMN is_guest BOOLEAN DEFAULT FALSE"))
            db.session.commit()
            print("Successfully added is_guest column to parents table")
        except Exception as e:
            db.session.rollback()
            print(f"Error adding is_guest column: {e}")

if __name__ == "__main__":
    add_is_guest_column()