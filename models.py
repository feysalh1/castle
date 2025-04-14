from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import secrets
import os
from time import time
import jwt
from db import db

class Parent(UserMixin, db.Model):
    """Parent user model"""
    __tablename__ = 'parents'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=True)  # Made nullable for Firebase auth
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    display_name = db.Column(db.String(128), nullable=True)  # Display name for Firebase auth
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reset_password_token = db.Column(db.String(256), nullable=True)
    reset_token_expires = db.Column(db.DateTime, nullable=True)
    firebase_uid = db.Column(db.String(128), unique=True, nullable=True)  # Firebase Auth User ID
    is_guest = db.Column(db.Boolean, default=False)  # Flag for guest accounts
    
    # Relationships
    children = db.relationship('Child', backref='parent', lazy=True, cascade="all, delete-orphan")
    settings = db.relationship('ParentSettings', backref='parent', uselist=False, cascade="all, delete-orphan")
    device_pairings = db.relationship('DevicePairing', backref='parent', lazy=True, cascade="all, delete-orphan")
    
    def set_password(self, password):
        """Set the password hash"""
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """Check if password is correct"""
        return check_password_hash(self.password_hash, password)
    
    def get_reset_token(self, expires_in=3600):
        """Generate a JWT token for password reset"""
        now = datetime.utcnow()
        self.reset_token_expires = now + timedelta(seconds=expires_in)
        self.reset_password_token = jwt.encode(
            {'reset_password': self.id, 'exp': (now + timedelta(seconds=expires_in)).timestamp()},
            os.environ.get('SECRET_KEY', 'children-castle-app-secret'),
            algorithm='HS256'
        )
        return self.reset_password_token
    
    @staticmethod
    def verify_reset_token(token):
        """Verify the reset token"""
        try:
            data = jwt.decode(
                token,
                os.environ.get('SECRET_KEY', 'children-castle-app-secret'),
                algorithms=['HS256']
            )
            parent_id = data.get('reset_password')
        except:
            return None
        
        # Return parent or None if invalid
        return Parent.query.get(parent_id)
    
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
    learning_goals = db.relationship('LearningGoal', backref='child', lazy=True, cascade="all, delete-orphan")
    story_queue = db.relationship('StoryQueue', backref='child', uselist=False, cascade="all, delete-orphan")
    skill_progress = db.relationship('SkillProgress', backref='child', lazy=True, cascade="all, delete-orphan")
    daily_reports = db.relationship('DailyReport', backref='child', lazy=True, cascade="all, delete-orphan")
    weekly_reports = db.relationship('WeeklyReport', backref='child', lazy=True, cascade="all, delete-orphan")
    approved_books = db.relationship('ApprovedBooks', backref='child', lazy=True, cascade="all, delete-orphan")
    story_moods = db.relationship('StoryMood', back_populates='child', lazy=True, cascade="all, delete-orphan")
    
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
    
    # Content Controls
    allow_external_games = db.Column(db.Boolean, default=False)
    max_daily_playtime = db.Column(db.Integer, default=60)  # minutes
    max_weekly_playtime = db.Column(db.Integer, default=420)  # minutes (7 hours)
    content_age_filter = db.Column(db.Integer, default=4)  # max age-appropriate content
    
    # Access Schedule
    access_start_time = db.Column(db.Time, default=datetime.strptime('08:00', '%H:%M').time())
    access_end_time = db.Column(db.Time, default=datetime.strptime('20:00', '%H:%M').time())
    
    # Audio & Visual Settings
    enable_audio_narration = db.Column(db.Boolean, default=True)
    enable_background_music = db.Column(db.Boolean, default=True)
    narrator_voice_type = db.Column(db.String(32), default='friendly')
    reading_speed = db.Column(db.Float, default=1.0)
    sound_effects_volume = db.Column(db.Integer, default=80)  # percentage
    
    # Theme Filters - Stored as JSON list
    story_theme_filters = db.Column(db.String(512), default='["friendship","kindness","adventure","learning","problem-solving"]')
    
    # Rewards Settings
    stars_per_story = db.Column(db.Integer, default=2)
    stars_per_game = db.Column(db.Integer, default=3)
    star_milestone_rewards = db.Column(db.String(1024), default='{"10":"Special badge","25":"New avatar","50":"Unlock special game"}')
    
    # Notification Settings
    notifications_enabled = db.Column(db.Boolean, default=True)
    notification_frequency = db.Column(db.String(32), default='daily')  # 'immediate', 'daily', 'weekly'
    email_reports_enabled = db.Column(db.Boolean, default=True)
    report_delivery_day = db.Column(db.String(32), default='monday')
    
    # Security Settings
    parent_pin = db.Column(db.String(256))  # Hashed PIN for quick parent access
    require_parent_auth = db.Column(db.Boolean, default=True)
    session_timeout = db.Column(db.Integer, default=30)  # minutes
    
    # Sync Settings
    cloud_sync_enabled = db.Column(db.Boolean, default=True)
    sync_frequency = db.Column(db.String(32), default='hourly')  # 'realtime', 'hourly', 'daily', 'manual'
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def set_parent_pin(self, pin):
        """Set the parent PIN hash"""
        if pin and len(pin) == 4 and pin.isdigit():
            self.parent_pin = generate_password_hash(pin)
    
    def check_parent_pin(self, pin):
        """Check if parent PIN is correct"""
        if not self.parent_pin:
            return False
        return check_password_hash(self.parent_pin, pin)
    
    def __repr__(self):
        return f'<ParentSettings for parent_id {self.parent_id}>'


