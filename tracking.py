"""
Tracking and analytics helper functions for Children's Castle application.
"""

from datetime import datetime, timedelta
from flask_login import current_user
from app import db
from models import Progress, Milestone, Event, ErrorLog, Reward, Session, Child

def track_milestone_progress(child_id, milestone_id, value=1, check_only=False):
    """
    Track progress towards a milestone and award if completed.
    Returns True if the milestone was just completed, False otherwise.
    If check_only is True, just check if the milestone is already completed.
    """
    milestone = Milestone.query.filter_by(
        child_id=child_id,
        milestone_id=milestone_id
    ).first()

    if not milestone:
        return False

    if check_only:
        return milestone.completed

    # Update progress and check if completed
    completed = milestone.update_progress(value)
    db.session.commit()

    if completed:
        # Award a reward for achieving the milestone
        reward = Reward(
            child_id=child_id,
            badge_id=f"milestone_{milestone_id}",
            badge_name=f"Achievement: {milestone.milestone_name}",
            badge_description=milestone.milestone_description or f"Completed {milestone.milestone_name}",
            badge_image=f"badges/milestone_{milestone_id}.png",
            source_type='milestone',
            source_id=milestone_id,
            achievement_level='gold',  # Milestones are higher value
            points_value=5  # Higher points for milestones
        )
        db.session.add(reward)
        db.session.commit()

    return completed

def check_and_create_milestones(child_id):
    """
    Check for milestone conditions and create new ones if needed.
    This should be called periodically, like on login or at the end of a session.
    """
    # Get child data
    child = Child.query.get(child_id)
    if not child:
        return []

    # Get existing milestones to avoid duplicates
    existing_milestones = Milestone.query.filter_by(child_id=child_id).all()
    existing_ids = [m.milestone_id for m in existing_milestones]

    # Get progress data
    all_progress = Progress.query.filter_by(child_id=child_id).all()
    story_progress = [p for p in all_progress if p.content_type == 'story']
    game_progress = [p for p in all_progress if p.content_type == 'game']

    # Calculate some stats
    stories_read = sum(1 for p in story_progress if p.completed)
    games_played = sum(1 for p in game_progress if p.completed)
    total_time = sum(p.time_spent for p in all_progress) / 60  # minutes

    # Define potential milestones
    milestone_definitions = [
        # Story milestones
        {
            'id': 'read_first_story',
            'type': 'completion', 
            'name': 'First Story',
            'description': 'Read your first story',
            'condition': stories_read >= 1,
            'target': 1
        },
        {
            'id': 'read_5_stories',
            'type': 'completion', 
            'name': 'Story Explorer',
            'description': 'Read 5 different stories',
            'condition': stories_read >= 5,
            'target': 5
        },
        {
            'id': 'read_all_stories',
            'type': 'completion', 
            'name': 'Story Master',
            'description': 'Read all available stories',
            'condition': stories_read >= 12,  # Assuming 12 stories
            'target': 12
        },

        # Game milestones
        {
            'id': 'play_first_game',
            'type': 'completion', 
            'name': 'First Game',
            'description': 'Complete your first game',
            'condition': games_played >= 1,
            'target': 1
        },
        {
            'id': 'play_5_games',
            'type': 'completion', 
            'name': 'Game Explorer',
            'description': 'Play 5 different games',
            'condition': games_played >= 5,
            'target': 5
        },

        # Time spent milestones
        {
            'id': 'time_spent_60',
            'type': 'engagement', 
            'name': 'One Hour Wonder',
            'description': 'Spend at least 60 minutes learning and having fun',
            'condition': total_time >= 60,
            'target': 60
        },

        # Streak milestones - these will be created with progress=0 initially
        {
            'id': 'daily_login_3',
            'type': 'streak', 
            'name': '3-Day Streak',
            'description': 'Log in for 3 days in a row',
            'condition': False,  # Will be tracked separately
            'target': 3
        },
        {
            'id': 'daily_login_7',
            'type': 'streak', 
            'name': 'Weekly Streak',
            'description': 'Log in for 7 days in a row',
            'condition': False,  # Will be tracked separately
            'target': 7
        }
    ]

    # Create any missing milestones
    created_milestones = []
    for milestone_def in milestone_definitions:
        if milestone_def['id'] not in existing_ids:
            # Create the milestone
            milestone = Milestone(
                child_id=child_id,
                milestone_type=milestone_def['type'],
                milestone_id=milestone_def['id'],
                milestone_name=milestone_def['name'],
                milestone_description=milestone_def['description'],
                target_value=milestone_def['target']
            )

            # For completion-based milestones, set progress based on condition
            if milestone_def['type'] == 'completion' and milestone_def['condition']:
                milestone.progress = milestone_def['target']
                milestone.completed = True
                milestone.earned_at = datetime.utcnow()

            db.session.add(milestone)
            created_milestones.append(milestone)

    if created_milestones:
        db.session.commit()

    return created_milestones

