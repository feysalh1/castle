from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class Parent(UserMixin, db.Model):
    """Parent user model"""
    __tablename__ = 'parents'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    children = db.relationship('Child', backref='parent', lazy=True, cascade="all, delete-orphan")
    settings = db.relationship('ParentSettings', backref='parent', uselist=False, cascade="all, delete-orphan")
    
    def set_password(self, password):
        """Set the password hash"""
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """Check if password is correct"""
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        """Return the id for Flask-Login"""
        return f"parent-{self.id}"
    
    def __repr__(self):
        return f'<Parent {self.username}>'


class Child(UserMixin, db.Model):
    """Child user model"""
    __tablename__ = 'children'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    display_name = db.Column(db.String(64), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=False)
    age = db.Column(db.Integer)
    birthday = db.Column(db.Date)
    avatar = db.Column(db.String(256), default='default.png')
    pin_code = db.Column(db.String(256))  # Simple numeric pin for child login
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    progress = db.relationship('Progress', backref='child', lazy=True, cascade="all, delete-orphan")
    rewards = db.relationship('Reward', backref='child', lazy=True, cascade="all, delete-orphan")
    
    def set_pin(self, pin):
        """Set the PIN hash"""
        self.pin_code = generate_password_hash(pin)
        
    def check_pin(self, pin):
        """Check if PIN is correct"""
        return check_password_hash(self.pin_code, pin)
    
    def get_id(self):
        """Return the id for Flask-Login"""
        return f"child-{self.id}"
    
    def __repr__(self):
        return f'<Child {self.display_name}>'


class ParentSettings(db.Model):
    """Parent settings model"""
    __tablename__ = 'parent_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=False, unique=True)
    allow_external_games = db.Column(db.Boolean, default=False)
    max_daily_playtime = db.Column(db.Integer, default=60)  # minutes
    content_age_filter = db.Column(db.Integer, default=4)  # max age-appropriate content
    notifications_enabled = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ParentSettings for parent_id {self.parent_id}>'


class Progress(db.Model):
    """Child's progress model"""
    __tablename__ = 'progress'
    
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)
    content_type = db.Column(db.String(64), nullable=False)  # 'story' or 'game'
    content_id = db.Column(db.String(64), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    completion_count = db.Column(db.Integer, default=0)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)
    time_spent = db.Column(db.Integer, default=0)  # seconds
    
    __table_args__ = (
        db.UniqueConstraint('child_id', 'content_type', 'content_id', name='unique_child_content'),
    )
    
    def __repr__(self):
        return f'<Progress {self.content_type}:{self.content_id} for child_id {self.child_id}>'


class Reward(db.Model):
    """Child's rewards model"""
    __tablename__ = 'rewards'
    
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)
    badge_id = db.Column(db.String(64), nullable=False)
    badge_name = db.Column(db.String(64), nullable=False)
    badge_description = db.Column(db.String(256))
    badge_image = db.Column(db.String(256))
    earned_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('child_id', 'badge_id', name='unique_child_badge'),
    )
    
    def __repr__(self):
        return f'<Reward {self.badge_name} for child_id {self.child_id}>'


class Session(db.Model):
    """User session model"""
    __tablename__ = 'sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(10), nullable=False)  # 'parent' or 'child'
    user_id = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Integer)  # seconds
    
    def __repr__(self):
        return f'<Session {self.id} for {self.user_type} {self.user_id}>'