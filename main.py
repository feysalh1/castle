import os
import logging
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Define base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass

# Initialize database
db = SQLAlchemy(model_class=Base)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "childrens_castle_app_secret")

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
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Log the database URL (without credentials)
print(f"Using database URL: {database_url.split('@')[-1] if '@' in database_url else 'SQLite'}")

# Log the database URL (without credentials)
db_url = app.config["SQLALCHEMY_DATABASE_URI"]
if db_url:
    print(f"Using database: {db_url.split('@')[-1] if '@' in db_url else 'SQLite'}")

# Initialize database
db.init_app(app)

# Import models after initializing app and db
from models import (
    Parent, Child, ParentSettings, Progress, Reward, Session,
    LearningGoal, StoryQueue, SkillProgress, WeeklyReport, DevicePairing,
    DailyReport, Milestone, Event, ErrorLog, AgeGroup, Book, ApprovedBooks
)

# Import views and routes - this must come after db and app are initialized
import app as application

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

# Import database commands
import db_commands

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)