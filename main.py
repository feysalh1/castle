import os
import logging
from dotenv import load_dotenv
from flask import Flask
from db import db, init_db

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "childrens_castle_app_secret")

# Firebase configuration from environment variables
app.config['FIREBASE_API_KEY'] = os.environ.get('FIREBASE_API_KEY')
app.config['FIREBASE_PROJECT_ID'] = os.environ.get('FIREBASE_PROJECT_ID')
app.config['FIREBASE_APP_ID'] = os.environ.get('FIREBASE_APP_ID')
app.config['FIREBASE_MEASUREMENT_ID'] = os.environ.get('FIREBASE_MEASUREMENT_ID')
app.config['FIREBASE_MESSAGING_SENDER_ID'] = os.environ.get('FIREBASE_MESSAGING_SENDER_ID')
app.config['FIREBASE_STORAGE_BUCKET'] = os.environ.get('FIREBASE_STORAGE_BUCKET')
app.config['FIREBASE_AUTH_DOMAIN'] = os.environ.get('FIREBASE_AUTH_DOMAIN')

# Set derived Firebase values if not explicitly set
if app.config['FIREBASE_PROJECT_ID'] and not app.config['FIREBASE_STORAGE_BUCKET']:
    app.config['FIREBASE_STORAGE_BUCKET'] = f"{app.config['FIREBASE_PROJECT_ID']}.appspot.com"

if app.config['FIREBASE_PROJECT_ID'] and not app.config['FIREBASE_AUTH_DOMAIN']:
    app.config['FIREBASE_AUTH_DOMAIN'] = f"{app.config['FIREBASE_PROJECT_ID']}.firebaseapp.com"

# Configure database
# Default database URL for local development if not provided
default_db_url = "sqlite:///children_castle.db"

# Configure the database, prioritize DATABASE_URL environment variable
database_url = os.environ.get("DATABASE_URL")
if not database_url:
    print("WARNING: DATABASE_URL not set, using SQLite for local development")
    database_url = default_db_url

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "connect_args": {
        "options": "-c timezone=utc",
        "sslmode": "require"
    } if database_url and database_url.startswith('postgresql') else {}
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Log the database URL (without credentials)
print(f"Using database URL: {database_url.split('@')[-1] if '@' in database_url else 'SQLite'}")

# Initialize database
db.init_app(app)

# Import models after initializing app and db
from models import (
    Parent, Child, ParentSettings, Progress, Reward, Session,
    LearningGoal, StoryQueue, SkillProgress, WeeklyReport, DevicePairing,
    DailyReport, Milestone, Event, ErrorLog, AgeGroup, Book, ApprovedBooks
)

# Function to test different SSL modes for PostgreSQL
def try_db_connection():
    if not database_url or not database_url.startswith('postgresql'):
        return False

    # Try different SSL modes
    ssl_modes = ["require", "prefer", "allow", "disable"]

    for ssl_mode in ssl_modes:
        try:
            print(f"Trying database connection with sslmode={ssl_mode}...")
            app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
                "pool_recycle": 300,
                "pool_pre_ping": True,
                "connect_args": {
                    "options": "-c timezone=utc",
                    "sslmode": ssl_mode
                } if database_url and database_url.startswith('postgresql') else {}
            }
            # Re-initialize the app with new settings
            db.init_app(app)

            # Test connection by creating tables
            with app.app_context():
                db.create_all()
                print(f"Database connection successful with sslmode={ssl_mode}!")
                return True
        except Exception as e:
            print(f"Connection failed with sslmode={ssl_mode}: {str(e)}")

    print("All SSL modes failed. Database functionality may be limited.")
    return False

# Create database tables if they don't exist
db_connected = False
try:
    with app.app_context():
        db.create_all()
        print("Database tables created successfully.")
        db_connected = True
except Exception as e:
    print(f"Error creating database tables: {str(e)}")
    print("Attempting to reconnect to database with different settings...")
    db_connected = try_db_connection()

if not db_connected:
    print("WARNING: Database connection failed. Some features may not work correctly.")

# Import database commands
import db_commands

# Add global template context for Firebase configuration
@app.context_processor
def inject_firebase_config():
    """Inject Firebase configuration into all templates"""
    return {
        'firebase_api_key': app.config.get('FIREBASE_API_KEY'),
        'firebase_project_id': app.config.get('FIREBASE_PROJECT_ID'),
        'firebase_app_id': app.config.get('FIREBASE_APP_ID'),
        'firebase_measurement_id': app.config.get('FIREBASE_MEASUREMENT_ID'),
        'firebase_messaging_sender_id': app.config.get('FIREBASE_MESSAGING_SENDER_ID'),
        'firebase_storage_bucket': app.config.get('FIREBASE_STORAGE_BUCKET'),
        'firebase_auth_domain': app.config.get('FIREBASE_AUTH_DOMAIN')
    }

# Import app functions AFTER database initialization
# The functions and routes are already defined in app.py
# We do NOT import app as a module to avoid circular imports

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, ssl_context='adhoc')