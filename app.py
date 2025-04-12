import os
import logging
import json
import re
import qrcode
import io
import psutil
import platform
import sys
import uuid
from datetime import datetime, timedelta, date
from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify, send_file, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from dotenv import load_dotenv
from sqlalchemy.exc import SQLAlchemyError

# Load environment variables from .env file
load_dotenv()

# Define constants for file paths
STORIES_DIR = "static/stories"
IMAGES_DIR = "static/images/stories"
AUDIO_DIR = "static/audio"

# Use our db object 
from db import db

# Import model classes
from models import (
    Parent, Child, ParentSettings, Progress, Reward, Session,
    LearningGoal, StoryQueue, SkillProgress, WeeklyReport, DevicePairing,
    DailyReport, Milestone, Event, ErrorLog, AgeGroup, Book, ApprovedBooks
)
from reports import generate_daily_report, generate_weekly_report, get_report_data_for_period, generate_chart_data

def detect_device_type(user_agent_string):
    """
    Detect device type based on User-Agent string
    Returns 'mobile', 'tablet', or 'desktop'
    """
    if not user_agent_string:
        return 'unknown'
        
    # Check for mobile
    mobile_patterns = [
        r'Android.*Mobile', 
        r'iPhone', 
        r'iPod', 
        r'BlackBerry', 
        r'Opera Mini', 
        r'IEMobile'
    ]
    for pattern in mobile_patterns:
        if re.search(pattern, user_agent_string, re.IGNORECASE):
            return 'mobile'
    
    # Check for tablets
    tablet_patterns = [
        r'iPad', 
        r'Android(?!.*Mobile)', 
        r'Tablet'
    ]
    for pattern in tablet_patterns:
        if re.search(pattern, user_agent_string, re.IGNORECASE):
            return 'tablet'
    
    # Default to desktop
    return 'desktop'

# Import custom ElevenLabs voice generation module
import generate_elevenlabs_audio

# Define function to get database size (will be executed after db is initialized)
def get_database_size():
    """Get the size of the database in MB"""
    try:
        # Extract DB name from connection string
        db_name = os.environ.get("PGDATABASE", "postgres")
        # Try to get database size via db connection
        with db.engine.connect() as conn:
            result = conn.execute(db.text(f"SELECT pg_database_size('{db_name}') / (1024*1024) as size_mb;"))
            size_mb = result.scalar()
            return round(size_mb or 0, 2)
    except Exception as e:
        # Fallback if SQL query fails
        logging.error(f"Failed to get database size: {str(e)}")
        return 0

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Import Flask app from main
from main import app

# Configure WTF-CSRF
app.config['WTF_CSRF_ENABLED'] = True
app.config['WTF_CSRF_SECRET_KEY'] = app.secret_key
app.config['WTF_CSRF_TIME_LIMIT'] = 3600  # 1 hour

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Exempt API endpoints from CSRF protection
csrf.exempt('/api/track-progress')
csrf.exempt('/api/get-progress')
csrf.exempt('/api/get-rewards')
csrf.exempt('/api/child-activity')
csrf.exempt('/api/save-learning-goal')
csrf.exempt('/api/delete-learning-goal')
csrf.exempt('/api/save-story-queue')
csrf.exempt('/api/generate-pairing-code')
csrf.exempt('/api/generate-voice')
csrf.exempt('/api/voices')
csrf.exempt('/api/session-stats')
csrf.exempt('/api/ask-assistant')
csrf.exempt('/api/generate-story')
csrf.exempt('/api/answer-question')
csrf.exempt('/api/parent-tip')
csrf.exempt('/api/track-event')
csrf.exempt('/api/reports/generate-daily')
csrf.exempt('/api/reports/generate-weekly')
csrf.exempt('/api/reports/data')
csrf.exempt('/api/reports/emotional-feedback')
csrf.exempt('/api/books/get-child-approved')
csrf.exempt('/api/books/approve')
csrf.exempt('/api/books/unapprove')

# The database configuration is now handled in main.py

# Database is already initialized in main.py

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'
login_manager.login_message = "Please log in to access this page."
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    """Load user from database"""
    # Format: parent-1 or child-1
    try:
        user_type, user_id = user_id.split('-')
        if user_type == 'parent':
            return Parent.query.get(int(user_id))
        elif user_type == 'child':
            return Child.query.get(int(user_id))
    except:
        return None


# Import and register ChatGPT routes
from chatgpt_routes import chatgpt_bp
from story_enhancement_routes import story_enhancement
from firebase_auth import firebase_auth

# Register blueprints
app.register_blueprint(chatgpt_bp)
app.register_blueprint(story_enhancement)
app.register_blueprint(firebase_auth)

# Create forms
class EmptyForm(FlaskForm):
    """Simple form for CSRF protection"""
    pass

class RequestResetForm(FlaskForm):
    """Form for requesting a password reset"""
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')
    
    def validate_email(self, email):
        """Check if email exists in database"""
        parent = Parent.query.filter_by(email=email.data).first()
        if not parent:
            raise ValidationError('There is no account with that email address.')

class ResetPasswordForm(FlaskForm):
    """Form for resetting password"""
    password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long.')
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.')
    ])
    submit = SubmitField('Reset Password')

# Database tables are created in main.py


@app.route('/')
def index():
    """Render the homepage of the Children's Castle app."""
    if current_user.is_authenticated:
        if session.get('user_type') == 'parent':
            return redirect(url_for('parent_dashboard'))
        elif session.get('user_type') == 'child':
            return redirect(url_for('child_dashboard'))
    # Create empty form for CSRF protection in the guest login form
    form = EmptyForm()
    return render_template('login_landing.html', form=form)


@app.route('/parent/register', methods=['GET', 'POST'])
def parent_register():
    """Register a new parent account"""
    if current_user.is_authenticated:
        return redirect(url_for('parent_dashboard'))
    
    form = EmptyForm()
    
    if form.validate_on_submit():
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('parent_register'))
        
        # Check if username or email already exists
        if Parent.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('parent_register'))
        
        if Parent.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return redirect(url_for('parent_register'))
        
        # Create new parent
        parent = Parent(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        parent.set_password(password)
        
        # Create default settings
        settings = ParentSettings(
            parent=parent,
            allow_external_games=True,
            max_daily_playtime=90,
            content_age_filter=6
        )
        
        # Save to database
        db.session.add(parent)
        db.session.add(settings)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('parent_login'))
    
    return render_template('parent_register.html', form=form)


@app.route('/parent/login', methods=['GET', 'POST'])
def parent_login():
    """Login for parent accounts"""
    if current_user.is_authenticated:
        return redirect(url_for('parent_dashboard'))
    
    form = EmptyForm()
    
    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember') == 'on'
        
        parent = Parent.query.filter_by(username=username).first()
        
        if not parent or not parent.check_password(password):
            flash('Invalid username or password', 'error')
            return redirect(url_for('parent_login'))
        
        # Log in the parent
        login_user(parent, remember=remember)
        session['user_type'] = 'parent'
        
        # Record login session with additional metadata
        new_session = Session(
            user_type='parent', 
            user_id=parent.id,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string,
            device_type=detect_device_type(request.user_agent.string)
        )
        new_session.record_activity('login')
        db.session.add(new_session)
        db.session.commit()
        
        # Redirect to next page or dashboard
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect(url_for('parent_dashboard'))
    
    # Get Firebase configuration from environment
    firebase_api_key = os.environ.get('FIREBASE_API_KEY')
    firebase_project_id = os.environ.get('FIREBASE_PROJECT_ID')
    firebase_app_id = os.environ.get('FIREBASE_APP_ID')
    
    return render_template(
        'parent_login.html', 
        form=form,
        firebase_config_script=f"""
            <script>
                window.FIREBASE_API_KEY = "{firebase_api_key}";
                window.FIREBASE_PROJECT_ID = "{firebase_project_id}";
                window.FIREBASE_APP_ID = "{firebase_app_id}";
            </script>
        """
    )


@app.route('/parent/reset-password', methods=['GET', 'POST'])
def request_reset_password():
    """Request a password reset"""
    if current_user.is_authenticated:
        return redirect(url_for('parent_dashboard'))
    
    form = RequestResetForm()
    
    if form.validate_on_submit():
        # Find parent by email
        parent = Parent.query.filter_by(email=form.email.data).first()
        
        # Generate reset token
        token = parent.get_reset_token()
        
        # Create reset URL with the server's hostname
        # Get the host from request or environment
        host = request.host_url.rstrip('/')
        if not host:
            host = os.environ.get('REPLIT_DEV_DOMAIN') or os.environ.get('REPLIT_DOMAIN')
            if host:
                host = f"https://{host}"
        
        # Create the reset URL
        reset_path = url_for('reset_password', token=token)
        reset_url = f"{host}{reset_path}"
        
        # Import email service
        from email_service import send_password_reset_email
        
        # Try to send email
        if send_password_reset_email(parent, token, reset_url):
            flash('A password reset link has been sent to your email address.', 'success')
            # Log reset request in session activity
            new_session = Session(
                user_type='parent', 
                user_id=parent.id,
                ip_address=request.remote_addr,
                user_agent=request.user_agent.string,
                device_type=detect_device_type(request.user_agent.string)
            )
            new_session.record_activity('password_reset_request')
            db.session.add(new_session)
            db.session.commit()
        else:
            flash('Failed to send reset email. Please try again later.', 'error')
            
        return redirect(url_for('parent_login'))
    
    return render_template('request_reset_password.html', form=form)