class Progress(db.Model):
    """Child's progress model"""
    __tablename__ = 'progress'
    
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)
    content_type = db.Column(db.String(64), nullable=False)  # 'story' or 'game'
    content_id = db.Column(db.String(64), nullable=False)
    content_title = db.Column(db.String(128))  # Actual title of story or game
    completed = db.Column(db.Boolean, default=False)
    completion_count = db.Column(db.Integer, default=0)
    last_accessed = db.Column(db.DateTime, default=datetime.utcnow)
    time_spent = db.Column(db.Integer, default=0)  # seconds
    first_accessed = db.Column(db.DateTime, default=datetime.utcnow)  # When first read/played
    completion_history = db.Column(db.String(1024), default='[]')  # JSON array of completion timestamps
    pages_read = db.Column(db.Integer, default=0)  # For stories: number of pages read
    score = db.Column(db.Integer)  # For games: highest score achieved
    difficulty_level = db.Column(db.String(32))  # 'easy', 'medium', 'hard'
    is_favorite = db.Column(db.Boolean, default=False)  # If marked as favorite by the child
    engagement_rating = db.Column(db.Integer)  # 1-5 star rating of how much child enjoyed it
    access_count = db.Column(db.Integer, default=1)  # How many times content was accessed
    last_session_duration = db.Column(db.Integer)  # Duration of last session in seconds
    average_session_time = db.Column(db.Float)  # Average session time in seconds
    
    # For analytics and engagement tracking
    streak_count = db.Column(db.Integer, default=0)  # Days in a row accessed
    last_streak_date = db.Column(db.Date)  # Last date this was accessed for streak tracking
    
    # Error tracking
    error_count = db.Column(db.Integer, default=0)  # Count of errors during content usage
    last_error = db.Column(db.String(256))  # Description of last error encountered
    
    __table_args__ = (
        db.UniqueConstraint('child_id', 'content_type', 'content_id', name='unique_child_content'),
    )
    
    def add_completion_timestamp(self):
        """Add current timestamp to completion history"""
        import json
        try:
            history = json.loads(self.completion_history)
        except:
            history = []
        
        history.append(datetime.utcnow().isoformat())
        self.completion_history = json.dumps(history)
    
    def update_streak(self):
        """Update the access streak for this content"""
        today = datetime.now().date()
        
        # If no previous access or streak was broken (more than 1 day gap)
        if not self.last_streak_date or (today - self.last_streak_date).days > 1:
            self.streak_count = 1
        # If accessed on consecutive days
        elif (today - self.last_streak_date).days == 1:
            self.streak_count += 1
        # Otherwise it's the same day, streak doesn't change
        
        self.last_streak_date = today
    
    def record_access(self, session_duration=None):
        """Record an access to this content and update relevant metrics"""
        self.access_count += 1
        self.last_accessed = datetime.utcnow()
        
        # Update streak information
        self.update_streak()
        
        # Update session duration metrics if provided
        if session_duration:
            self.last_session_duration = session_duration
            
            # Update the average session time
            if not self.average_session_time:
                self.average_session_time = session_duration
            else:
                # Weighted average (90% old, 10% new) to smooth outliers
                self.average_session_time = (self.average_session_time * 0.9) + (session_duration * 0.1)
    
    def record_error(self, error_description):
        """Record an error that occurred during content usage"""
        self.error_count += 1
        self.last_error = error_description
    
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
    source_type = db.Column(db.String(32))  # 'story', 'game', 'achievement', 'milestone'
    source_id = db.Column(db.String(64))  # ID of the source (story_id, game_id, etc.)
    achievement_level = db.Column(db.String(32))  # 'bronze', 'silver', 'gold', 'platinum', 'diamond'
    points_value = db.Column(db.Integer, default=1)  # Points/stars value of this reward
    showcase_priority = db.Column(db.Integer, default=0)  # Higher values show up first in showcase
    
    __table_args__ = (
        db.UniqueConstraint('child_id', 'badge_id', name='unique_child_badge'),
    )
    
    def __repr__(self):
        return f'<Reward {self.badge_name} for child_id {self.child_id}>'


