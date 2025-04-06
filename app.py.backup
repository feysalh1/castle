import os
import logging
from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.middleware.proxy_fix import ProxyFix

from models import db, Parent, Child, ParentSettings, Progress, Reward, Session

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "childrens_castle_app_secret")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # needed for url_for to generate with https

# Configure database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db.init_app(app)

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


# Create database tables
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    """Render the homepage of the Children's Castle app."""
    if current_user.is_authenticated:
        if session.get('user_type') == 'parent':
            return redirect(url_for('parent_dashboard'))
        elif session.get('user_type') == 'child':
            return redirect(url_for('child_dashboard'))
    return render_template('login_landing.html')


@app.route('/parent/register', methods=['GET', 'POST'])
def parent_register():
    """Register a new parent account"""
    if current_user.is_authenticated:
        return redirect(url_for('parent_dashboard'))
    
    if request.method == 'POST':
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
        settings = ParentSettings(parent=parent)
        
        # Save to database
        db.session.add(parent)
        db.session.add(settings)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('parent_login'))
    
    return render_template('parent_register.html')


@app.route('/parent/login', methods=['GET', 'POST'])
def parent_login():
    """Login for parent accounts"""
    if current_user.is_authenticated:
        return redirect(url_for('parent_dashboard'))
    
    if request.method == 'POST':
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
        
        # Record login session
        new_session = Session(user_type='parent', user_id=parent.id)
        db.session.add(new_session)
        db.session.commit()
        
        # Redirect to next page or dashboard
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect(url_for('parent_dashboard'))
    
    return render_template('parent_login.html')


# Child login is no longer needed as children access through parent accounts


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
            user_session.end_time = datetime.utcnow()
            user_session.duration = (user_session.end_time - user_session.start_time).total_seconds()
            db.session.commit()
    
    logout_user()
    session.pop('user_type', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))


@app.route('/parent/dashboard')
@login_required
def parent_dashboard():
    """Parent dashboard"""
    if session.get('user_type') != 'parent':
        flash('Access denied. This page is for parents only.', 'error')
        return redirect(url_for('index'))
    
    # Get all children for this parent
    children = Child.query.filter_by(parent_id=current_user.id).all()
    
    return render_template('parent_dashboard.html', children=children)