@app.route('/parent/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password with token"""
    if current_user.is_authenticated:
        return redirect(url_for('parent_dashboard'))
    
    # Verify token and get parent
    parent = Parent.verify_reset_token(token)
    
    if not parent:
        flash('Invalid or expired reset token. Please try again.', 'error')
        return redirect(url_for('request_reset_password'))
    
    form = ResetPasswordForm()
    
    if form.validate_on_submit():
        # Set new password
        parent.set_password(form.password.data)
        
        # Clear reset token
        parent.reset_password_token = None
        parent.reset_token_expires = None
        
        # Save changes
        db.session.commit()
        
        # Log password reset in session activity
        new_session = Session(
            user_type='parent', 
            user_id=parent.id,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string,
            device_type=detect_device_type(request.user_agent.string)
        )
        new_session.record_activity('password_reset_complete')
        db.session.add(new_session)
        db.session.commit()
        
        flash('Your password has been reset successfully! You can now log in with your new password.', 'success')
        return redirect(url_for('parent_login'))
    
    return render_template('reset_password.html', form=form)


@app.route('/guest_login', methods=['POST'])
def guest_login():
    """Guest login functionality with combined parent/child view"""
    form = EmptyForm()
    
    if form.validate_on_submit():
        # Create a guest parent account or find existing one
        guest_parent = Parent.query.filter_by(username='guest').first()
        
        if not guest_parent:
            # Create a new guest parent account if it doesn't exist
            guest_parent = Parent(
                username='guest',
                email='guest@example.com',
                is_guest=True
            )
            # Set a random password for security (even though it won't be used directly)
            guest_parent.set_password(str(uuid.uuid4()))
            db.session.add(guest_parent)
            db.session.commit()
            
            # Create parent settings if needed
            if not ParentSettings.query.filter_by(parent_id=guest_parent.id).first():
                guest_settings = ParentSettings(parent_id=guest_parent.id)
                db.session.add(guest_settings)
                db.session.commit()
            
            # Create a demo child account for the guest parent
            demo_child = Child(
                parent_id=guest_parent.id,
                username='demo_child',
                display_name='Demo Child',
                age=4,
                avatar='fox'
            )
            demo_child.set_pin('1234')
            db.session.add(demo_child)
            db.session.commit()
            
            # Approve some books for the demo child
            # Get books suitable for age 4-5
            age_group = AgeGroup.query.filter_by(name='4-5 years').first()
            if age_group:
                books = Book.query.filter_by(age_group_id=age_group.id).limit(5).all()
                for book in books:
                    approved_book = ApprovedBooks(child_id=demo_child.id, book_id=book.id, approved_by=guest_parent.id)
                    db.session.add(approved_book)
                db.session.commit()
                
            # Add some rewards and progress for demo purposes
            demo_reward = Reward(
                child_id=demo_child.id,
                badge_id='welcome_badge',
                badge_name='Welcome Badge',
                badge_description='Earned for trying the app as a guest',
                badge_image='stars.svg',
                source_type='achievement',
                points_value=10,
                achievement_level='bronze'
            )
            db.session.add(demo_reward)
            
            if books:
                demo_progress = Progress(
                    child_id=demo_child.id,
                    content_type='story',
                    content_id=books[0].id,
                    progress_value=50,
                    completed=False
                )
                db.session.add(demo_progress)
                db.session.commit()
        else:
            # Get the demo child for this parent
            demo_child = Child.query.filter_by(parent_id=guest_parent.id).first()
        
        # Log in as the guest parent
        login_user(guest_parent)
        
        # Store both parent and child info in session for combined access
        session['user_type'] = 'guest'
        
        # Store the demo child ID in the session for easy access
        if demo_child:
            session['guest_child_id'] = demo_child.id
        
        # Record login activity
        new_session = Session(
            user_type='guest', 
            user_id=guest_parent.id,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string,
            device_type=detect_device_type(request.user_agent.string)
        )
        new_session.record_activity('guest_login')
        db.session.add(new_session)
        db.session.commit()
        
        flash('Welcome to Children\'s Castle! You are signed in as a guest with access to both parent and child features.', 'success')
        return redirect(url_for('guest_dashboard'))
    
    # If form validation failed (CSRF)
    flash('Session expired. Please try again.', 'error')
    return redirect(url_for('parent_login'))


@app.route('/child/login', methods=['GET', 'POST'])
def child_login():
    """Login for child accounts"""
    if current_user.is_authenticated:
        return redirect(url_for('child_dashboard'))
    
    form = EmptyForm()
    
    if request.method == 'POST':
        # Using form validation for CSRF protection
        if not form.validate_on_submit():
            flash('Invalid form submission. Please try again.', 'error')
            return redirect(url_for('child_login'))
            
        username = request.form.get('username')
        pin = request.form.get('pin')
        
        child = Child.query.filter_by(username=username).first()
        
        if not child or not child.check_pin(pin):
            flash('Invalid username or PIN', 'error')
            return redirect(url_for('child_login'))
        
        # Log in the child
        login_user(child)
        session['user_type'] = 'child'
        
        # Record login session with additional metadata
        new_session = Session(
            user_type='child', 
            user_id=child.id,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string,
            device_type=detect_device_type(request.user_agent.string)
        )
        new_session.record_activity('login')
        db.session.add(new_session)
        db.session.commit()
        
        return redirect(url_for('child_dashboard'))
    
    # Get all children for visual selection
    children = Child.query.all()
    
    return render_template('child_login.html', form=form, children=children)


@app.route('/logout')
@login_required
def logout():
    """Logout the current user"""
    # Update session end time
    if 'user_type' in session:
        user_session = Session.query.filter_by(
            user_type=session['user_type'], 
            user_id=current_user.id,
            end_time=None
        ).order_by(Session.start_time.desc()).first()
        
        if user_session:
            user_session.record_activity('logout')
            user_session.close()  # This sets end_time and calculates duration
            db.session.commit()
    
    logout_user()
    session.pop('user_type', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))


@app.route('/guest/dashboard')
@login_required
def guest_dashboard():
    """Combined guest dashboard with both parent and child views"""
    if session.get('user_type') != 'guest':
        flash('Access denied. This page is for guest accounts only.', 'error')
        return redirect(url_for('index'))
    
    # Get the parent (current user) and associated demo child
    guest_parent = current_user
    demo_child_id = session.get('guest_child_id')
    demo_child = Child.query.filter_by(id=demo_child_id).first() if demo_child_id else None
    
    if not demo_child:
        # Something went wrong, fallback to parent dashboard
        session['user_type'] = 'parent'
        return redirect(url_for('parent_dashboard'))
    
    # Get all children for this parent (should be just the demo child)
    children = Child.query.filter_by(parent_id=guest_parent.id).all()
    
    # Get all age groups for book approval section
    age_groups = AgeGroup.query.order_by(AgeGroup.min_age).all()
    
    # Get child's progress and rewards for the child section
    progress = Progress.query.filter_by(child_id=demo_child.id).all()
    rewards = Reward.query.filter_by(child_id=demo_child.id).all()
    
    # Record dashboard access in session activity log
    user_session = Session.query.filter_by(
        user_type='guest',
        user_id=guest_parent.id,
        end_time=None
    ).order_by(Session.start_time.desc()).first()
    
    if user_session:
        user_session.record_activity('view_guest_dashboard')
        db.session.commit()
    
    return render_template('guest_dashboard.html', 
                          parent=guest_parent,
                          child=demo_child,
                          children=children, 
                          age_groups=age_groups,
                          progress=progress, 
                          rewards=rewards)

@app.route('/parent/dashboard')
@login_required
def parent_dashboard():
    """Parent dashboard"""
    if session.get('user_type') not in ['parent', 'guest']:
        flash('Access denied. This page is for parents only.', 'error')
        return redirect(url_for('index'))
    
    # Get all children for this parent
    children = Child.query.filter_by(parent_id=current_user.id).all()
    
    # Get all age groups for book approval section
    age_groups = AgeGroup.query.order_by(AgeGroup.min_age).all()
    
    # Record dashboard access in session activity log
    user_session = Session.query.filter_by(
        user_type='parent',
        user_id=current_user.id,
        end_time=None
    ).order_by(Session.start_time.desc()).first()
    
    if user_session:
        user_session.record_activity('view_dashboard')
        db.session.commit()
    
    return render_template('parent_dashboard.html', children=children, age_groups=age_groups)


@app.route('/parent/add-child', methods=['GET', 'POST'])
@login_required
def add_child():
    """Add a new child account"""
    if session.get('user_type') != 'parent':
        flash('Access denied. This page is for parents only.', 'error')
        return redirect(url_for('index'))
    
    form = EmptyForm()
    
    if request.method == 'POST':
        # Using form validation for CSRF protection
        if not form.validate_on_submit():
            flash('Invalid form submission. Please try again.', 'error')
            return redirect(url_for('add_child'))
        
        username = request.form.get('username')
        display_name = request.form.get('display_name')
        age = request.form.get('age')
        birthday = request.form.get('birthday')
        pin = request.form.get('pin')
        
        # Check if username already exists
        if Child.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('add_child'))
        
        # Create new child
        child = Child(
            username=username,
            display_name=display_name,
            parent_id=current_user.id,
            age=age,
            birthday=birthday
        )
        child.set_pin(pin)
        
        # Save to database
        db.session.add(child)
        db.session.commit()
        
        flash(f'Child account for {display_name} created successfully!', 'success')
        return redirect(url_for('parent_dashboard'))
    
    return render_template('add_child.html', form=form)


@app.route('/parent/reset-child-pin', methods=['POST'])
@login_required
def reset_child_pin():
    """Reset a child's PIN"""
    if session.get('user_type') != 'parent':
        flash('Access denied. This page is for parents only.', 'error')
        return redirect(url_for('index'))
    
    form = EmptyForm()
    
    if request.method == 'POST':
        # Using form validation for CSRF protection
        if not form.validate_on_submit():
            flash('Invalid form submission. Please try again.', 'error')
            return redirect(url_for('parent_dashboard'))
            
        child_id = request.form.get('child_id')
        new_pin = request.form.get('new_pin')
        
        # Verify PIN format
        if not new_pin or len(new_pin) != 4 or not new_pin.isdigit():
            flash('PIN must be exactly 4 digits.', 'error')
            return redirect(url_for('parent_dashboard'))
        
        # Get the child
        child = Child.query.filter_by(id=child_id, parent_id=current_user.id).first()
        if not child:
            flash('Child account not found.', 'error')
            return redirect(url_for('parent_dashboard'))
        
        # Reset the PIN
        child.set_pin(new_pin)
        db.session.commit()
        
        flash(f'PIN for {child.display_name} has been reset successfully!', 'success')
    else:
        flash('Invalid form submission.', 'error')
    
    return redirect(url_for('parent_dashboard'))


@app.route('/parent/edit-child', methods=['POST'])
@login_required
def parent_edit_child():
    """Edit a child account"""
    if session.get('user_type') != 'parent':
        flash('Access denied. This page is for parents only.', 'error')
        return redirect(url_for('index'))
    
    form = EmptyForm()
    
    # Using form validation for CSRF protection
    if not form.validate_on_submit():
        flash('Invalid form submission. Please try again.', 'error')
        return redirect(url_for('parent_dashboard'))
    
    # Get form data
    child_id = request.form.get('child_id')
    display_name = request.form.get('display_name')
    age = request.form.get('age')
    birthday = request.form.get('birthday')
    avatar = request.form.get('avatar')
    
    # Validate input
    if not child_id or not display_name or not age:
        flash('Missing required fields.', 'error')
        return redirect(url_for('parent_dashboard'))
    
    # Get the child and verify parent ownership
    child = Child.query.filter_by(id=child_id, parent_id=current_user.id).first()
    if not child:
        flash('Child not found or access denied.', 'error')
        return redirect(url_for('parent_dashboard'))
    
    # Update child information
    child.display_name = display_name
    child.age = int(age)
    
    if birthday:
        try:
            child.birthday = datetime.strptime(birthday, '%Y-%m-%d').date()
        except ValueError:
            # If date format is invalid, don't update this field
            pass
    
    if avatar:
        child.avatar = avatar
    
    # Save changes
    db.session.commit()
    
    flash(f'Profile for {child.display_name} updated successfully!', 'success')
    return redirect(url_for('parent_dashboard'))