class LearningGoal(db.Model):
    """Child's learning goals model"""
    __tablename__ = 'learning_goals'
    
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)
    goal_type = db.Column(db.String(32), nullable=False)  # 'story', 'game', 'badge', 'custom'
    goal_descriptor = db.Column(db.String(64))  # e.g., 'new', 'counting', etc.
    goal_text = db.Column(db.String(256), nullable=False)
    goal_quantity = db.Column(db.Integer, default=1)
    completed_quantity = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<LearningGoal "{self.goal_text}" for child_id {self.child_id}>'


class AgeGroup(db.Model):
    """Age group model for categorizing books"""
    __tablename__ = 'age_groups'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    min_age = db.Column(db.Integer, nullable=False)
    max_age = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    books = db.relationship('Book', backref='age_group', lazy=True)
    
    def __repr__(self):
        return f'<AgeGroup {self.name} ({self.min_age}-{self.max_age})>'


class Book(db.Model):
    """Book model for children's books"""
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    file_name = db.Column(db.String(128), nullable=False, unique=True)  # Name of the text file
    author = db.Column(db.String(128))
    description = db.Column(db.String(512))
    age_group_id = db.Column(db.Integer, db.ForeignKey('age_groups.id'), nullable=False)
    difficulty_level = db.Column(db.String(32), default='easy')  # 'easy', 'medium', 'hard'
    themes = db.Column(db.String(256), default='[]')  # JSON array of themes
    is_interactive = db.Column(db.Boolean, default=False)
    has_illustrations = db.Column(db.Boolean, default=True)
    has_audio = db.Column(db.Boolean, default=False)
    reading_time_minutes = db.Column(db.Integer, default=5)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Book {self.title}>'


class ApprovedBooks(db.Model):
    """Parent-approved books for children"""
    __tablename__ = 'approved_books'
    
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    approved_at = db.Column(db.DateTime, default=datetime.utcnow)
    approved_by = db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=False)
    
    # Relationships
    book = db.relationship('Book', backref='approved_for', lazy=True)
    parent = db.relationship('Parent', backref='approved_books', lazy=True)
    
    __table_args__ = (
        db.UniqueConstraint('child_id', 'book_id', name='unique_child_book'),
    )
    
    def __repr__(self):
        return f'<ApprovedBook book_id={self.book_id} for child_id={self.child_id}>'


class StoryQueue(db.Model):
    """Custom story queue for children"""
    __tablename__ = 'story_queues'
    
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False, unique=True)
    story_ids = db.Column(db.String(1024), default='[]')  # JSON array of story IDs in order
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<StoryQueue for child_id {self.child_id}>'


class SkillProgress(db.Model):
    """Child's skill progress model"""
    __tablename__ = 'skill_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)
    skill_name = db.Column(db.String(64), nullable=False)
    skill_level = db.Column(db.Integer, default=0)  # 0-100 percentage
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('child_id', 'skill_name', name='unique_child_skill'),
    )
    
    def __repr__(self):
        return f'<SkillProgress {self.skill_name}={self.skill_level}% for child_id {self.child_id}>'


