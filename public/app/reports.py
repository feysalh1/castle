"""
Reports module for Children's Castle.
Handles generation and display of daily and weekly reports for children's activities.
"""

import json
from datetime import datetime, timedelta, date
from sqlalchemy import func, desc, or_, and_
from flask import jsonify

from app import db
from models import Child, Session, Event, Progress, DailyReport, WeeklyReport


def generate_daily_report(child_id, report_date=None):
    """
    Generate a daily report for a child's activity
    
    Args:
        child_id (int): The ID of the child
        report_date (date, optional): The date for the report. Defaults to today.
    
    Returns:
        DailyReport: The generated or updated report object
    """
    # Set default date to today if not specified
    if report_date is None:
        report_date = date.today()
    
    # Check if a report already exists for this date
    existing_report = DailyReport.query.filter_by(
        child_id=child_id, 
        report_date=report_date
    ).first()
    
    if existing_report:
        # Update existing report
        report = existing_report
    else:
        # Create new report
        report = DailyReport(
            child_id=child_id,
            report_date=report_date
        )
    
    # Get start and end of the day
    day_start = datetime.combine(report_date, datetime.min.time())
    day_end = datetime.combine(report_date, datetime.max.time())
    
    # Calculate metrics from data
    
    # 1. Time spent in app
    sessions = Session.query.filter(
        Session.user_id == child_id,
        Session.user_type == 'child',
        Session.start_time.between(day_start, day_end)
    ).all()
    
    total_minutes = 0
    for session in sessions:
        # Calculate session duration
        if session.end_time:
            session_duration = (session.end_time - session.start_time).total_seconds() / 60
        else:
            # For open sessions, calculate duration up to now
            current_time = datetime.now()
            session_duration = (current_time - session.start_time).total_seconds() / 60
        
        total_minutes += session_duration
    
    # 2. Stories read
    story_events = Event.query.filter(
        Event.user_id == child_id,
        Event.user_type == 'child',
        Event.timestamp.between(day_start, day_end),
        Event.event_type == 'story',
        Event.event_name.in_(['story_complete', 'story_page_complete'])
    ).all()
    
    # Count unique stories by tracking unique content IDs
    unique_stories = set()
    for event in story_events:
        try:
            if event.event_data:
                data = json.loads(event.event_data) if isinstance(event.event_data, str) else event.event_data
                if 'content_id' in data:
                    unique_stories.add(data['content_id'])
        except (json.JSONDecodeError, TypeError):
            continue
    
    # 3. Games played
    game_events = Event.query.filter(
        Event.user_id == child_id,
        Event.user_type == 'child',
        Event.timestamp.between(day_start, day_end),
        Event.event_type == 'game',
        Event.event_name.in_(['game_complete', 'game_start'])
    ).all()
    
    # Count unique games
    unique_games = set()
    for event in game_events:
        try:
            if event.event_data:
                data = json.loads(event.event_data) if isinstance(event.event_data, str) else event.event_data
                if 'content_id' in data:
                    unique_games.add(data['content_id'])
        except (json.JSONDecodeError, TypeError):
            continue
    
    # 4. Stars earned (from progress data)
    progress_records = Progress.query.filter(
        Progress.child_id == child_id,
        Progress.last_accessed.between(day_start, day_end)
    ).all()
    
    stars_earned = 0
    for progress in progress_records:
        stars_earned += progress.stars or 0
    
    # 5. Emotional feedback
    emotion_events = Event.query.filter(
        Event.user_id == child_id,
        Event.user_type == 'child',
        Event.timestamp.between(day_start, day_end),
        Event.event_type == 'emotional_feedback'
    ).all()
    
    emotion_data = {}
    for event in emotion_events:
        try:
            if event.event_data:
                data = json.loads(event.event_data) if isinstance(event.event_data, str) else event.event_data
                if 'emoji' in data:
                    emoji = data['emoji']
                    if emoji in emotion_data:
                        emotion_data[emoji] += 1
                    else:
                        emotion_data[emoji] = 1
        except (json.JSONDecodeError, TypeError):
            continue
    
    # 6. Learning goals progress
    # Include any metrics on learning goals
    
    # 7. Record all metrics in the report
    report.stories_read = len(unique_stories)
    report.games_played = len(unique_games)
    report.time_spent = round(total_minutes)
    report.stars_earned = stars_earned
    
    # Store emotion data
    report.emotional_feedback = json.dumps(emotion_data)
    
    # Serialized activity breakdown
    activity_breakdown = {
        'stories': list(unique_stories),
        'games': list(unique_games),
        'sessions': [
            {
                'start': session.start_time.isoformat(),
                'end': session.end_time.isoformat() if session.end_time else None,
                'duration_minutes': round((session.end_time - session.start_time).total_seconds() / 60) if session.end_time else None,
                'device': session.device_type
            } 
            for session in sessions
        ]
    }
    report.activity_breakdown = json.dumps(activity_breakdown)
    
    # Save report to database
    if not existing_report:
        db.session.add(report)
    db.session.commit()
    
    return report