@app.route('/child/dashboard')
@login_required
def child_dashboard():
    """Child dashboard"""
    if session.get('user_type') != 'child':
        flash('Access denied. This page is for children only.', 'error')
        return redirect(url_for('index'))
    
    # Get child's progress and rewards
    progress = Progress.query.filter_by(child_id=current_user.id).all()
    rewards = Reward.query.filter_by(child_id=current_user.id).all()
    
    # Record dashboard access in session activity log
    user_session = Session.query.filter_by(
        user_type='child',
        user_id=current_user.id,
        end_time=None
    ).order_by(Session.start_time.desc()).first()
    
    if user_session:
        user_session.record_activity('view_dashboard')
        db.session.commit()
    
    return render_template('child_dashboard.html', progress=progress, rewards=rewards)


@app.route('/parent/settings', methods=['GET', 'POST'])
@login_required
def parent_settings():
    """Parent settings page"""
    if session.get('user_type') != 'parent':
        flash('Access denied. This page is for parents only.', 'error')
        return redirect(url_for('index'))
    
    form = EmptyForm()
    settings = ParentSettings.query.filter_by(parent_id=current_user.id).first()
    
    if request.method == 'POST':
        # Using form validation for CSRF protection
        if not form.validate_on_submit():
            flash('Invalid form submission. Please try again.', 'error')
            return redirect(url_for('parent_settings'))
            
        # Basic Settings
        settings.allow_external_games = request.form.get('allow_external_games') == 'on'
        settings.max_daily_playtime = int(request.form.get('max_daily_playtime', 60))
        settings.content_age_filter = int(request.form.get('content_age_filter', 4))
        settings.notifications_enabled = request.form.get('notifications_enabled') == 'on'
        
        # Additional Settings if provided
        if request.form.get('max_weekly_playtime'):
            settings.max_weekly_playtime = int(request.form.get('max_weekly_playtime'))
        
        # Access Schedule
        if request.form.get('access_start_time'):
            settings.access_start_time = datetime.strptime(request.form.get('access_start_time'), '%H:%M').time()
        
        if request.form.get('access_end_time'):
            settings.access_end_time = datetime.strptime(request.form.get('access_end_time'), '%H:%M').time()
        
        # Audio & Visual Settings
        settings.enable_audio_narration = request.form.get('enable_audio_narration') == 'on'
        settings.enable_background_music = request.form.get('enable_background_music') == 'on'
        
        if request.form.get('narrator_voice_type'):
            settings.narrator_voice_type = request.form.get('narrator_voice_type')
        
        if request.form.get('reading_speed'):
            settings.reading_speed = float(request.form.get('reading_speed'))
        
        if request.form.get('sound_effects_volume'):
            settings.sound_effects_volume = int(request.form.get('sound_effects_volume'))
        
        # Theme Filters
        theme_filters = []
        if request.form.get('theme_friendship') == 'on':
            theme_filters.append('friendship')
        if request.form.get('theme_kindness') == 'on':
            theme_filters.append('kindness')
        if request.form.get('theme_adventure') == 'on':
            theme_filters.append('adventure')
        if request.form.get('theme_learning') == 'on':
            theme_filters.append('learning')
        if request.form.get('theme_problem_solving') == 'on':
            theme_filters.append('problem-solving')
        
        import json
        settings.story_theme_filters = json.dumps(theme_filters)
        
        # Rewards Settings
        if request.form.get('stars_per_story'):
            settings.stars_per_story = int(request.form.get('stars_per_story'))
        
        if request.form.get('stars_per_game'):
            settings.stars_per_game = int(request.form.get('stars_per_game'))
        
        # Email Reports
        settings.email_reports_enabled = request.form.get('email_reports_enabled') == 'on'
        
        if request.form.get('report_delivery_day'):
            settings.report_delivery_day = request.form.get('report_delivery_day')
        
        # Security Settings
        parent_pin = request.form.get('parent_pin')
        if parent_pin and len(parent_pin) == 4 and parent_pin.isdigit():
            settings.set_parent_pin(parent_pin)
        
        settings.require_parent_auth = request.form.get('require_parent_auth') == 'on'
        
        if request.form.get('session_timeout'):
            settings.session_timeout = int(request.form.get('session_timeout'))
        
        # Sync Settings
        settings.cloud_sync_enabled = request.form.get('cloud_sync_enabled') == 'on'
        
        if request.form.get('sync_frequency'):
            settings.sync_frequency = request.form.get('sync_frequency')
        
        # Record settings update in session activity log
        user_session = Session.query.filter_by(
            user_type='parent',
            user_id=current_user.id,
            end_time=None
        ).order_by(Session.start_time.desc()).first()
        
        if user_session:
            settings_changed = []
            if request.form.get('allow_external_games') == 'on' != settings.allow_external_games:
                settings_changed.append('allow_external_games')
            if int(request.form.get('max_daily_playtime', 60)) != settings.max_daily_playtime:
                settings_changed.append('max_daily_playtime')
            if int(request.form.get('content_age_filter', 4)) != settings.content_age_filter:
                settings_changed.append('content_age_filter')
            
            user_session.record_activity('update_settings', None, {
                'settings_changed': settings_changed
            })
        
        db.session.commit()
        flash('Settings updated successfully', 'success')
        return redirect(url_for('parent_settings'))
    
    return render_template('parent_settings.html', form=form, settings=settings)


@app.route('/api/child-activity/<int:child_id>')
@login_required
def child_activity(child_id):
    """API endpoint to get child's activity data for the dashboard"""
    if session.get('user_type') != 'parent':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    # Verify this child belongs to the current parent
    child = Child.query.filter_by(id=child_id, parent_id=current_user.id).first()
    if not child:
        return jsonify({'success': False, 'message': 'Child not found'}), 404
    
    # Get child's progress data
    story_progress = Progress.query.filter_by(
        child_id=child_id, 
        content_type='story'
    ).all()
    
    game_progress = Progress.query.filter_by(
        child_id=child_id, 
        content_type='game'
    ).all()
    
    # Get rewards
    rewards = Reward.query.filter_by(child_id=child_id).all()
    
    # Calculate statistics
    stories_read = sum(1 for p in story_progress if p.completed)
    games_played = sum(1 for p in game_progress if p.completed)
    total_time_spent = sum(p.time_spent for p in story_progress + game_progress) / 60  # Convert to minutes
    
    # Get the top stories and games
    top_stories = sorted(
        [p for p in story_progress if p.completed],
        key=lambda x: (x.completion_count, x.time_spent),
        reverse=True
    )[:5]
    
    top_games = sorted(
        [p for p in game_progress if p.completed],
        key=lambda x: (x.completion_count, x.time_spent),
        reverse=True
    )[:5]
    
    # Get skill progress if any
    skills = SkillProgress.query.filter_by(child_id=child_id).all()
    skill_data = {
        skill.skill_name: skill.skill_level
        for skill in skills
    }
    
    # Default skill levels if none exist
    default_skills = {
        'Reading': 30,
        'Counting': 25,
        'Problem Solving': 40,
        'Memory': 35,
        'Creativity': 50
    }
    
    # Merge with defaults
    for skill, level in default_skills.items():
        if skill not in skill_data:
            skill_data[skill] = level
    
    # Get learning goals
    goals = LearningGoal.query.filter_by(child_id=child_id).all()
    
    # Format the response data
    response_data = {
        'success': True,
        'child': {
            'id': child.id,
            'name': child.display_name,
            'age': child.age
        },
        'activity': {
            'stories_read': stories_read,
            'games_played': games_played,
            'total_time_spent': int(total_time_spent),
            'badges_earned': len(rewards)
        },
        'top_content': {
            'stories': [{
                'id': p.content_id,
                'title': p.content_id.replace('_', ' ').title(),
                'completion_count': p.completion_count,
                'last_accessed': p.last_accessed.isoformat()
            } for p in top_stories],
            'games': [{
                'id': p.content_id,
                'title': p.content_id.replace('_', ' ').title(),
                'completion_count': p.completion_count,
                'last_accessed': p.last_accessed.isoformat()
            } for p in top_games]
        },
        'rewards': [{
            'badge_id': r.badge_id,
            'badge_name': r.badge_name,
            'badge_description': r.badge_description,
            'badge_image': r.badge_image,
            'earned_at': r.earned_at.isoformat()
        } for r in rewards],
        'skills': skill_data,
        'goals': [{
            'id': g.id,
            'text': g.goal_text,
            'type': g.goal_type,
            'quantity': g.goal_quantity,
            'completed_quantity': g.completed_quantity,
            'completed': g.completed
        } for g in goals]
    }
    
    return jsonify(response_data)


@app.route('/api/save-learning-goal', methods=['POST'])
@login_required
@csrf.exempt
def save_learning_goal():
    """API endpoint to save a new learning goal for a child"""
    if session.get('user_type') != 'parent':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    data = request.json
    child_id = data.get('child_id')
    
    # Verify this child belongs to the current parent
    child = Child.query.filter_by(id=child_id, parent_id=current_user.id).first()
    if not child:
        return jsonify({'success': False, 'message': 'Child not found'}), 404
    
    goal_type = data.get('goal_type')
    goal_descriptor = data.get('goal_descriptor')
    goal_text = data.get('goal_text')
    goal_quantity = data.get('goal_quantity', 1)
    
    # Create new goal
    goal = LearningGoal(
        child_id=child_id,
        goal_type=goal_type,
        goal_descriptor=goal_descriptor,
        goal_text=goal_text,
        goal_quantity=goal_quantity
    )
    
    db.session.add(goal)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'goal': {
            'id': goal.id,
            'text': goal.goal_text,
            'type': goal.goal_type,
            'quantity': goal.goal_quantity,
            'completed_quantity': goal.completed_quantity,
            'completed': goal.completed
        }
    })


@app.route('/api/delete-learning-goal/<int:goal_id>', methods=['DELETE'])
@login_required
@csrf.exempt
def delete_learning_goal(goal_id):
    """API endpoint to delete a learning goal"""
    if session.get('user_type') != 'parent':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    # Get the goal and verify it belongs to a child of the current parent
    goal = LearningGoal.query.get(goal_id)
    
    if not goal:
        return jsonify({'success': False, 'message': 'Goal not found'}), 404
    
    child = Child.query.filter_by(id=goal.child_id, parent_id=current_user.id).first()
    if not child:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    db.session.delete(goal)
    db.session.commit()
    
    return jsonify({'success': True})


