"""
Database command-line interface for Children's Castle application.
Provides commands to manage database schema and operations.
"""

import os
import click
from app import app, db
from models import *
from datetime import datetime

@app.cli.group()
def database():
    """Database management commands."""
    pass

@database.command()
def init():
    """Initialize the database with tables."""
    with app.app_context():
        db.create_all()
        click.echo('Database tables created!')

@database.command()
def drop():
    """Drop all database tables."""
    if click.confirm('Are you sure you want to drop all tables? This will delete all data!'):
        with app.app_context():
            db.drop_all()
            click.echo('All database tables dropped!')

@database.command()
def recreate():
    """Recreate all database tables (drop + create)."""
    if click.confirm('Are you sure you want to recreate all tables? This will delete all data!'):
        with app.app_context():
            db.drop_all()
            db.create_all()
            click.echo('All database tables dropped and recreated!')

@database.command()
def add_tracking_columns():
    """Add tracking columns to existing tables."""
    from sqlalchemy import inspect, text
    
    with app.app_context():
        conn = db.engine.connect()
        inspector = inspect(db.engine)
        
        # Progress table updates
        progress_columns = {
            'is_favorite': 'BOOLEAN DEFAULT FALSE',
            'engagement_rating': 'INTEGER',
            'access_count': 'INTEGER DEFAULT 1',
            'last_session_duration': 'INTEGER',
            'average_session_time': 'FLOAT',
            'streak_count': 'INTEGER DEFAULT 0',
            'last_streak_date': 'DATE',
            'error_count': 'INTEGER DEFAULT 0',
            'last_error': 'VARCHAR(256)'
        }
        
        # Session table updates
        session_columns = {
            'ip_address': 'VARCHAR(45)',
            'user_agent': 'VARCHAR(255)',
            'device_type': 'VARCHAR(32)'
        }
        
        # Add columns to Progress table
        existing_columns = [col['name'] for col in inspector.get_columns('progress')]
        for col_name, col_type in progress_columns.items():
            if col_name not in existing_columns:
                click.echo(f"Adding column '{col_name}' to table 'progress'")
                sql = f"ALTER TABLE progress ADD COLUMN IF NOT EXISTS {col_name} {col_type}"
                try:
                    conn.execute(text(sql))
                    conn.commit()
                except Exception as e:
                    click.echo(f"Error adding column '{col_name}': {e}")
            else:
                click.echo(f"Column '{col_name}' already exists in table 'progress'")
        
        # Add columns to Session table
        existing_columns = [col['name'] for col in inspector.get_columns('sessions')]
        for col_name, col_type in session_columns.items():
            if col_name not in existing_columns:
                click.echo(f"Adding column '{col_name}' to table 'sessions'")
                sql = f"ALTER TABLE sessions ADD COLUMN IF NOT EXISTS {col_name} {col_type}"
                try:
                    conn.execute(text(sql))
                    conn.commit()
                except Exception as e:
                    click.echo(f"Error adding column '{col_name}': {e}")
            else:
                click.echo(f"Column '{col_name}' already exists in table 'sessions'")

        click.echo("Database schema update completed!")

@database.command()
def create_milestone_table():
    """Create the milestone tracking table."""
    from sqlalchemy import text
    
    with app.app_context():
        conn = db.engine.connect()
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS milestones (
            id SERIAL PRIMARY KEY,
            child_id INTEGER NOT NULL REFERENCES children(id) ON DELETE CASCADE,
            milestone_type VARCHAR(32) NOT NULL,
            milestone_id VARCHAR(64) NOT NULL,
            milestone_name VARCHAR(128) NOT NULL,
            milestone_description VARCHAR(256),
            progress INTEGER DEFAULT 0,
            target_value INTEGER NOT NULL,
            completed BOOLEAN DEFAULT FALSE,
            earned_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (child_id, milestone_id)
        )
        """
        try:
            conn.execute(text(create_table_sql))
            conn.commit()
            click.echo("Milestones table created successfully!")
        except Exception as e:
            click.echo(f"Error creating milestones table: {e}")

@database.command()
def stats():
    """Show database statistics."""
    with app.app_context():
        parent_count = Parent.query.count()
        child_count = Child.query.count()
        progress_count = Progress.query.count()
        reward_count = Reward.query.count()
        session_count = Session.query.count()
        
        click.echo(f"Database Statistics:")
        click.echo(f"- Parents: {parent_count}")
        click.echo(f"- Children: {child_count}")
        click.echo(f"- Progress Records: {progress_count}")
        click.echo(f"- Rewards: {reward_count}")
        click.echo(f"- Sessions: {session_count}")

if __name__ == '__main__':
    print("This file should be imported and its commands used with Flask CLI")
    print("Usage: flask database [command]")