def generate_weekly_report(child_id, week_start=None):
    """
    Generate a weekly report for a child's activity
    
    Args:
        child_id (int): The ID of the child
        week_start (date, optional): The start date of the week (Monday). 
                                     Defaults to start of current week.
    
    Returns:
        WeeklyReport: The generated report object
    """
    # Set default week start to Monday of current week
    if week_start is None:
        today = date.today()
        week_start = today - timedelta(days=today.weekday())
    
    # Calculate week end (Sunday)
    week_end = week_start + timedelta(days=6)
    
    # Check if a report already exists for this week
    existing_report = WeeklyReport.query.filter_by(
        child_id=child_id, 
        week_start=week_start
    ).first()
    
    if existing_report:
        # Update existing report
        report = existing_report
    else:
        # Create new report
        report = WeeklyReport(
            child_id=child_id,
            week_start=week_start,
            week_end=week_end
        )
    
    # Aggregate daily reports for the week
    daily_reports = DailyReport.query.filter(
        DailyReport.child_id == child_id,
        DailyReport.report_date.between(week_start, week_end)
    ).all()
    
    # If no daily reports available, generate them for each day
    if not daily_reports:
        for i in range(7):
            day_date = week_start + timedelta(days=i)
            if day_date <= date.today():  # Only generate for days up to today
                generate_daily_report(child_id, day_date)
        
        # Retrieve newly generated reports
        daily_reports = DailyReport.query.filter(
            DailyReport.child_id == child_id,
            DailyReport.report_date.between(week_start, week_end)
        ).all()
    
    # If still no daily reports, return None (no activity for the week)
    if not daily_reports:
        return None
    
    # Aggregate metrics from daily reports
    stories_read = sum(report.stories_read for report in daily_reports)
    games_played = sum(report.games_played for report in daily_reports)
    time_spent = sum(report.time_spent for report in daily_reports)
    stars_earned = sum(report.stars_earned for report in daily_reports)
    
    # Aggregate emotional feedback
    all_emotions = {}
    for daily_report in daily_reports:
        if daily_report.emotional_feedback:
            try:
                emotions = json.loads(daily_report.emotional_feedback)
                for emoji, count in emotions.items():
                    if emoji in all_emotions:
                        all_emotions[emoji] += count
                    else:
                        all_emotions[emoji] = count
            except (json.JSONDecodeError, TypeError):
                continue
    
    # Build day-by-day breakdown
    daily_breakdown = []
    for day_offset in range(7):
        day_date = week_start + timedelta(days=day_offset)
        day_report = next((r for r in daily_reports if r.report_date == day_date), None)
        
        if day_report:
            daily_breakdown.append({
                'date': day_report.report_date.isoformat(),
                'stories_read': day_report.stories_read,
                'games_played': day_report.games_played,
                'time_spent': day_report.time_spent,
                'stars_earned': day_report.stars_earned
            })
        else:
            daily_breakdown.append({
                'date': day_date.isoformat(),
                'stories_read': 0,
                'games_played': 0,
                'time_spent': 0,
                'stars_earned': 0
            })
    
    # Update report metrics
    report.stories_read = stories_read
    report.games_played = games_played
    report.time_spent = time_spent
    report.stars_earned = stars_earned
    report.emotional_feedback = json.dumps(all_emotions)
    report.daily_breakdown = json.dumps(daily_breakdown)
    
    # Calculate streaks (consecutive days with activity)
    active_days = [r.report_date for r in daily_reports if r.time_spent > 0]
    active_days.sort()
    
    current_streak = 0
    longest_streak = 0
    last_date = None
    
    for idx, active_date in enumerate(active_days):
        if idx == 0:
            current_streak = 1
            longest_streak = 1
            last_date = active_date
        else:
            if (active_date - last_date).days == 1:
                current_streak += 1
                longest_streak = max(longest_streak, current_streak)
            else:
                current_streak = 1
            last_date = active_date
    
    # Check if current streak is ongoing until today
    if active_days and (date.today() - active_days[-1]).days <= 1:
        report.current_streak = current_streak
    else:
        report.current_streak = 0
    
    report.longest_streak = longest_streak
    
    # Save report to database
    if not existing_report:
        db.session.add(report)
    db.session.commit()
    
    return report