# API routes for approved books management
@app.route('/api/books/get-child-approved', methods=['GET'])
@login_required
@csrf.exempt
def get_child_approved_books():
    """API endpoint to get approved books for a child"""
    if session.get('user_type') != 'parent':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    child_id = request.args.get('child_id')
    if not child_id:
        return jsonify({'success': False, 'message': 'Child ID is required'}), 400
    
    # Verify this child belongs to the current parent
    child = Child.query.filter_by(id=child_id, parent_id=current_user.id).first()
    if not child:
        return jsonify({'success': False, 'message': 'Child not found'}), 404
    
    # Get approved books for this child
    approved_books = ApprovedBooks.query.filter_by(child_id=child_id).all()
    approved_book_ids = [ab.book_id for ab in approved_books]
    
    # Get all books with their details
    books = Book.query.all()
    
    # Format the books data
    books_data = []
    for book in books:
        age_group = AgeGroup.query.get(book.age_group_id)
        books_data.append({
            'id': book.id,
            'title': book.title,
            'description': book.description,
            'age_group': {
                'id': age_group.id,
                'name': age_group.name,
                'min_age': age_group.min_age,
                'max_age': age_group.max_age
            },
            'difficulty_level': book.difficulty_level,
            'reading_time_minutes': book.reading_time_minutes,
            'is_interactive': book.is_interactive,
            'has_audio': book.has_audio,
            'is_approved': book.id in approved_book_ids
        })
    
    return jsonify({
        'success': True,
        'child': {
            'id': child.id,
            'name': child.display_name,
            'age': child.age
        },
        'books': books_data
    })


@app.route('/api/books/approve', methods=['POST'])
@login_required
@csrf.exempt
def approve_books():
    """API endpoint to approve books for a child"""
    if session.get('user_type') != 'parent':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    data = request.json
    child_id = data.get('child_id')
    book_ids = data.get('book_ids', [])
    
    if not child_id:
        return jsonify({'success': False, 'message': 'Child ID is required'}), 400
    
    if not book_ids:
        return jsonify({'success': False, 'message': 'At least one book ID is required'}), 400
    
    # Verify this child belongs to the current parent
    child = Child.query.filter_by(id=child_id, parent_id=current_user.id).first()
    if not child:
        return jsonify({'success': False, 'message': 'Child not found'}), 404
    
    # Get existing approved books
    existing_approved = ApprovedBooks.query.filter_by(child_id=child_id).with_entities(ApprovedBooks.book_id).all()
    existing_approved_ids = [ab.book_id for ab in existing_approved]
    
    # Add new approvals
    new_approvals = []
    for book_id in book_ids:
        if book_id not in existing_approved_ids:
            # Verify the book exists
            book = Book.query.get(book_id)
            if book:
                new_approval = ApprovedBooks(
                    child_id=child_id,
                    book_id=book_id,
                    approved_by=current_user.id
                )
                db.session.add(new_approval)
                new_approvals.append(book_id)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'{len(new_approvals)} books approved for {child.display_name}',
        'approved_book_ids': new_approvals
    })


@app.route('/api/books/unapprove', methods=['POST'])
@login_required
@csrf.exempt
def unapprove_books():
    """API endpoint to remove book approvals for a child"""
    if session.get('user_type') != 'parent':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    data = request.json
    child_id = data.get('child_id')
    book_ids = data.get('book_ids', [])
    
    if not child_id:
        return jsonify({'success': False, 'message': 'Child ID is required'}), 400
    
    if not book_ids:
        return jsonify({'success': False, 'message': 'At least one book ID is required'}), 400
    
    # Verify this child belongs to the current parent
    child = Child.query.filter_by(id=child_id, parent_id=current_user.id).first()
    if not child:
        return jsonify({'success': False, 'message': 'Child not found'}), 404
    
    # Delete approvals
    for book_id in book_ids:
        approval = ApprovedBooks.query.filter_by(
            child_id=child_id,
            book_id=book_id
        ).first()
        
        if approval:
            db.session.delete(approval)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'{len(book_ids)} book approvals removed for {child.display_name}',
        'unapproved_book_ids': book_ids
    })


@app.route('/api/save-story-queue', methods=['POST'])
@login_required
@csrf.exempt
def save_story_queue():
    """API endpoint to save a custom story queue for a child"""
    if session.get('user_type') != 'parent':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    data = request.json
    child_id = data.get('child_id')
    story_ids = data.get('story_ids', [])
    
    # Verify this child belongs to the current parent
    child = Child.query.filter_by(id=child_id, parent_id=current_user.id).first()
    if not child:
        return jsonify({'success': False, 'message': 'Child not found'}), 404
    
    # Find existing queue or create new one
    queue = StoryQueue.query.filter_by(child_id=child_id).first()
    
    import json
    if queue:
        queue.story_ids = json.dumps(story_ids)
    else:
        queue = StoryQueue(
            child_id=child_id,
            story_ids=json.dumps(story_ids)
        )
        db.session.add(queue)
    
    db.session.commit()
    
    return jsonify({'success': True})


@app.route('/api/generate-pairing-code', methods=['POST'])
@login_required
@csrf.exempt
def generate_pairing_code():
    """API endpoint to generate a device pairing code"""
    if session.get('user_type') != 'parent':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    import random
    import string
    from datetime import timedelta
    
    # Generate random code
    letters = ''.join(random.choices(string.ascii_uppercase.replace('O', '').replace('I', ''), k=4))
    numbers = ''.join(random.choices(string.digits.replace('0', '').replace('1', ''), k=4))
    pairing_code = f"{letters}-{numbers}"
    
    # Set expiration to 24 hours from now
    expires_at = datetime.utcnow() + timedelta(hours=24)
    
    # Create pairing record
    pairing = DevicePairing(
        parent_id=current_user.id,
        pairing_code=pairing_code,
        device_type=request.json.get('device_type', 'unknown'),
        device_name=request.json.get('device_name', 'New Device'),
        expires_at=expires_at
    )
    
    db.session.add(pairing)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'pairing_code': pairing_code,
        'expires_at': expires_at.isoformat()
    })

@app.route('/link-to-parent', methods=['GET'])
@login_required
def link_to_parent():
    """Display the link to parent page with QR code"""
    import qrcode
    import io
    import base64
    from datetime import timedelta
    
    # Check if there's an existing active pairing code for the user
    if session.get('user_type') == 'parent':
        pairing = DevicePairing.query.filter_by(
            parent_id=current_user.id,
            is_active=True
        ).order_by(DevicePairing.created_at.desc()).first()
    else:
        # For child users, find their parent's pairing code
        child = Child.query.get(current_user.id)
        pairing = DevicePairing.query.filter_by(
            parent_id=child.parent_id,
            is_active=True
        ).order_by(DevicePairing.created_at.desc()).first()
    
    # Generate a new code if none exists or if it's expired
    if not pairing or (pairing.expires_at and pairing.expires_at < datetime.utcnow()):
        # Generate random code
        import random
        import string
        letters = ''.join(random.choices(string.ascii_uppercase.replace('O', '').replace('I', ''), k=4))
        numbers = ''.join(random.choices(string.digits.replace('0', '').replace('1', ''), k=4))
        pairing_code = f"{letters}-{numbers}"
        
        # Set expiration to 24 hours from now
        expires_at = datetime.utcnow() + timedelta(hours=24)
        
        # Get parent ID
        if session.get('user_type') == 'parent':
            parent_id = current_user.id
        else:
            child = Child.query.get(current_user.id)
            parent_id = child.parent_id
        
        # Create pairing record
        pairing = DevicePairing(
            parent_id=parent_id,
            pairing_code=pairing_code,
            device_type='companion-app',
            device_name='Companion App',
            expires_at=expires_at
        )
        
        db.session.add(pairing)
        db.session.commit()
    
    # Generate QR code containing the pairing code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(pairing.pairing_code)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert PIL image to base64
    buffered = io.BytesIO()
    img.save(buffered)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    
    return render_template('link_to_parent.html', 
                          pairing_code=pairing.pairing_code, 
                          qr_code=img_str, 
                          expires_at=pairing.expires_at)


@app.route('/api/generate-voice', methods=['POST'])
@login_required
@csrf.exempt
def generate_voice():
    """API endpoint to generate voice narration using ElevenLabs"""
    try:
        # Get request data
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'message': 'No data provided'}), 400
        
        text = data.get('text')
        voice_type = data.get('voice_type', 'narrator')
        story_title = data.get('story_title')
        
        if not text:
            return jsonify({'success': False, 'message': 'No text provided'}), 400
        
        # Check if it's a full story generation or just a text snippet
        if story_title:
            # Generate audio for an entire story
            output_path = generate_elevenlabs_audio.generate_story_audio(text, story_title)
            if output_path:
                audio_url = url_for('static', filename=output_path.replace('static/', ''))
                return jsonify({
                    'success': True, 
                    'audio_url': audio_url,
                    'message': f'Story audio generated for {story_title}'
                })
            else:
                return jsonify({'success': False, 'message': 'Failed to generate story audio'}), 500
        else:
            # Generate audio for a text snippet (character speech)
            output_dir = 'static/audio/snippets'
            os.makedirs(output_dir, exist_ok=True)
            
            # Create a unique filename based on a hash of the text
            import hashlib
            filename = hashlib.md5(text.encode()).hexdigest()
            output_path = f"{output_dir}/{filename}.mp3"
            
            result = generate_elevenlabs_audio.generate_character_audio(
                text, 
                character_type=voice_type, 
                output_path=output_path
            )
            
            if result:
                audio_url = url_for('static', filename=output_path.replace('static/', ''))
                return jsonify({
                    'success': True, 
                    'audio_url': audio_url,
                    'message': 'Audio generated successfully'
                })
            else:
                return jsonify({'success': False, 'message': 'Failed to generate audio'}), 500
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/voices')
@login_required
@csrf.exempt
def list_voices():
    """API endpoint to get available ElevenLabs voices with their IDs"""
    try:
        voices = generate_elevenlabs_audio.list_available_voices()
        return jsonify({'success': True, 'voices': voices})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/story-mode')
