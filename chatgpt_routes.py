"""
ChatGPT integration routes for Children's Castle application.
These routes handle API endpoints for the AI assistant features.
"""

from flask import Blueprint, jsonify, request, session, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
import chatgpt_helper
from app import csrf, db
# Removed import, Session, Conversation, ConversationMessage

# Create Blueprint for ChatGPT routes
chatgpt_bp = Blueprint('chatgpt', __name__)

@chatgpt_bp.route('/ai-assistant')
@login_required
def ai_assistant():
    """AI Assistant page for children"""
    # Check if user is a child
    if session.get('user_type') != 'child':
        flash('Access denied. This page is for children only.', 'error')
        return redirect(url_for('index'))
    
    # Record AI assistant access in session activity log
    user_session = Session.query.filter_by(
        user_type='child',
        user_id=current_user.id,
        end_time=None
    ).order_by(Session.start_time.desc()).first()
    
    if user_session:
        user_session.record_activity('view_ai_assistant')
        db.session.commit()
    
    # Removed import
    return render_template('ai_assistant.html')

@chatgpt_bp.route('/api/ask-assistant', methods=['POST'])
@login_required
@csrf.exempt
def ask_assistant():
    """API endpoint to ask the AI assistant a question"""
    # Check if user is a child
    # Removed import
    if session.get('user_type') != 'child':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    # Get request data
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    question = data.get('question')
    if not question:
        return jsonify({'success': False, 'message': 'No question provided'}), 400
    
    # Get child's age from database
    # Removed import
    child = Child.query.get(current_user.id)
    child_age = child.age if hasattr(child, 'age') and child.age else 4
    
    # Generate response using ChatGPT
    response = chatgpt_helper.generate_kid_friendly_response(question, child_age)
    
    # Determine the topic for analytics
    topic = 'general'
    if 'dinosaur' in question.lower():
        topic = 'dinosaurs'
    elif any(word in question.lower() for word in ['space', 'planet', 'star', 'moon']):
        topic = 'space'
    elif any(word in question.lower() for word in ['rain', 'weather', 'cloud', 'snow']):
        topic = 'weather'
    
    # Track this interaction
    # Removed import
    from app import tracking
    tracking.track_custom_event(
        event_type='ai_assistant',
        event_name='question_asked',
        event_data={
            'question': question,
            'topic': topic
        }
    )
    
    return jsonify({
        'success': True,
        'response': response,
        'topic': topic
    })

@chatgpt_bp.route('/api/generate-story', methods=['POST'])
@login_required
@csrf.exempt
def generate_story():
    """API endpoint to generate an interactive story"""
    # Check if user is a child
    # Removed import
    if session.get('user_type') != 'child':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    # Get request data
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    prompt = data.get('prompt', 'a magical adventure')
    include_questions = data.get('include_questions', True)
    
    # Get child's age from database
    # Removed import
    child = Child.query.get(current_user.id)
    child_age = child.age if hasattr(child, 'age') and child.age else 4
    
    # Generate interactive story
    story = chatgpt_helper.generate_interactive_story(
        prompt, 
        child_age=child_age,
        include_questions=include_questions
    )
    
    # Track story generation
    from app import tracking
    tracking.track_custom_event(
        event_type='ai_assistant',
        event_name='story_generated',
        event_data={
            'prompt': prompt,
            'title': story.get('title', 'Interactive Story'),
            'pages': len(story.get('pages', []))
        }
    )
    
    return jsonify({
        'success': True,
        'story': story
    })

@chatgpt_bp.route('/api/answer-question', methods=['POST'])
@login_required
@csrf.exempt
def answer_question():
    """API endpoint to respond to a child's answer to a story question"""
    # Check if user is a child
    # Removed import
    if session.get('user_type') != 'child':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    # Get request data
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    story_context = data.get('story_context', '')
    question = data.get('question', '')
    answer = data.get('answer', '')
    
    if not question or not answer:
        return jsonify({'success': False, 'message': 'Missing question or answer'}), 400
    
    # Get child's age from database
    # Removed import
    child = Child.query.get(current_user.id)
    child_age = child.age if hasattr(child, 'age') and child.age else 4
    
    # Generate response to the child's answer
    response = chatgpt_helper.answer_story_question(
        story_context=story_context,
        question=question,
        child_age=child_age
    )
    
    # Track the interaction
    from app import tracking
    tracking.track_custom_event(
        event_type='ai_assistant',
        event_name='question_answered',
        event_data={
            'question': question,
            'answer_length': len(answer)
        }
    )
    
    return jsonify({
        'success': True,
        'response': response
    })

@chatgpt_bp.route('/api/parent-tip', methods=['POST'])
@login_required
@csrf.exempt
def parent_tip():
    """API endpoint to get learning tips for parents"""
    # Check if user is a parent
    # Removed import
    if session.get('user_type') != 'parent':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    # Get request data
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    topic = data.get('topic', 'learning')
    child_id = data.get('child_id')
    
    # If child_id is provided, get child's age
    child_age = 4
    if child_id:
        # Removed import
        child = Child.query.filter_by(id=child_id, parent_id=current_user.id).first()
        if child and hasattr(child, 'age') and child.age:
            child_age = child.age
    
    # Generate learning tip
    tip = chatgpt_helper.generate_learning_tip(topic, child_age)
    
    return jsonify({
        'success': True,
        'tip': tip
    })