class DailyReport(db.Model):
    """Daily report model for children"""
    __tablename__ = 'daily_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)
    report_date = db.Column(db.Date, nullable=False)
    stories_read = db.Column(db.Integer, default=0)
    games_played = db.Column(db.Integer, default=0)
    time_spent = db.Column(db.Integer, default=0)  # minutes
    stars_earned = db.Column(db.Integer, default=0)
    badges_earned = db.Column(db.Integer, default=0)
    reading_time = db.Column(db.Integer, default=0)  # seconds spent reading
    game_time = db.Column(db.Integer, default=0)  # seconds spent playing games
    quiz_scores = db.Column(db.String(512), default='[]')  # JSON array of quiz scores
    emotional_feedback = db.Column(db.String(1024), default='{}')  # JSON object of emoji reaction counts
    content_interactions = db.Column(db.Integer, default=0)  # Number of interactive elements clicked
    daily_streak = db.Column(db.Integer, default=0)  # Current streak as of this day
    activity_breakdown = db.Column(db.Text, default='{}')  # Detailed JSON of daily activity breakdown
    learning_tags = db.Column(db.String(512), default='[]')  # JSON array of learning tags engaged with
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('child_id', 'report_date', name='unique_child_day'),
    )
    
    def __repr__(self):
        return f'<DailyReport for child_id {self.child_id} on {self.report_date}>'


class ChatHistory(db.Model):
    """Model to store chat history between children and AI assistant"""
    __tablename__ = 'chat_history'
    
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)
    question = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    topic = db.Column(db.String(64), default='general')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    parent_reviewed = db.Column(db.Boolean, default=False)
    flagged_for_review = db.Column(db.Boolean, default=False)
    parent_note = db.Column(db.Text)
    
    # Add relationship to Child model
    child = db.relationship('Child', backref=db.backref('chat_history', lazy=True, cascade="all, delete-orphan"))
    
    def __repr__(self):
        preview = self.question[:30] + '...' if len(self.question) > 30 else self.question
        return f'<ChatHistory "{preview}" for child_id {self.child_id}>'


class WeeklyReport(db.Model):
    """Weekly report model for children"""
    __tablename__ = 'weekly_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)
    week_start = db.Column(db.Date, nullable=False)
    week_end = db.Column(db.Date, nullable=False)
    stories_read = db.Column(db.Integer, default=0)
    games_played = db.Column(db.Integer, default=0)
    time_spent = db.Column(db.Integer, default=0)  # minutes
    stars_earned = db.Column(db.Integer, default=0)
    badges_earned = db.Column(db.Integer, default=0)
    goals_completed = db.Column(db.Integer, default=0)
    skills_data = db.Column(db.String(1024), default='{}')  # JSON of skill progress
    top_stories = db.Column(db.String(512), default='[]')  # JSON array of top story IDs
    top_games = db.Column(db.String(512), default='[]')  # JSON array of top game IDs
    reading_time = db.Column(db.Integer, default=0)  # seconds spent reading
    game_time = db.Column(db.Integer, default=0)  # seconds spent playing games
    quiz_scores = db.Column(db.String(512), default='[]')  # JSON array of quiz scores
    emotional_feedback = db.Column(db.String(1024), default='{}')  # JSON object of emoji reaction counts
    daily_breakdown = db.Column(db.Text, default='[]')  # JSON array of daily metrics
    current_streak = db.Column(db.Integer, default=0)  # Current ongoing streak
    longest_streak = db.Column(db.Integer, default=0)  # Longest streak during week
    learning_progress = db.Column(db.String(1024), default='{}')  # Progress on learning categories
    favorite_content = db.Column(db.String(512), default='[]')  # Most engaged content
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    email_sent = db.Column(db.Boolean, default=False)  # Whether report has been emailed
    email_sent_date = db.Column(db.DateTime)  # When report was emailed
    
    __table_args__ = (
        db.UniqueConstraint('child_id', 'week_start', name='unique_child_week'),
    )
    
    def __repr__(self):
        return f'<WeeklyReport for child_id {self.child_id} week of {self.week_start}>'


class DevicePairing(db.Model):
    """Device pairing model"""
    __tablename__ = 'device_pairings'
    
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=False)
    pairing_code = db.Column(db.String(16), unique=True, nullable=False)
    device_name = db.Column(db.String(64))
    device_type = db.Column(db.String(32))  # 'mobile', 'tablet', 'desktop'
    is_active = db.Column(db.Boolean, default=True)
    last_sync = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<DevicePairing code={self.pairing_code} for parent_id {self.parent_id}>'


