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
    device_pairings = db.relationship('DevicePairing', backref='parent', lazy=True, cascade="all, delete-orphan")
    
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
    learning_goals = db.relationship('LearningGoal', backref='child', lazy=True, cascade="all, delete-orphan")
    story_queue = db.relationship('StoryQueue', backref='child', uselist=False, cascade="all, delete-orphan")
    skill_progress = db.relationship('SkillProgress', backref='child', lazy=True, cascade="all, delete-orphan")
    weekly_reports = db.relationship('WeeklyReport', backref='child', lazy=True, cascade="all, delete-orphan")
    
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
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
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
        activities = json.loads(self.activities)
        
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
    
    def __repr__(self):
        return f'<ErrorLog {self.error_type} for {self.user_type or "system"} {self.user_id or ""}>'