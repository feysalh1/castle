from werkzeug.security import generate_password_hash
from app import db
from models import Parent

def reset_admin_password():
    """Reset the admin password (first parent account)"""
    parent = Parent.query.filter_by(id=1).first()
    if parent:
        new_password = "admin123"  # Simple password for testing
        parent.password_hash = generate_password_hash(new_password)
        db.session.commit()
        print(f"Password for user {parent.username} (ID: {parent.id}) has been reset to {new_password}")
    else:
        print("Admin user not found")

if __name__ == "__main__":
    reset_admin_password()
