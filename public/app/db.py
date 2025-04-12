from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


# Define base class for SQLAlchemy models
class Base(DeclarativeBase):
    pass


# Initialize database without binding to app
db = SQLAlchemy(model_class=Base)

def init_db(app):
    """Initialize the database with the Flask app"""
    db.init_app(app)
    return db