@login_required
def story_mode():
    """Story mode page for children"""
    if session.get('user_type') not in ['child', 'guest']:
        flash('Access denied. This page is for children only.', 'error')
        return redirect(url_for('index'))
    
    # Get all age groups
    age_groups = AgeGroup.query.order_by(AgeGroup.min_age).all()
    
    # Get child's age and information
    child = Child.query.get(current_user.id)
    child_age = child.age if child else 4  # Default to 4 if not set
    
    # Get parent settings for age filter
    parent_settings = None
    if child:
        parent = Parent.query.get(child.parent_id)
        if parent:
            parent_settings = ParentSettings.query.filter_by(parent_id=parent.id).first()
    
    # Apply content age filter if set in parent settings
    max_age_filter = None
    if parent_settings and parent_settings.content_age_filter:
        max_age_filter = parent_settings.content_age_filter
    
    # Filter age groups if needed
    if max_age_filter:
        age_groups = [group for group in age_groups if group.max_age <= max_age_filter]
    
    # Get approved books for this child
    approved_books_ids = []
    if child:
        approved_books = ApprovedBooks.query.filter_by(child_id=child.id).all()
        approved_books_ids = [ab.book_id for ab in approved_books]
    
    # Get all books and filter by approved books
    all_books = Book.query.all()
    
    # If we have approved books, only show those; otherwise show all books that match age filter
    if approved_books_ids:
        # Only show parent-approved books
        books = [book for book in all_books if book.id in approved_books_ids]
    else:
        # No approved books yet, so just filter by age (fallback behavior)
        books = all_books
        if max_age_filter:
            filtered_book_ids = [book.id for book in books if book.age_group_id in [g.id for g in age_groups]]
            books = [book for book in books if book.id in filtered_book_ids]
    
    # Check for enhanced stories with diverse audio narration (legacy support)
    enhanced_stories = []
    if os.path.exists(STORIES_DIR):
        for file in os.listdir(STORIES_DIR):
            if file.endswith('.json'):
                story_id = os.path.splitext(file)[0]
                try:
                    with open(os.path.join(STORIES_DIR, file), 'r') as f:
                        story_data = json.load(f)
                    
                    has_audio = all('audio' in page and page['audio'] 
                                   for page in story_data.get('pages', []))
                    
                    enhanced_stories.append({
                        'id': story_id,
                        'title': story_data.get('title', f"Story {story_id}"),
                        'has_audio': has_audio
                    })
                except Exception as e:
                    app.logger.warning(f"Error reading story file {file}: {str(e)}")
    
    # Record story mode access in session activity log
    user_session = Session.query.filter_by(
        user_type='child',
        user_id=current_user.id,
        end_time=None
    ).order_by(Session.start_time.desc()).first()
    
    if user_session:
        user_session.record_activity('view_story_mode')
        db.session.commit()
    
    return render_template('story_mode.html', age_groups=age_groups, books=books, 
                          enhanced_stories=enhanced_stories, child_age=child_age)


@app.route('/game-mode')
@login_required
def game_mode():
    """Game mode page for children"""
    if session.get('user_type') not in ['child', 'guest']:
        flash('Access denied. This page is for children only.', 'error')
        return redirect(url_for('index'))
    
    # Initialize settings
    settings = None
    
    # For regular child users, get parent settings
    if session.get('user_type') == 'child':
        # When current_user is a Child object, we can directly access the parent_id attribute
        from models import Child, Parent, ParentSettings
        if isinstance(current_user, Child) and hasattr(current_user, 'parent_id'):
            parent = Parent.query.get(current_user.parent_id)
            if parent:
                settings = ParentSettings.query.filter_by(parent_id=parent.id).first()
    
    # For guest users, use default settings that allow everything
    if session.get('user_type') == 'guest' or not settings:
        # Create default settings for guest users or when parent settings are not available
        from models import ParentSettings
        settings = ParentSettings()
        settings.allow_external_games = True
        settings.allow_chat_assistant = True
        settings.time_limit_minutes = 0  # No time limit
        settings.age_filter_min = 0
        settings.age_filter_max = 15
    
    # Record game mode access in session activity log
    from models import Session
    user_session = Session.query.filter_by(
        user_type='child',
        user_id=current_user.id,
        end_time=None
    ).order_by(Session.start_time.desc()).first()
    
    if user_session:
        user_session.record_activity('view_game_mode')
        db.session.commit()
    
    return render_template('game_mode.html', settings=settings)


@app.route('/rewards')
@login_required
def rewards():
    """Child's rewards page"""
    if session.get('user_type') not in ['child', 'guest']:
        flash('Access denied. This page is for children only.', 'error')
        return redirect(url_for('index'))
    
    # Get child's rewards from database
    from models import Reward
    child_rewards = Reward.query.filter_by(child_id=current_user.id).all()
    
    # Record rewards page access in session activity log
    user_session = Session.query.filter_by(
        user_type='child',
        user_id=current_user.id,
        end_time=None
    ).order_by(Session.start_time.desc()).first()
    
    if user_session:
        user_session.record_activity('view_rewards')
        db.session.commit()
    
    return render_template('rewards.html', rewards=child_rewards)


@app.route('/api/track-progress', methods=['POST'])
@login_required
@csrf.exempt
def track_progress():
    """API endpoint to track child's progress"""
    if session.get('user_type') not in ['child', 'guest']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    data = request.json
    content_type = data.get('content_type')  # 'story' or 'game'
    content_id = data.get('content_id')
    content_title = data.get('content_title', '')
    completed = data.get('completed', False)
    time_spent = data.get('time_spent', 0)  # in seconds
    pages_read = data.get('pages_read', 0)  # for stories
    score = data.get('score')  # for games
    difficulty_level = data.get('difficulty_level')  # 'easy', 'medium', 'hard'
    is_favorite = data.get('is_favorite', False)  # Track if user marked as favorite
    engagement_rating = data.get('engagement_rating')  # 1-5 rating
    
    # Find existing progress or create new
    from models import Progress
    progress = Progress.query.filter_by(
        child_id=current_user.id,
        content_type=content_type,
        content_id=content_id
    ).first()
    
    if progress:
        # Update basic fields
        progress.last_accessed = datetime.utcnow()
        progress.time_spent += time_spent
        progress.access_count += 1
        progress.last_session_duration = time_spent
        
        # Update engagement rating if provided
        if engagement_rating is not None:
            progress.engagement_rating = engagement_rating
        
        # Update favorite status if explicitly set
        if 'is_favorite' in data:
            progress.is_favorite = is_favorite
            
        # Update content-specific metrics
        if pages_read > progress.pages_read:
            progress.pages_read = pages_read
            
        if score is not None and (progress.score is None or score > progress.score):
            progress.score = score
            
        if difficulty_level and not progress.difficulty_level:
            progress.difficulty_level = difficulty_level
            
        if content_title and not progress.content_title:
            progress.content_title = content_title
            
        # Update streak information
        progress.update_streak()
        
        if completed and not progress.completed:
            progress.completed = True
            progress.completion_count += 1
            progress.add_completion_timestamp()
            
            # Add a reward if this is the first completion
            if progress.completion_count == 1:
                achievement_level = 'bronze'  # Default level
                
                # Determine level based on completion speed, score, etc.
                if content_type == 'game' and score is not None:
                    if score > 90:
                        achievement_level = 'gold'
                    elif score > 70:
                        achievement_level = 'silver'
                
                if content_type == 'story':
                    reward = Reward(
                        child_id=current_user.id,
                        badge_id=f"story_{content_id}",
                        badge_name=f"Story Master: {content_title or content_id.title()}",
                        badge_description=f"Completed the {content_title or content_id.title()} story",
                        badge_image=f"badges/story_{content_id}.png",
                        source_type='story',
                        source_id=content_id,
                        achievement_level=achievement_level,
                        points_value=2  # Default points for story completion
                    )
                else:  # game
                    reward = Reward(
                        child_id=current_user.id,
                        badge_id=f"game_{content_id}",
                        badge_name=f"Game Master: {content_title or content_id.title()}",
                        badge_description=f"Completed the {content_title or content_id.title()} game",
                        badge_image=f"badges/game_{content_id}.png",
                        source_type='game',
                        source_id=content_id,
                        achievement_level=achievement_level,
                        points_value=3  # Default points for game completion
                    )
                
                db.session.add(reward)
        elif completed:
            progress.completion_count += 1
            progress.add_completion_timestamp()
    else:
        progress = Progress(
            child_id=current_user.id,
            content_type=content_type,
            content_id=content_id,
            content_title=content_title,
            completed=completed,
            completion_count=1 if completed else 0,
            time_spent=time_spent,
            pages_read=pages_read,
            score=score,
            difficulty_level=difficulty_level,
            is_favorite=is_favorite,
            engagement_rating=engagement_rating,
            access_count=1,
            last_session_duration=time_spent
        )
        
        # Initialize streak information
        progress.update_streak()
        
        if completed:
            progress.add_completion_timestamp()
            
        db.session.add(progress)
    
    # Record this activity in the current session
    user_session = Session.query.filter_by(
        user_type='child',
        user_id=current_user.id,
        end_time=None
    ).order_by(Session.start_time.desc()).first()
    
    if user_session:
        activity_type = f"{content_type}_{'completion' if completed else 'progress'}"
        details = {
            'content_title': content_title or content_id,
            'time_spent': time_spent
        }
        if content_type == 'game' and score is not None:
            details['score'] = score
        elif content_type == 'story' and pages_read > 0:
            details['pages_read'] = pages_read
            
        user_session.record_activity(activity_type, content_id, details)
    
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'progress': {
            'content_id': progress.content_id,
            'content_title': progress.content_title,
            'completed': progress.completed,
            'completion_count': progress.completion_count,
            'time_spent': progress.time_spent,
            'pages_read': progress.pages_read,
            'score': progress.score,
            'difficulty_level': progress.difficulty_level
        }
    })


@app.route('/api/get-progress')
@login_required
@csrf.exempt
def get_progress():
    """API endpoint to get child's progress"""
    if session.get('user_type') not in ['child', 'guest']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    content_type = request.args.get('content_type')
    content_id = request.args.get('content_id')  # Optional filter for specific content
    
    from models import Progress
    query = Progress.query.filter_by(child_id=current_user.id)
    
    if content_type:
        query = query.filter_by(content_type=content_type)
        
    if content_id:
        query = query.filter_by(content_id=content_id)
        
    progress_items = query.all()
    
    progress_data = [{
        'content_type': item.content_type,
        'content_id': item.content_id,
        'content_title': item.content_title,
        'completed': item.completed,
        'completion_count': item.completion_count,
        'last_accessed': item.last_accessed.isoformat(),
        'first_accessed': item.first_accessed.isoformat() if item.first_accessed else None,
        'time_spent': item.time_spent,
        'pages_read': item.pages_read,
        'score': item.score,
        'difficulty_level': item.difficulty_level,
        'is_favorite': item.is_favorite,
        'engagement_rating': item.engagement_rating,
        'access_count': item.access_count,
        'last_session_duration': item.last_session_duration,
        'average_session_time': item.average_session_time,
        'streak_count': item.streak_count,
        'last_streak_date': item.last_streak_date.isoformat() if item.last_streak_date else None,
        'error_count': item.error_count
    } for item in progress_items]
    
    # Calculate statistics
    total_time = sum(item.time_spent for item in progress_items)
    completed_count = sum(1 for item in progress_items if item.completed)
    
    stories_read = sum(1 for item in progress_items 
                       if item.content_type == 'story' and item.completed)
    games_played = sum(1 for item in progress_items 
                       if item.content_type == 'game' and item.completed)
    
    return jsonify({
        'success': True,
        'progress': progress_data,
        'stats': {
            'total_items': len(progress_items),
            'completed_items': completed_count,
            'total_time_spent': total_time,
            'stories_read': stories_read,
            'games_played': games_played
        }
    })