class Session(db.Model):
    """User session model"""
    __tablename__ = 'sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(10), nullable=False)  # 'parent' or 'child'
    user_id = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    duration = db.Column(db.Integer)  # seconds
    ip_address = db.Column(db.String(45))  # Store IP address (IPv4 or IPv6)
    user_agent = db.Column(db.String(255))  # Store browser/device info
    device_type = db.Column(db.String(32))  # 'desktop', 'tablet', 'mobile'
    activities = db.Column(db.String(1024), default='[]')  # JSON array of activity logs
    
    # Relationships
    events = db.relationship('Event', backref='session', lazy=True, cascade="all, delete-orphan")
    error_logs = db.relationship('ErrorLog', backref='session', lazy=True, cascade="all, delete-orphan")
    
    def record_activity(self, activity_type, content_id=None, details=None):
        """Add activity to the session log"""
        import json
        activities = json.loads(self.activities if self.activities else '[]')
        
        activity = {
            'timestamp': datetime.utcnow().isoformat(),
            'type': activity_type,  # 'login', 'story_view', 'game_play', 'reward_earned', etc.
            'content_id': content_id,
            'details': details or {}
        }
        
        activities.append(activity)
        self.activities = json.dumps(activities)
    
    def close(self):
        """Close the session and calculate duration"""
        if not self.end_time:
            self.end_time = datetime.utcnow()
            if self.start_time:
                delta = self.end_time - self.start_time
                self.duration = int(delta.total_seconds())
    
    def __repr__(self):
        return f'<Session {self.id} for {self.user_type} {self.user_id}>'


class Milestone(db.Model):
    """Milestone/Achievement tracking model"""
    __tablename__ = 'milestones'
    
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)
    milestone_type = db.Column(db.String(32), nullable=False)  # 'daily', 'weekly', 'streak', 'completion'
    milestone_id = db.Column(db.String(64), nullable=False)  # Unique identifier
    milestone_name = db.Column(db.String(128), nullable=False)
    milestone_description = db.Column(db.String(256))
    progress = db.Column(db.Integer, default=0)
    target_value = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    earned_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.UniqueConstraint('child_id', 'milestone_id', name='unique_child_milestone'),
    )
    
    def update_progress(self, value=1):
        """Increment milestone progress and check for completion"""
        self.progress += value
        
        # Check if milestone is completed
        if self.progress >= self.target_value and not self.completed:
            self.completed = True
            self.earned_at = datetime.utcnow()
            
            # Here you could add code to create a reward when a milestone is completed
            return True
        
        return False
    
    def __repr__(self):
        return f'<Milestone {self.milestone_id} for child_id {self.child_id}>'


class Event(db.Model):
    """Custom event tracking model"""
    __tablename__ = 'events'
    
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(10), nullable=False)  # 'parent' or 'child'
    user_id = db.Column(db.Integer, nullable=False)
    event_type = db.Column(db.String(64), nullable=False)
    event_name = db.Column(db.String(128), nullable=False)
    event_data = db.Column(db.JSON)
    occurred_at = db.Column(db.DateTime, default=datetime.utcnow)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id', ondelete='SET NULL'))
    
    @classmethod
    def track_event(cls, user_type, user_id, event_type, event_name, event_data=None, session_id=None):
        """Create and save a new event"""
        event = cls(
            user_type=user_type,
            user_id=user_id,
            event_type=event_type,
            event_name=event_name,
            event_data=event_data,
            session_id=session_id
        )
        db.session.add(event)
        db.session.commit()
        return event
    
    def __repr__(self):
        return f'<Event {self.event_type}:{self.event_name} for {self.user_type} {self.user_id}>'