def get_report_data_for_period(child_id, period_type='week', start_date=None, end_date=None):
    """
    Get report data for a specific period
    
    Args:
        child_id (int): The ID of the child
        period_type (str): The period type ('day', 'week', 'month', 'custom')
        start_date (date, optional): Start date for custom period
        end_date (date, optional): End date for custom period
    
    Returns:
        dict: Report data
    """
    # Handle different period types
    today = date.today()
    
    if period_type == 'day':
        # Use provided date or default to today
        report_date = start_date or today
        daily_report = generate_daily_report(child_id, report_date)
        
        if not daily_report:
            return {
                'period_type': 'day',
                'start_date': report_date.isoformat(),
                'end_date': report_date.isoformat(),
                'stories_read': 0,
                'games_played': 0,
                'time_spent': 0,
                'stars_earned': 0,
                'emotional_feedback': {},
                'activity_breakdown': {'stories': [], 'games': [], 'sessions': []}
            }
        
        # Convert JSON strings to Python objects
        emotional_feedback = json.loads(daily_report.emotional_feedback) if daily_report.emotional_feedback else {}
        activity_breakdown = json.loads(daily_report.activity_breakdown) if daily_report.activity_breakdown else {}
        
        return {
            'period_type': 'day',
            'start_date': daily_report.report_date.isoformat(),
            'end_date': daily_report.report_date.isoformat(),
            'stories_read': daily_report.stories_read,
            'games_played': daily_report.games_played,
            'time_spent': daily_report.time_spent,
            'stars_earned': daily_report.stars_earned,
            'emotional_feedback': emotional_feedback,
            'activity_breakdown': activity_breakdown
        }
    
    elif period_type == 'week':
        # Calculate week start (Monday) if not provided
        if not start_date:
            start_date = today - timedelta(days=today.weekday())
        
        # Calculate week end (Sunday)
        end_date = start_date + timedelta(days=6)
        
        weekly_report = generate_weekly_report(child_id, start_date)
        
        if not weekly_report:
            return {
                'period_type': 'week',
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'stories_read': 0,
                'games_played': 0,
                'time_spent': 0,
                'stars_earned': 0,
                'current_streak': 0,
                'longest_streak': 0,
                'emotional_feedback': {},
                'daily_breakdown': [
                    {
                        'date': (start_date + timedelta(days=i)).isoformat(),
                        'stories_read': 0,
                        'games_played': 0,
                        'time_spent': 0,
                        'stars_earned': 0
                    }
                    for i in range(7)
                ]
            }
        
        # Convert JSON strings to Python objects
        emotional_feedback = json.loads(weekly_report.emotional_feedback) if weekly_report.emotional_feedback else {}
        daily_breakdown = json.loads(weekly_report.daily_breakdown) if weekly_report.daily_breakdown else []
        
        return {
            'period_type': 'week',
            'start_date': weekly_report.week_start.isoformat(),
            'end_date': weekly_report.week_end.isoformat(),
            'stories_read': weekly_report.stories_read,
            'games_played': weekly_report.games_played,
            'time_spent': weekly_report.time_spent,
            'stars_earned': weekly_report.stars_earned,
            'current_streak': weekly_report.current_streak,
            'longest_streak': weekly_report.longest_streak,
            'emotional_feedback': emotional_feedback,
            'daily_breakdown': daily_breakdown
        }
    
    elif period_type == 'month':
        # Calculate month start
        if not start_date:
            start_date = date(today.year, today.month, 1)
        
        # Calculate month end
        if today.month == 12:
            next_month = date(today.year + 1, 1, 1)
        else:
            next_month = date(today.year, today.month + 1, 1)
        
        end_date = next_month - timedelta(days=1)
        
        # Get all daily reports for the month
        daily_reports = DailyReport.query.filter(
            DailyReport.child_id == child_id,
            DailyReport.report_date.between(start_date, end_date)
        ).order_by(DailyReport.report_date).all()
        
        # Generate missing daily reports
        current_date = start_date
        while current_date <= min(today, end_date):
            if not any(r.report_date == current_date for r in daily_reports):
                report = generate_daily_report(child_id, current_date)
                if report:
                    daily_reports.append(report)
            current_date += timedelta(days=1)
        
        # Sort daily reports by date
        daily_reports.sort(key=lambda x: x.report_date)
        
        # Aggregate monthly metrics
        stories_read = sum(report.stories_read for report in daily_reports)
        games_played = sum(report.games_played for report in daily_reports)
        time_spent = sum(report.time_spent for report in daily_reports)
        stars_earned = sum(report.stars_earned for report in daily_reports)
        
        # Aggregate emotional feedback
        all_emotions = {}
        for daily_report in daily_reports:
            if daily_report.emotional_feedback:
                try:
                    emotions = json.loads(daily_report.emotional_feedback)
                    for emoji, count in emotions.items():
                        if emoji in all_emotions:
                            all_emotions[emoji] += count
                        else:
                            all_emotions[emoji] = count
                except (json.JSONDecodeError, TypeError):
                    continue
        
        # Build day-by-day breakdown
        daily_breakdown = []
        for report in daily_reports:
            daily_breakdown.append({
                'date': report.report_date.isoformat(),
                'stories_read': report.stories_read,
                'games_played': report.games_played,
                'time_spent': report.time_spent,
                'stars_earned': report.stars_earned
            })
        
        # Calculate streaks
        active_days = [r.report_date for r in daily_reports if r.time_spent > 0]
        active_days.sort()
        
        current_streak = 0
        longest_streak = 0
        last_date = None
        
        for idx, active_date in enumerate(active_days):
            if idx == 0:
                current_streak = 1
                longest_streak = 1
                last_date = active_date
            else:
                if (active_date - last_date).days == 1:
                    current_streak += 1
                    longest_streak = max(longest_streak, current_streak)
                else:
                    current_streak = 1
                last_date = active_date
        
        # Check if current streak is ongoing until today
        if active_days and (today - active_days[-1]).days <= 1:
            current_streak_value = current_streak
        else:
            current_streak_value = 0
        
        return {
            'period_type': 'month',
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'stories_read': stories_read,
            'games_played': games_played,
            'time_spent': time_spent,
            'stars_earned': stars_earned,
            'current_streak': current_streak_value,
            'longest_streak': longest_streak,
            'emotional_feedback': all_emotions,
            'daily_breakdown': daily_breakdown
        }
    
    elif period_type == 'custom':
        # Requires both start and end dates
        if not start_date or not end_date:
            return {
                'error': 'Custom period requires both start and end dates'
            }
        
        # Ensure start date is before end date
        if start_date > end_date:
            start_date, end_date = end_date, start_date
        
        # Get all daily reports for the custom period
        daily_reports = DailyReport.query.filter(
            DailyReport.child_id == child_id,
            DailyReport.report_date.between(start_date, end_date)
        ).order_by(DailyReport.report_date).all()
        
        # Generate missing daily reports
        current_date = start_date
        while current_date <= min(today, end_date):
            if not any(r.report_date == current_date for r in daily_reports):
                report = generate_daily_report(child_id, current_date)
                if report:
                    daily_reports.append(report)
            current_date += timedelta(days=1)
        
        # Sort daily reports by date
        daily_reports.sort(key=lambda x: x.report_date)
        
        # Aggregate metrics
        stories_read = sum(report.stories_read for report in daily_reports)
        games_played = sum(report.games_played for report in daily_reports)
        time_spent = sum(report.time_spent for report in daily_reports)
        stars_earned = sum(report.stars_earned for report in daily_reports)
        
        # Aggregate emotional feedback
        all_emotions = {}
        for daily_report in daily_reports:
            if daily_report.emotional_feedback:
                try:
                    emotions = json.loads(daily_report.emotional_feedback)
                    for emoji, count in emotions.items():
                        if emoji in all_emotions:
                            all_emotions[emoji] += count
                        else:
                            all_emotions[emoji] = count
                except (json.JSONDecodeError, TypeError):
                    continue
        
        # Build day-by-day breakdown
        daily_breakdown = []
        for report in daily_reports:
            daily_breakdown.append({
                'date': report.report_date.isoformat(),
                'stories_read': report.stories_read,
                'games_played': report.games_played,
                'time_spent': report.time_spent,
                'stars_earned': report.stars_earned
            })
        
        return {
            'period_type': 'custom',
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'stories_read': stories_read,
            'games_played': games_played,
            'time_spent': time_spent,
            'stars_earned': stars_earned,
            'emotional_feedback': all_emotions,
            'daily_breakdown': daily_breakdown
        }
    
    else:
        return {
            'error': f'Invalid period type: {period_type}'
        }