@app.route('/api/story/<story_id>')
@login_required
def get_story_content(story_id):
    """API endpoint to get a story's content"""
    if session.get('user_type') not in ['child', 'guest']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    # First try to find the book in the database
    from models import Book
    book = Book.query.filter_by(file_name=f"{story_id}.txt").first()
    
    if book:
        try:
            with open(book.file_name, 'r') as f:
                content = f.read()
            
            # Track this story view
            progress = Progress.query.filter_by(
                child_id=current_user.id,
                content_type='story',
                content_id=story_id
            ).first()
            
            if not progress:
                progress = Progress(
                    child_id=current_user.id,
                    content_type='story',
                    content_id=story_id,
                    content_title=book.title,
                    completed=False,
                    access_count=1,
                    last_session_duration=0
                )
                db.session.add(progress)
            else:
                progress.last_accessed = datetime.utcnow()
                progress.access_count += 1
            
            progress.update_streak()
            db.session.commit()
            
            return jsonify({
                'success': True,
                'content': content,
                'title': book.title,
                'author': book.author,
                'description': book.description,
                'age_group': book.age_group.name,
                'difficulty_level': book.difficulty_level,
                'reading_time_minutes': book.reading_time_minutes
            })
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error reading story: {str(e)}'}), 500
    
    # If not found in the database, try the legacy story files
    try:
        # Check for .txt file
        if os.path.exists(f"{story_id}.txt"):
            with open(f"{story_id}.txt", 'r') as f:
                content = f.read()
                
            # Also track this view
            progress = Progress.query.filter_by(
                child_id=current_user.id,
                content_type='story',
                content_id=story_id
            ).first()
            
            if not progress:
                progress = Progress(
                    child_id=current_user.id,
                    content_type='story',
                    content_id=story_id,
                    content_title=story_id.replace('_', ' ').title(),
                    completed=False,
                    access_count=1,
                    last_session_duration=0
                )
                db.session.add(progress)
            else:
                progress.last_accessed = datetime.utcnow()
                progress.access_count += 1
            
            progress.update_streak()
            db.session.commit()
            
            return jsonify({
                'success': True,
                'content': content,
                'title': story_id.replace('_', ' ').title()
            })
        
        # Check for enhanced JSON-based story
        if os.path.exists(os.path.join(STORIES_DIR, f"{story_id}.json")):
            with open(os.path.join(STORIES_DIR, f"{story_id}.json"), 'r') as f:
                story_data = json.load(f)
            
            # For enhanced stories, we combine all page content
            content = story_data.get('title', '')
            for i, page in enumerate(story_data.get('pages', [])):
                content += f"\n\n--- Page {i+1} ---\n\n"
                content += page.get('text', '')
            
            # Track this view
            progress = Progress.query.filter_by(
                child_id=current_user.id,
                content_type='story',
                content_id=story_id
            ).first()
            
            if not progress:
                progress = Progress(
                    child_id=current_user.id,
                    content_type='story',
                    content_id=story_id,
                    content_title=story_data.get('title', story_id.replace('_', ' ').title()),
                    completed=False,
                    access_count=1,
                    last_session_duration=0
                )
                db.session.add(progress)
            else:
                progress.last_accessed = datetime.utcnow()
                progress.access_count += 1
            
            progress.update_streak()
            db.session.commit()
            
            return jsonify({
                'success': True,
                'content': content,
                'title': story_data.get('title', story_id.replace('_', ' ').title()),
                'enhanced': True,
                'pages': story_data.get('pages', [])
            })
        
        # Story not found
        return jsonify({'success': False, 'message': 'Story not found'}), 404
        
    except Exception as e:
        return jsonify({'success': False, 'message': f'Error loading story: {str(e)}'}), 500


@app.route('/api/get-rewards')
@login_required
@csrf.exempt
def get_rewards():
    """API endpoint to get child's rewards"""
    if session.get('user_type') not in ['child', 'guest']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    # Optional filters
    source_type = request.args.get('source_type')  # 'story', 'game', 'achievement', etc.
    achievement_level = request.args.get('achievement_level')  # 'bronze', 'silver', 'gold', etc.
    
    query = Reward.query.filter_by(child_id=current_user.id)
    
    if source_type:
        query = query.filter_by(source_type=source_type)
        
    if achievement_level:
        query = query.filter_by(achievement_level=achievement_level)
    
    # If showcase is specified, prioritize showcase rewards
    if request.args.get('showcase') == 'true':
        rewards = query.order_by(Reward.showcase_priority.desc(), Reward.earned_at.desc()).all()
    else:
        rewards = query.order_by(Reward.earned_at.desc()).all()
    
    rewards_data = [{
        'badge_id': reward.badge_id,
        'badge_name': reward.badge_name,
        'badge_description': reward.badge_description,
        'badge_image': reward.badge_image,
        'earned_at': reward.earned_at.isoformat(),
        'source_type': reward.source_type,
        'source_id': reward.source_id,
        'achievement_level': reward.achievement_level,
        'points_value': reward.points_value,
        'showcase_priority': reward.showcase_priority
    } for reward in rewards]
    
    # Calculate statistics by achievement level
    achievement_stats = {}
    for level in ['bronze', 'silver', 'gold', 'platinum', 'diamond']:
        level_count = sum(1 for r in rewards if r.achievement_level == level)
        if level_count > 0:
            achievement_stats[level] = level_count
    
    # Calculate total points/stars earned
    total_points = sum(r.points_value for r in rewards if r.points_value)
    
    return jsonify({
        'success': True,
        'rewards': rewards_data,
        'total_rewards': len(rewards_data),
        'achievement_stats': achievement_stats,
        'total_points': total_points
    })


@app.route('/api/session-stats', methods=['GET'])
@login_required
@csrf.exempt
def session_stats():
    """API endpoint to get session statistics"""
    if session.get('user_type') != 'parent':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
        
    # For parent, get their own sessions and their children's sessions
    from models import Child, Session
    parent_sessions = Session.query.filter_by(
        user_type='parent',
        user_id=current_user.id
    ).all()
    
    children = Child.query.filter_by(parent_id=current_user.id).all()
    child_ids = [child.id for child in children]
    
    child_sessions = Session.query.filter(
        Session.user_type == 'child',
        Session.user_id.in_(child_ids)
    ).all()
    
    # Calculate statistics
    today = datetime.now().date()
    this_week_start = today - timedelta(days=today.weekday())
    this_month_start = datetime(today.year, today.month, 1).date()
    
    # Parent stats
    parent_stats = {
        'total_sessions': len(parent_sessions),
        'total_time': sum(s.duration or 0 for s in parent_sessions) / 3600,  # hours
        'sessions_today': sum(1 for s in parent_sessions if s.start_time.date() == today),
        'sessions_this_week': sum(1 for s in parent_sessions if s.start_time.date() >= this_week_start),
        'sessions_this_month': sum(1 for s in parent_sessions if s.start_time.date() >= this_month_start),
        'device_breakdown': {}
    }
    
    # Count sessions by device type
    for s in parent_sessions:
        device = s.device_type or 'unknown'
        parent_stats['device_breakdown'][device] = parent_stats['device_breakdown'].get(device, 0) + 1
    
    # Child stats (combined and individual)
    child_stats = {
        'total': {
            'total_sessions': len(child_sessions),
            'total_time': sum(s.duration or 0 for s in child_sessions) / 3600,  # hours
            'sessions_today': sum(1 for s in child_sessions if s.start_time.date() == today),
            'sessions_this_week': sum(1 for s in child_sessions if s.start_time.date() >= this_week_start),
            'sessions_this_month': sum(1 for s in child_sessions if s.start_time.date() >= this_month_start),
        },
        'by_child': {}
    }
    
    # Calculate per-child stats
    for child in children:
        child_data = {
            'id': child.id,
            'name': child.display_name,
            'sessions': []
        }
        
        child_session_list = [s for s in child_sessions if s.user_id == child.id]
        
        # Include recent sessions
        for s in sorted(child_session_list, key=lambda x: x.start_time, reverse=True)[:10]:
            session_data = {
                'start_time': s.start_time.isoformat(),
                'end_time': s.end_time.isoformat() if s.end_time else None,
                'duration': s.duration / 60 if s.duration else None,  # minutes
                'device_type': s.device_type
            }
            
            # Parse activities
            if s.activities:
                import json
                try:
                    activities = json.loads(s.activities)
                    session_data['activities'] = activities
                except:
                    session_data['activities'] = []
            else:
                session_data['activities'] = []
                
            child_data['sessions'].append(session_data)
            
        # Calculate totals
        child_data['total_sessions'] = len(child_session_list)
        child_data['total_time'] = sum(s.duration or 0 for s in child_session_list) / 3600  # hours
        child_data['sessions_today'] = sum(1 for s in child_session_list if s.start_time.date() == today)
        
        child_stats['by_child'][child.id] = child_data
    
    return jsonify({
        'success': True,
        'parent_stats': parent_stats,
        'child_stats': child_stats
    })


# Import tracking helpers
import tracking
from models import Milestone, Progress

@app.route('/api/track-event', methods=['POST'])
@login_required
@csrf.exempt
def track_event():
    """API endpoint to track custom events"""
    data = request.json
    event_type = data.get('event_type')
    event_name = data.get('event_name')
    event_data = data.get('event_data')
    
    if not event_type or not event_name:
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400
    
    event = tracking.track_custom_event(event_type, event_name, event_data)
    
    return jsonify({'success': True, 'event_id': event.id})

@app.route('/api/log-error', methods=['POST'])
@login_required
@csrf.exempt
def log_error():
    """API endpoint to log errors"""
    data = request.json
    error_type = data.get('error_type')
    error_message = data.get('error_message')
    error_context = data.get('error_context')
    stack_trace = data.get('stack_trace')
    
    if not error_type or not error_message:
        return jsonify({'success': False, 'message': 'Missing required fields'}), 400
    
    error_log = tracking.log_error(error_type, error_message, error_context, stack_trace)
    
    return jsonify({'success': True, 'error_id': error_log.id})