@app.route('/parent/add-child', methods=['GET', 'POST'])
@login_required
def add_child():
    """Add a new child account"""
    if session.get('user_type') != 'parent':
        flash('Access denied. This page is for parents only.', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
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
    
    return render_template('add_child.html')


@app.route('/access-child/<int:child_id>')
@login_required
def access_child_view(child_id):
    """Allow parent to access child's view"""
    if session.get('user_type') != 'parent':
        flash('Access denied. Only parents can access this feature.', 'error')
        return redirect(url_for('index'))
    
    # Check if the child belongs to the current parent
    child = Child.query.filter_by(id=child_id, parent_id=current_user.id).first()
    
    if not child:
        flash('Child not found or does not belong to you.', 'error')
        return redirect(url_for('parent_dashboard'))
    
    # Store the child ID in the session for child view access
    session['active_child_id'] = child.id
    session['active_child_name'] = child.display_name
    
    # Redirect to child dashboard
    return redirect(url_for('child_dashboard'))


@app.route('/child/dashboard')
@login_required
def child_dashboard():
    """Child dashboard"""
    if session.get('user_type') != 'parent' or not session.get('active_child_id'):
        flash('Access denied. Please log in as a parent and select a child profile.', 'error')
        return redirect(url_for('index'))
    
    # Get child's information
    child_id = session.get('active_child_id')
    child = Child.query.get(child_id)
    
    if not child or child.parent_id != current_user.id:
        flash('Child not found or does not belong to you.', 'error')
        return redirect(url_for('parent_dashboard'))
    
    # Get child's progress and rewards
    progress = Progress.query.filter_by(child_id=child_id).all()
    rewards = Reward.query.filter_by(child_id=child_id).all()
    
    return render_template('child_dashboard.html', child=child, progress=progress, rewards=rewards)


@app.route('/parent/settings', methods=['GET', 'POST'])
@login_required
def parent_settings():
    """Parent settings page"""
    if session.get('user_type') != 'parent':
        flash('Access denied. This page is for parents only.', 'error')
        return redirect(url_for('index'))
    
    settings = ParentSettings.query.filter_by(parent_id=current_user.id).first()
    
    if request.method == 'POST':
        settings.allow_external_games = request.form.get('allow_external_games') == 'on'
        settings.max_daily_playtime = int(request.form.get('max_daily_playtime'))
        settings.content_age_filter = int(request.form.get('content_age_filter'))
        settings.notifications_enabled = request.form.get('notifications_enabled') == 'on'
        
        db.session.commit()
        flash('Settings updated successfully', 'success')
        return redirect(url_for('parent_settings'))
    
    return render_template('parent_settings.html', settings=settings)


@app.route('/story-mode')
@login_required
def story_mode():
    """Story mode page for children"""
    if session.get('user_type') != 'parent' or not session.get('active_child_id'):
        flash('Access denied. Please log in as a parent and select a child profile.', 'error')
        return redirect(url_for('index'))
    
    # Get child's information
    child_id = session.get('active_child_id')
    child = Child.query.get(child_id)
    
    if not child or child.parent_id != current_user.id:
        flash('Child not found or does not belong to you.', 'error')
        return redirect(url_for('parent_dashboard'))
    
    # Fetch stories that are appropriate for this child's age
    # In a full implementation, this would filter stories by age appropriateness
    
    return render_template('story_mode.html', child=child)


@app.route('/game-mode')
@login_required
def game_mode():
    """Game mode page for children"""
    if session.get('user_type') != 'parent' or not session.get('active_child_id'):
        flash('Access denied. Please log in as a parent and select a child profile.', 'error')
        return redirect(url_for('index'))
    
    # Get child's information
    child_id = session.get('active_child_id')
    child = Child.query.get(child_id)
    
    if not child or child.parent_id != current_user.id:
        flash('Child not found or does not belong to you.', 'error')
        return redirect(url_for('parent_dashboard'))
    
    # Get parent settings to apply age filters
    settings = ParentSettings.query.filter_by(parent_id=current_user.id).first()
    
    return render_template('game_mode.html', child=child, settings=settings)


@app.route('/rewards')
@login_required
def rewards():
    """Child's rewards page"""
    if session.get('user_type') != 'parent' or not session.get('active_child_id'):
        flash('Access denied. Please log in as a parent and select a child profile.', 'error')
        return redirect(url_for('index'))
    
    # Get child's information
    child_id = session.get('active_child_id')
    child = Child.query.get(child_id)
    
    if not child or child.parent_id != current_user.id:
        flash('Child not found or does not belong to you.', 'error')
        return redirect(url_for('parent_dashboard'))
    
    # Get child's rewards from database
    child_rewards = Reward.query.filter_by(child_id=child_id).all()
    
    return render_template('rewards.html', child=child, rewards=child_rewards)


@app.route('/api/track-progress', methods=['POST'])
@login_required
def track_progress():
    """API endpoint to track child's progress"""
    if session.get('user_type') != 'parent' or not session.get('active_child_id'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    # Get child's information
    child_id = session.get('active_child_id')
    child = Child.query.get(child_id)
    
    if not child or child.parent_id != current_user.id:
        return jsonify({'success': False, 'message': 'Child not found or unauthorized'}), 403
    
    data = request.json
    content_type = data.get('content_type')  # 'story' or 'game'
    content_id = data.get('content_id')
    completed = data.get('completed', False)
    time_spent = data.get('time_spent', 0)  # in seconds
    
    # Find existing progress or create new
    progress = Progress.query.filter_by(
        child_id=child_id,
        content_type=content_type,
        content_id=content_id
    ).first()
    
    if progress:
        progress.last_accessed = datetime.utcnow()
        progress.time_spent += time_spent
        
        if completed and not progress.completed:
            progress.completed = True
            progress.completion_count += 1
            
            # Add a reward if this is the first completion
            if progress.completion_count == 1:
                if content_type == 'story':
                    reward = Reward(
                        child_id=child_id,
                        badge_id=f"story_{content_id}",
                        badge_name=f"Story Master: {content_id.title()}",
                        badge_description=f"Completed the {content_id.title()} story",
                        badge_image=f"badges/story_{content_id}.png"
                    )
                else:  # game
                    reward = Reward(
                        child_id=child_id,
                        badge_id=f"game_{content_id}",
                        badge_name=f"Game Master: {content_id.title()}",
                        badge_description=f"Completed the {content_id.title()} game",
                        badge_image=f"badges/game_{content_id}.png"
                    )
                
                db.session.add(reward)
    else:
        progress = Progress(
            child_id=child_id,
            content_type=content_type,
            content_id=content_id,
            completed=completed,
            completion_count=1 if completed else 0,
            time_spent=time_spent
        )
        db.session.add(progress)
    
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'progress': {
            'content_id': progress.content_id,
            'completed': progress.completed,
            'completion_count': progress.completion_count,
            'time_spent': progress.time_spent
        }
    })


@app.route('/api/get-progress')
@login_required
def get_progress():
    """API endpoint to get child's progress"""
    if session.get('user_type') != 'parent' or not session.get('active_child_id'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    # Get child's information
    child_id = session.get('active_child_id')
    child = Child.query.get(child_id)
    
    if not child or child.parent_id != current_user.id:
        return jsonify({'success': False, 'message': 'Child not found or unauthorized'}), 403
    
    content_type = request.args.get('content_type')
    
    if content_type:
        progress_items = Progress.query.filter_by(
            child_id=child_id,
            content_type=content_type
        ).all()
    else:
        progress_items = Progress.query.filter_by(
            child_id=child_id
        ).all()
    
    progress_data = [{
        'content_type': item.content_type,
        'content_id': item.content_id,
        'completed': item.completed,
        'completion_count': item.completion_count,
        'last_accessed': item.last_accessed.isoformat(),
        'time_spent': item.time_spent
    } for item in progress_items]
    
    return jsonify({
        'success': True,
        'progress': progress_data
    })


@app.route('/api/get-rewards')
@login_required
def get_rewards():
    """API endpoint to get child's rewards"""
    if session.get('user_type') != 'parent' or not session.get('active_child_id'):
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    # Get child's information
    child_id = session.get('active_child_id')
    child = Child.query.get(child_id)
    
    if not child or child.parent_id != current_user.id:
        return jsonify({'success': False, 'message': 'Child not found or unauthorized'}), 403
    
    rewards = Reward.query.filter_by(child_id=child_id).all()
    
    rewards_data = [{
        'badge_id': reward.badge_id,
        'badge_name': reward.badge_name,
        'badge_description': reward.badge_description,
        'badge_image': reward.badge_image,
        'earned_at': reward.earned_at.isoformat()
    } for reward in rewards]
    
    return jsonify({
        'success': True,
        'rewards': rewards_data,
        'total_rewards': len(rewards_data)
    })


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