class ErrorLog(db.Model):
    """Error logging model"""
    __tablename__ = 'error_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_type = db.Column(db.String(10))  # 'parent', 'child', or None for system errors
    user_id = db.Column(db.Integer)
    error_type = db.Column(db.String(64), nullable=False)
    error_message = db.Column(db.Text, nullable=False)
    error_context = db.Column(db.JSON)
    stack_trace = db.Column(db.Text)
    occurred_at = db.Column(db.DateTime, default=datetime.utcnow)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id', ondelete='SET NULL'))
    resolved = db.Column(db.Boolean, default=False)
    resolution_notes = db.Column(db.Text)
    
    @classmethod
    def log_error(cls, error_type, error_message, user_type=None, user_id=None, 
                  error_context=None, stack_trace=None, session_id=None):
        """Create and save a new error log"""
        error_log = cls(
            user_type=user_type,
            user_id=user_id,
            error_type=error_type,
            error_message=error_message,
            error_context=error_context,
            stack_trace=stack_trace,
            session_id=session_id
        )
        db.session.add(error_log)
        db.session.commit()
        return error_log
    
    def mark_resolved(self, resolution_notes=None):
        """Mark an error as resolved"""
        self.resolved = True
        if resolution_notes:
            self.resolution_notes = resolution_notes
        db.session.commit()


class Conversation(db.Model):
    """AI Assistant conversation history model"""
    __tablename__ = 'conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)
    assistant_character = db.Column(db.String(64), default='castle_buddy')
    title = db.Column(db.String(128), default='Conversation')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship with child
    child = db.relationship('Child', backref='conversations')
    
    # Relationship with messages
    messages = db.relationship('ConversationMessage', backref='conversation', 
                              cascade='all, delete-orphan', lazy='dynamic',
                              order_by='ConversationMessage.timestamp')
    
    def __repr__(self):
        return f'<Conversation {self.id} with {self.assistant_character} for child {self.child_id}>'


class ConversationMessage(db.Model):
    """Individual messages in an AI Assistant conversation"""
    __tablename__ = 'conversation_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversations.id'), nullable=False)
    role = db.Column(db.String(32), nullable=False)  # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    audio_path = db.Column(db.String(256))  # Path to voice narration audio file
    
    def __repr__(self):
        return f'<Message {self.id} ({self.role}) in conversation {self.conversation_id}>'


class AssistantCharacter(db.Model):
    """Themed AI Assistant characters"""
    __tablename__ = 'assistant_characters'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    display_name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    character_type = db.Column(db.String(32))  # 'animal', 'robot', 'fantasy', etc.
    voice_id = db.Column(db.String(64))  # ElevenLabs voice ID
    image_path = db.Column(db.String(256))  # Path to character image
    system_prompt = db.Column(db.Text)  # Custom system prompt for this character
    
    def __repr__(self):
        return f'<AssistantCharacter {self.name}>'


class EducationalGame(db.Model):
    """Educational games suggested by AI Assistant"""
    __tablename__ = 'educational_games'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(64))  # math, language, science, etc.
    min_age = db.Column(db.Integer, default=3)
    max_age = db.Column(db.Integer, default=8)
    difficulty = db.Column(db.String(32))  # easy, medium, hard
    instructions = db.Column(db.Text)
    url = db.Column(db.String(256))  # URL for external games
    image_path = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<EducationalGame {self.title}>'


class PhotoAlbum(db.Model):
    """Album/collection for organizing photos"""
    __tablename__ = 'photo_albums'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    cover_photo_id = db.Column(db.Integer, db.ForeignKey('photos.id', ondelete='SET NULL'), nullable=True)
    
    # Security and access control
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=True)
    
    # Only one of child_id or parent_id should be filled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Access control
    is_private = db.Column(db.Boolean, default=True)
    
    # Relationships
    photos = db.relationship('Photo', secondary='photo_album_items', 
                            backref=db.backref('albums', lazy='dynamic'))
    
    def __repr__(self):
        owner = f"child:{self.child_id}" if self.child_id else f"parent:{self.parent_id}"
        return f'<PhotoAlbum {self.id} by {owner}: {self.name}>'


class PhotoAlbumItem(db.Model):
    """Join table for photos and albums"""
    __tablename__ = 'photo_album_items'
    
    photo_id = db.Column(db.Integer, db.ForeignKey('photos.id', ondelete='CASCADE'), primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('photo_albums.id', ondelete='CASCADE'), primary_key=True)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    position = db.Column(db.Integer, default=0)  # For ordering photos in album