def update_streak_milestones(child_id, current_streak):
    """Update streak-based milestones with the current streak count"""
    # Check 3-day streak
    track_milestone_progress(
        child_id, 
        'daily_login_3', 
        value=current_streak if current_streak <= 3 else 3
    )

    # Check 7-day streak
    track_milestone_progress(
        child_id, 
        'daily_login_7',
        value=current_streak if current_streak <= 7 else 7
    )

def track_custom_event(event_type, event_name, event_data=None):
    """Track a custom event for the current user"""
    if not current_user or not current_user.is_authenticated:
        return None

    # Determine user type (parent or child)
    user_id = current_user.id
    if hasattr(current_user, 'get_id') and current_user.get_id().startswith('parent-'):
        user_type = 'parent'
    else:
        user_type = 'child'

    # Find the current session
    session = Session.query.filter_by(
        user_type=user_type,
        user_id=user_id,
        end_time=None
    ).order_by(Session.start_time.desc()).first()

    # Create the event
    return Event.track_event(
        user_type=user_type,
        user_id=user_id,
        event_type=event_type,
        event_name=event_name,
        event_data=event_data,
        session_id=session.id if session else None
    )

def log_error(error_type, error_message, error_context=None, stack_trace=None):
    """Log an error for the current user or system"""
    user_type = None
    user_id = None
    session_id = None

    # Get user info if authenticated
    if current_user and current_user.is_authenticated:
        if hasattr(current_user, 'get_id') and current_user.get_id().startswith('parent-'):
            user_type = 'parent'
        else:
            user_type = 'child'
        user_id = current_user.id

        # Find current session
        session = Session.query.filter_by(
            user_type=user_type,
            user_id=user_id,
            end_time=None
        ).order_by(Session.start_time.desc()).first()

        if session:
            session_id = session.id

    # Log the error
    return ErrorLog.log_error(
        error_type=error_type,
        error_message=error_message,
        user_type=user_type,
        user_id=user_id,
        error_context=error_context,
        stack_trace=stack_trace,
        session_id=session_id
    )

def get_favorites(child_id, content_type=None, limit=5):
    """Get a child's favorite content based on engagement metrics"""
    # Start with explicit favorites
    query = Progress.query.filter_by(
        child_id=child_id,
        is_favorite=True
    )

    if content_type:
        query = query.filter_by(content_type=content_type)

    favorites = query.all()

    # If not enough explicit favorites, add most engaged with content
    if len(favorites) < limit:
        # Create a query for non-favorites ordered by engagement
        query = Progress.query.filter_by(
            child_id=child_id,
            is_favorite=False
        )

        if content_type:
            query = query.filter_by(content_type=content_type)

        # Order by a combination of metrics to determine "implicit favorites"
        # We prioritize completion count, time spent and access count
        additional = query.order_by(
            Progress.completion_count.desc(),
            Progress.time_spent.desc(), 
            Progress.access_count.desc()
        ).limit(limit - len(favorites)).all()

        favorites.extend(additional)

    return favorites

def track_story_progress(child_id, story_id, story_title, completed=False):
    try:
        # Check if child exists
        child = Child.query.get(child_id)
        if not child:
            return {"message": f"Child with ID {child_id} not found"}, 404

        # Create new progress entry
        new_progress = Progress(
            child_id=child_id,
            content_id=story_id,
            content_type='story',
            content_title=story_title,
            completed=completed,
            access_count=1,
            time_spent=0  # Updated later
        )
        db.session.add(new_progress)
        db.session.commit()
        return new_progress

    except Exception as e:
        return {"message": f"Error tracking story progress: {e}"}, 500