@app.route('/api/get-milestones')
@login_required
@csrf.exempt
def get_milestones():
    """API endpoint to get child's milestones"""
    if session.get('user_type') not in ['child', 'guest']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    # Get milestones for the current child - using proper table name
    from models import db
    milestones = db.session.query(Milestone).filter_by(child_id=current_user.id).all()
    
    # Format milestone data
    milestones_data = [{
        'id': m.id,
        'milestone_id': m.milestone_id,
        'milestone_type': m.milestone_type,
        'milestone_name': m.milestone_name,
        'milestone_description': m.milestone_description,
        'progress': m.progress,
        'target_value': m.target_value,
        'completed': m.completed,
        'earned_at': m.earned_at.isoformat() if m.earned_at else None,
        'created_at': m.created_at.isoformat()
    } for m in milestones]
    
    # Check and create any new milestones
    new_milestones = tracking.check_and_create_milestones(current_user.id)
    
    # Add new milestones to response if any were created
    if new_milestones:
        for m in new_milestones:
            milestones_data.append({
                'id': m.id,
                'milestone_id': m.milestone_id,
                'milestone_type': m.milestone_type,
                'milestone_name': m.milestone_name,
                'milestone_description': m.milestone_description,
                'progress': m.progress,
                'target_value': m.target_value,
                'completed': m.completed,
                'earned_at': m.earned_at.isoformat() if m.earned_at else None,
                'created_at': m.created_at.isoformat()
            })
    
    return jsonify({
        'success': True,
        'milestones': milestones_data,
        'total_milestones': len(milestones_data),
        'completed_milestones': sum(1 for m in milestones if m.completed)
    })

@app.route('/api/get-favorites')
@login_required
@csrf.exempt
def get_favorites():
    """API endpoint to get child's favorite content"""
    if session.get('user_type') not in ['child', 'guest']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    content_type = request.args.get('content_type')  # Optional filter for stories or games
    limit = int(request.args.get('limit', 5))
    
    favorites = tracking.get_favorites(current_user.id, content_type, limit)
    
    # Format favorite data
    favorite_data = [{
        'content_type': item.content_type,
        'content_id': item.content_id,
        'content_title': item.content_title,
        'is_explicit_favorite': item.is_favorite,
        'completion_count': item.completion_count,
        'time_spent': item.time_spent,
        'last_accessed': item.last_accessed.isoformat()
    } for item in favorites]
    
    return jsonify({
        'success': True,
        'favorites': favorite_data
    })

@app.route('/api/toggle-favorite', methods=['POST'])
@login_required
@csrf.exempt
def toggle_favorite():
    """API endpoint to toggle favorite status for content"""
    if session.get('user_type') not in ['child', 'guest']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    data = request.json
    content_type = data.get('content_type')
    content_id = data.get('content_id')
    
    if not content_type or not content_id:
        return jsonify({'success': False, 'message': 'Missing content information'}), 400
    
    # Find the progress record
    progress = Progress.query.filter_by(
        child_id=current_user.id,
        content_type=content_type,
        content_id=content_id
    ).first()
    
    if not progress:
        return jsonify({'success': False, 'message': 'Content not found in progress'}), 404
    
    # Toggle favorite status
    progress.is_favorite = not progress.is_favorite
    db.session.commit()
    
    # Track this as an event
    tracking.track_custom_event(
        'favorite', 
        f"{'add' if progress.is_favorite else 'remove'}_favorite",
        {
            'content_type': content_type,
            'content_id': content_id,
            'content_title': progress.content_title
        }
    )
    
    return jsonify({
        'success': True,
        'is_favorite': progress.is_favorite
    })


# ----- Daily/Weekly Reports Routes -----

@app.route('/parent/reports')
@login_required
def parent_reports_dashboard():
    """Parent reports dashboard - shows all children's reports"""
    if session.get('user_type') != 'parent':
        flash('Access denied. This page is for parents only.', 'error')
        return redirect(url_for('index'))
    
    # Get all children for this parent
    children = Child.query.filter_by(parent_id=current_user.id).all()
    
    # Record dashboard access in session activity log
    user_session = Session.query.filter_by(
        user_type='parent',
        user_id=current_user.id,
        end_time=None
    ).order_by(Session.start_time.desc()).first()
    
    if user_session:
        user_session.record_activity('view_reports_dashboard')
        db.session.commit()
    
    return render_template('parent_reports.html', children=children)


@app.route('/parent/reports/<int:child_id>')
@login_required
def child_reports(child_id):
    """Individual child's reports dashboard"""
    if session.get('user_type') != 'parent':
        flash('Access denied. This page is for parents only.', 'error')
        return redirect(url_for('index'))
    
    # Verify the child belongs to this parent
    child = Child.query.filter_by(id=child_id, parent_id=current_user.id).first()
    if not child:
        flash('Child not found or access denied.', 'error')
        return redirect(url_for('parent_reports_dashboard'))
    
    # Get period parameters
    period_type = request.args.get('period', 'week')
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    
    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        except ValueError:
            start_date = None
    
    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            end_date = None
    
    # Get the report data
    report_data = get_report_data_for_period(child_id, period_type, start_date, end_date)
    chart_data = generate_chart_data(report_data)
    
    # Record access in session activity log
    user_session = Session.query.filter_by(
        user_type='parent',
        user_id=current_user.id,
        end_time=None
    ).order_by(Session.start_time.desc()).first()
    
    if user_session:
        user_session.record_activity('view_child_report', str(child_id), {'period': period_type})
        db.session.commit()
    
    return render_template(
        'child_reports.html', 
        child=child, 
        report_data=report_data, 
        chart_data=chart_data,
        period_type=period_type
    )


