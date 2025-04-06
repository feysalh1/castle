#!/usr/bin/env python3
from app import app
from models import Parent, db
from werkzeug.security import generate_password_hash

# Define a simple but strong password
NEW_PASSWORD = "Admin123!"

with app.app_context():
    # Find the admin user (assuming it's the first parent)
    admin = Parent.query.filter_by(id=1).first()
    
    if admin:
        # Update the password
        admin.password_hash = generate_password_hash(NEW_PASSWORD)
        db.session.commit()
        print(f"Successfully reset password for {admin.username} (ID: {admin.id})")
        print(f"New login credentials:")
        print(f"Username: {admin.username}")
        print(f"Password: {NEW_PASSWORD}")
    else:
        print("Admin user not found!")