class Photo(db.Model):
    """Secure photo storage for children and parents"""
    __tablename__ = 'photos'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(256), nullable=False)
    thumbnail_filename = db.Column(db.String(256), nullable=True)
    original_filename = db.Column(db.String(256), nullable=True)
    file_size = db.Column(db.Integer, nullable=False)  # Size in bytes
    file_type = db.Column(db.String(10), nullable=False)  # jpg, png, etc.
    
    # Firebase Storage integration
    firebase_storage_path = db.Column(db.String(256), nullable=True)
    firebase_thumbnail_path = db.Column(db.String(256), nullable=True)
    firebase_url = db.Column(db.String(512), nullable=True)
    firebase_thumbnail_url = db.Column(db.String(512), nullable=True)
    storage_type = db.Column(db.String(20), default='local', nullable=False)  # 'local' or 'firebase'
    
    # Security and access control
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('parents.id'), nullable=True)
    
    # Only one of child_id or parent_id should be filled
    # If parent_id is filled, it's a parent's photo
    # If child_id is filled, it's a child's photo
    
    # Extra metadata
    title = db.Column(db.String(256), nullable=True)
    description = db.Column(db.Text, nullable=True)
    tags = db.Column(db.String(512), nullable=True)  # Comma-separated tags
    is_favorite = db.Column(db.Boolean, default=False)
    
    # Journal entry content
    journal_entry = db.Column(db.Text, nullable=True)  # Additional text for journal entries
    mood = db.Column(db.String(50), nullable=True)  # happy, sad, excited, etc.
    journal_date = db.Column(db.Date, nullable=True)  # Specific date for the journal entry
    
    # Timestamps
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Access control
    is_private = db.Column(db.Boolean, default=True)  # If True, only visible to the uploader and linked parent/child
    
    # Relationships
    # Define relationships in a way that works with nullable foreign keys
    child = db.relationship('Child', backref=db.backref('photos', lazy=True, cascade="all, delete-orphan"), 
                           foreign_keys=[child_id], primaryjoin="Photo.child_id==Child.id")
    parent = db.relationship('Parent', backref=db.backref('photos', lazy=True, cascade="all, delete-orphan"), 
                            foreign_keys=[parent_id], primaryjoin="Photo.parent_id==Parent.id")
    
    def __repr__(self):
        owner = f"child:{self.child_id}" if self.child_id else f"parent:{self.parent_id}"
        return f'<Photo {self.id} by {owner}: {self.filename}>'
        
    def get_secure_url(self):
        """Generate a secure URL for accessing the photo, including security tokens"""
        from app import app
        import jwt
        import time
        
        # Generate a token that expires in 1 hour
        token_data = {
            'photo_id': self.id,
            'user_type': 'child' if self.child_id else 'parent',
            'user_id': self.child_id if self.child_id else self.parent_id,
            'exp': int(time.time()) + 3600  # 1 hour expiration
        }
        
        token = jwt.encode(
            token_data,
            app.config.get('SECRET_KEY', 'children-castle-app-secret'),
            algorithm='HS256'
        )
        
        # Return a URL that includes the token
        return f"/photos/view/{self.id}?token={token}"


class StoryMood(db.Model):
    """Mood settings for dynamic storytelling"""
    __tablename__ = 'story_moods'
    
    id = db.Column(db.Integer, primary_key=True)
    child_id = db.Column(db.Integer, db.ForeignKey('children.id'), nullable=False)
    mood_type = db.Column(db.String(50), nullable=False)  # e.g., 'happy', 'calm', 'adventurous', 'sleepy'
    intensity = db.Column(db.Integer, nullable=False, default=5)  # Scale of 1-10
    active = db.Column(db.Boolean, default=True)
    background_music = db.Column(db.String(100), nullable=True)  # Path to background music matching mood
    color_theme = db.Column(db.String(50), nullable=True)  # CSS color theme for UI
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_used = db.Column(db.DateTime, nullable=True)
    
    # Define standard moods
    @staticmethod
    def get_standard_moods():
        return [
            {"type": "happy", "music": "happy_music.mp3", "color": "#FFD700"},
            {"type": "calm", "music": "calm_music.mp3", "color": "#87CEEB"},
            {"type": "adventurous", "music": "adventure_music.mp3", "color": "#FF6347"},
            {"type": "sleepy", "music": "lullaby_music.mp3", "color": "#9370DB"},
            {"type": "curious", "music": "curious_music.mp3", "color": "#32CD32"},
        ]
    
    def __repr__(self):
        return f'<StoryMood {self.child_id} - {self.mood_type}>'