def generate_chart_data(report_data):
    """
    Generate chart-friendly data from report data
    
    Args:
        report_data (dict): Report data from get_report_data_for_period
    
    Returns:
        dict: Chart data formatted for easy rendering
    """
    period_type = report_data.get('period_type')
    
    if period_type == 'day':
        # For a single day, we might want to show hourly breakdowns
        # This would require more detailed session data
        return {
            'labels': ['Today'],
            'stories': [report_data.get('stories_read', 0)],
            'games': [report_data.get('games_played', 0)],
            'time': [report_data.get('time_spent', 0)],
            'stars': [report_data.get('stars_earned', 0)]
        }
    
    elif period_type in ['week', 'month', 'custom']:
        # For longer periods, use daily breakdown
        daily_breakdown = report_data.get('daily_breakdown', [])
        
        if not daily_breakdown:
            return {
                'labels': [],
                'stories': [],
                'games': [],
                'time': [],
                'stars': []
            }
        
        # Extract data for charts
        labels = []
        stories = []
        games = []
        time_spent = []
        stars = []
        
        for day_data in daily_breakdown:
            # Format date for display
            day_date = datetime.fromisoformat(day_data['date']).date()
            
            if period_type == 'week':
                # For week, show day names
                label = day_date.strftime('%a')
            else:
                # For month/custom, show dates
                label = day_date.strftime('%d')
            
            labels.append(label)
            stories.append(day_data.get('stories_read', 0))
            games.append(day_data.get('games_played', 0))
            time_spent.append(day_data.get('time_spent', 0))
            stars.append(day_data.get('stars_earned', 0))
        
        return {
            'labels': labels,
            'stories': stories,
            'games': games,
            'time': time_spent,
            'stars': stars
        }
    
    else:
        return {
            'error': f'Invalid period type for chart data: {period_type}'
        }


def send_weekly_report_email(child_id, week_start=None):
    """
    Send weekly report email to the parent
    
    Args:
        child_id (int): The ID of the child
        week_start (date, optional): Start of the week for the report
    
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    # This will be implemented when email functionality is added
    # For now, we'll just return False
    return False