@app.route('/api/reports/generate-daily', methods=['POST'])
@login_required
@csrf.exempt
def api_generate_daily_report():
    """API endpoint to generate a daily report for a child"""
    if session.get('user_type') != 'parent':
        return jsonify({'success': False, 'error': 'Access denied'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Invalid request'}), 400
    
    child_id = data.get('child_id')
    report_date = data.get('date')
    
    # Verify the child belongs to this parent
    child = Child.query.filter_by(id=child_id, parent_id=current_user.id).first()
    if not child:
        return jsonify({'success': False, 'error': 'Child not found or access denied'}), 404
    
    # Parse the date if provided
    if report_date:
        try:
            report_date = datetime.strptime(report_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'success': False, 'error': 'Invalid date format'}), 400
    
    # Generate the report
    try:
        report = generate_daily_report(child_id, report_date)
        return jsonify({
            'success': True, 
            'report_id': report.id,
            'date': report.report_date.strftime('%Y-%m-%d'),
            'stories_read': report.stories_read,
            'games_played': report.games_played,
            'time_spent': report.time_spent
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/reports/generate-weekly', methods=['POST'])
@login_required
@csrf.exempt
def api_generate_weekly_report():
    """API endpoint to generate a weekly report for a child"""
    if session.get('user_type') != 'parent':
        return jsonify({'success': False, 'error': 'Access denied'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Invalid request'}), 400
    
    child_id = data.get('child_id')
    week_start = data.get('week_start')
    
    # Verify the child belongs to this parent
    child = Child.query.filter_by(id=child_id, parent_id=current_user.id).first()
    if not child:
        return jsonify({'success': False, 'error': 'Child not found or access denied'}), 404
    
    # Parse the date if provided
    if week_start:
        try:
            week_start = datetime.strptime(week_start, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'success': False, 'error': 'Invalid date format'}), 400
    
    # Generate the report
    try:
        report = generate_weekly_report(child_id, week_start)
        if not report:
            return jsonify({'success': False, 'error': 'Could not generate report for this period'}), 400
            
        return jsonify({
            'success': True, 
            'report_id': report.id,
            'week_start': report.week_start.strftime('%Y-%m-%d'),
            'week_end': report.week_end.strftime('%Y-%m-%d'),
            'stories_read': report.stories_read,
            'games_played': report.games_played,
            'time_spent': report.time_spent
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/reports/data/<int:child_id>')
@login_required
def api_get_report_data(child_id):
    """API endpoint to get report data for a child"""
    if session.get('user_type') != 'parent':
        return jsonify({'success': False, 'error': 'Access denied'}), 403
    
    # Verify the child belongs to this parent
    child = Child.query.filter_by(id=child_id, parent_id=current_user.id).first()
    if not child:
        return jsonify({'success': False, 'error': 'Child not found or access denied'}), 404
    
    # Get period parameters
    period_type = request.args.get('period', 'week')
    start_date = request.args.get('start')
    end_date = request.args.get('end')
    
    # Parse dates if provided
    if start_date:
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'success': False, 'error': 'Invalid start date format'}), 400
    
    if end_date:
        try:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'success': False, 'error': 'Invalid end date format'}), 400
    
    # Get the report data
    try:
        report_data = get_report_data_for_period(child_id, period_type, start_date, end_date)
        chart_data = generate_chart_data(report_data)
        
        return jsonify({
            'success': True,
            'report_data': report_data,
            'chart_data': chart_data
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/reports/emotional-feedback', methods=['POST'])
@login_required
@csrf.exempt
def api_record_emotional_feedback():
    """API endpoint to record emotional feedback for content"""
    # Check authentication
    if session.get('user_type') not in ['child', 'guest']:
        return jsonify({'success': False, 'error': 'Authentication required'}), 401
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'error': 'Invalid request'}), 400
    
    content_type = data.get('content_type')
    content_id = data.get('content_id')
    emoji = data.get('emoji')
    reaction = data.get('reaction')
    
    if not content_type or not content_id or not emoji:
        return jsonify({'success': False, 'error': 'Missing required parameters'}), 400
    
    # Record emotional feedback as an event
    event_data = {
        'content_type': content_type,
        'content_id': content_id,
        'emoji': emoji,
        'reaction': reaction
    }
    
    # Find the current session
    user_session = Session.query.filter_by(
        user_type='child',
        user_id=current_user.id,
        end_time=None
    ).order_by(Session.start_time.desc()).first()
    
    # Create the event
    Event.track_event(
        user_type='child',
        user_id=current_user.id,
        event_type='emotional_feedback',
        event_name='emoji_reaction',
        event_data=event_data,
        session_id=user_session.id if user_session else None
    )
    
    return jsonify({
        'success': True,
        'message': 'Emotional feedback recorded'
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)


# Book Approval API Routes

@app.route('/api/books/get-child-approved', methods=['GET'])
@login_required
@csrf.exempt
def api_get_child_approved_books():
    """API endpoint to get books approved for a child"""
    # Get child ID from query parameters
    child_id = request.args.get('child_id')
    
    if not child_id:
        return jsonify({'success': False, 'message': 'Child ID is required'}), 400
    
    # Parent can only view their own children's approved books
    if session.get('user_type') == 'parent':
        child = Child.query.filter_by(id=child_id, parent_id=current_user.id).first()
        if not child:
            return jsonify({'success': False, 'message': 'Child not found or not authorized'}), 403
    # Child can only view their own approved books
    elif session.get('user_type') == 'child':
        if str(current_user.id) != str(child_id):
            return jsonify({'success': False, 'message': 'Not authorized'}), 403
    # Guest users have access to all books
    elif session.get('user_type') == 'guest':
        pass
    else:
        return jsonify({'success': False, 'message': 'Not authorized'}), 403
    
    # Get all books with approval status for this child
    all_books = Book.query.all()
    
    # For each book, check if it's approved for this child
    books_with_status = []
    for book in all_books:
        approval = ApprovedBooks.query.filter_by(
            child_id=child_id,
            book_id=book.id
        ).first()
        
        # Get the age group for the book
        age_group = AgeGroup.query.get(book.age_group_id)
        
        books_with_status.append({
            'id': book.id,
            'title': book.title,
            'description': book.description,
            'difficulty_level': book.difficulty_level,
            'reading_time_minutes': book.reading_time_minutes,
            'age_group': {
                'id': age_group.id,
                'name': age_group.name,
                'min_age': age_group.min_age,
                'max_age': age_group.max_age
            },
            'is_approved': approval is not None
        })
    
    return jsonify({
        'success': True,
        'books': books_with_status
    })


@app.route('/api/books/approve', methods=['POST'])
@login_required
@csrf.exempt
def api_approve_books():
    """API endpoint to approve books for a child"""
    # Ensure user is a parent
    if session.get('user_type') != 'parent':
        return jsonify({'success': False, 'message': 'Only parents can approve books'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'Invalid request data'}), 400
    
    child_id = data.get('child_id')
    book_ids = data.get('book_ids', [])
    
    if not child_id or not book_ids:
        return jsonify({'success': False, 'message': 'Child ID and book IDs are required'}), 400
    
    # Check if child belongs to this parent
    child = Child.query.filter_by(id=child_id, parent_id=current_user.id).first()
    if not child:
        return jsonify({'success': False, 'message': 'Child not found or not authorized'}), 403
    
    # Approve each book
    approved_count = 0
    for book_id in book_ids:
        # Check if book exists
        book = Book.query.get(book_id)
        if not book:
            continue
        
        # Check if already approved
        existing = ApprovedBooks.query.filter_by(
            child_id=child_id,
            book_id=book_id
        ).first()
        
        if not existing:
            # Create approval record
            approval = ApprovedBooks(
                child_id=child_id,
                book_id=book_id,
                approved_by=current_user.id
            )
            db.session.add(approval)
            approved_count += 1
    
    if approved_count > 0:
        # Log activity in parent session
        user_session = Session.query.filter_by(
            user_type='parent',
            user_id=current_user.id,
            end_time=None
        ).order_by(Session.start_time.desc()).first()
        
        if user_session:
            user_session.record_activity('approve_books', {
                'child_id': child_id,
                'book_count': approved_count
            })
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{approved_count} book(s) approved for {child.display_name}'
        })
    else:
        return jsonify({
            'success': True,
            'message': 'No new books were approved'
        })


@app.route('/api/books/unapprove', methods=['POST'])
@login_required
@csrf.exempt
def api_unapprove_books():
    """API endpoint to remove book approvals for a child"""
    # Ensure user is a parent
    if session.get('user_type') != 'parent':
        return jsonify({'success': False, 'message': 'Only parents can manage book approvals'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': 'Invalid request data'}), 400
    
    child_id = data.get('child_id')
    book_ids = data.get('book_ids', [])
    
    if not child_id or not book_ids:
        return jsonify({'success': False, 'message': 'Child ID and book IDs are required'}), 400
    
    # Check if child belongs to this parent
    child = Child.query.filter_by(id=child_id, parent_id=current_user.id).first()
    if not child:
        return jsonify({'success': False, 'message': 'Child not found or not authorized'}), 403
    
    # Remove approvals
    removed_count = 0
    for book_id in book_ids:
        # Delete the approval record
        deleted = ApprovedBooks.query.filter_by(
            child_id=child_id,
            book_id=book_id
        ).delete()
        
        if deleted:
            removed_count += 1
    
    if removed_count > 0:
        # Log activity in parent session
        user_session = Session.query.filter_by(
            user_type='parent',
            user_id=current_user.id,
            end_time=None
        ).order_by(Session.start_time.desc()).first()
        
        if user_session:
            user_session.record_activity('unapprove_books', {
                'child_id': child_id,
                'book_count': removed_count
            })
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Approval removed for {removed_count} book(s)'
        })
    else:
        return jsonify({
            'success': True,
            'message': 'No approvals were removed'
        })

# Admin routes
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard to view app statistics and parent emails"""
    # Get current user type from the database directly
    parent = Parent.query.filter_by(id=current_user.id).first()
    
    # Admin is user with ID 1
    if not parent or parent.id != 1:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    # Get statistics
    stats = {
        'parent_count': Parent.query.count(),
        'child_count': Child.query.count(),
        'active_sessions_today': Session.query.filter(
            Session.start_time >= datetime.combine(date.today(), datetime.min.time()),
            Session.end_time.is_(None)
        ).count(),
        'total_stories_read': Progress.query.filter_by(content_type='story', completed=True).count(),
        'new_parents_last_month': Parent.query.filter(
            Parent.created_at >= datetime.now() - timedelta(days=30)
        ).count(),
        'new_children_last_month': Child.query.filter(
            Child.created_at >= datetime.now() - timedelta(days=30)
        ).count(),
    }
    
    # Get system health information
    import psutil
    import platform
    import sys
    
    # Check if OpenAI API key is configured
    openai_key_status = bool(os.environ.get('OPENAI_API_KEY'))
    
    # Check if ElevenLabs API key is configured
    elevenlabs_key_status = bool(os.environ.get('ELEVENLABS_API_KEY'))
    
    # Check database connection
    db_status = True
    try:
        db.session.execute(db.select(Parent).limit(1))
    except Exception:
        db_status = False
    
    system_health = {
        'cpu_usage': round(psutil.cpu_percent(), 1),
        'memory_usage': round(psutil.virtual_memory().percent, 1),
        'disk_usage': round(psutil.disk_usage('/').percent, 1),
        'python_version': platform.python_version(),
        'os_info': f"{platform.system()} {platform.release()}",
        'app_uptime': datetime.now() - datetime.fromtimestamp(psutil.boot_time()),
        'database_status': db_status,
        'openai_api_configured': openai_key_status,
        'elevenlabs_api_configured': elevenlabs_key_status,
        'database_size': get_database_size(),
        'error_count_24h': Event.query.filter(
            Event.event_name == 'error',
            Event.occurred_at >= datetime.now() - timedelta(hours=24)
        ).count()
    }
    
    # Get recent parent registrations
    recent_parents = Parent.query.order_by(Parent.created_at.desc()).limit(10).all()
    
    # Get all parents for email list
    all_parents = Parent.query.order_by(Parent.email).all()
    
    # Get recent error events
    recent_errors = Event.query.filter_by(event_name='error').order_by(Event.occurred_at.desc()).limit(10).all()
    
    return render_template(
        'admin_dashboard.html', 
        stats=stats,
        system_health=system_health,
        recent_parents=recent_parents,
        all_parents=all_parents,
        recent_errors=recent_errors
    )

@app.route('/admin/export-emails')
@login_required
def admin_export_emails():
    """Export all parent emails as CSV"""
    # Get current user type from the database directly
    parent = Parent.query.filter_by(id=current_user.id).first()
    
    # Admin is user with ID 1
    if not parent or parent.id != 1:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    # Create CSV in memory
    import csv
    from io import StringIO
    
    output = StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['Email', 'Username', 'First Name', 'Last Name', 'Registration Date'])
    
    # Write data
    for parent in Parent.query.all():
        writer.writerow([
            parent.email,
            parent.username,
            parent.first_name or '',
            parent.last_name or '',
            parent.created_at.strftime('%Y-%m-%d')
        ])
    
    # Prepare response
    response_data = output.getvalue().encode('utf-8')
    output.close()
    
    # Create in-memory file for download
    mem_file = io.BytesIO()
    mem_file.write(response_data)
    mem_file.seek(0)
    
    # Get current date for filename
    today = date.today().strftime('%Y-%m-%d')
    
    return send_file(
        mem_file,
        as_attachment=True,
        download_name=f'childrens_castle_parent_emails_{today}.csv',
        mimetype='text/csv'
    )

@app.route('/admin/edit-user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_user(user_id):
    """Admin page to edit user details"""
    # Verify admin access
    if current_user.id != 1:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    parent = Parent.query.get_or_404(user_id)
    
    if request.method == 'POST':
        # Check for valid CSRF token
        csrf_token = request.form.get('csrf_token')
        if not csrf_token or not csrf.validate_csrf(csrf_token):
            flash('Invalid form submission. Please try again.', 'error')
            return redirect(url_for('admin_edit_user', user_id=user_id))
            
        # Update user details
        parent.username = request.form.get('username')
        parent.email = request.form.get('email')
        parent.first_name = request.form.get('first_name')
        parent.last_name = request.form.get('last_name')
        
        # Only update password if provided
        new_password = request.form.get('new_password')
        if new_password and len(new_password) >= 8:
            parent.set_password(new_password)
        
        try:
            db.session.commit()
            flash('User details updated successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating user: {str(e)}', 'error')
        
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin_edit_user.html', parent=parent)

@app.route('/admin/delete-user/<int:user_id>', methods=['POST'])
@login_required
def admin_delete_user(user_id):
    """Delete a user account"""
    # Verify admin access
    if current_user.id != 1:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    # Check for valid CSRF token
    csrf_token = request.form.get('csrf_token')
    if not csrf_token or not csrf.validate_csrf(csrf_token):
        flash('Invalid form submission. Please try again.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    # Cannot delete admin account
    if user_id == 1:
        flash('Cannot delete the admin account', 'error')
        return redirect(url_for('admin_dashboard'))
    
    parent = Parent.query.get_or_404(user_id)
    
    try:
        db.session.delete(parent)
        db.session.commit()
        flash(f'User {parent.username} and all associated data deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting user: {str(e)}', 'error')
    
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/reset-password/<int:user_id>', methods=['POST'])
@login_required
def admin_reset_password(user_id):
    """Reset a user's password and send email"""
    # Verify admin access
    if current_user.id != 1:
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('index'))
    
    # Check for valid CSRF token
    csrf_token = request.form.get('csrf_token')
    if not csrf_token or not csrf.validate_csrf(csrf_token):
        flash('Invalid form submission. Please try again.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    parent = Parent.query.get_or_404(user_id)
    
    # Generate a token
    token = parent.get_reset_token()
    db.session.commit()
    
    # Create reset URL with the server's hostname
    # Get the host from request or environment
    host = request.host_url.rstrip('/')
    if not host:
        host = os.environ.get('REPLIT_DEV_DOMAIN') or os.environ.get('REPLIT_DOMAIN')
        if host:
            host = f"https://{host}"
    
    # Create the reset URL
    reset_path = url_for('reset_password', token=token)
    reset_url = f"{host}{reset_path}"
    
    # Send email
    from email_service import send_password_reset_email
    if send_password_reset_email(parent, token, reset_url):
        flash(f'Password reset email sent to {parent.email}', 'success')
    else:
        flash('Error sending password reset email', 'error')
    
    return redirect(url_for('admin_dashboard'))

