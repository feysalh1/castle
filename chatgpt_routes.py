"""
ChatGPT integration routes for Children's Castle application.
These routes handle API endpoints for the AI assistant features.
"""

import logging
from flask import Blueprint, jsonify, request, session, render_template, flash, redirect, url_for
from flask_login import current_user, login_required
import chatgpt_helper
from app import csrf, db

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
    from models import Session
    user_session = Session.query.filter_by(
        user_type='child',
        user_id=current_user.id,
        end_time=None
    ).order_by(Session.start_time.desc()).first()
    
    if user_session:
        user_session.record_activity('view_ai_assistant')
        db.session.commit()
    
    return render_template('ai_assistant.html')

@chatgpt_bp.route('/api/ask-assistant', methods=['POST'])
@login_required
@csrf.exempt
def ask_assistant():
    """API endpoint to ask the AI assistant a question"""
    # Check if user is a child
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
    from models import Child
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
    if session.get('user_type') != 'child':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    # Get request data
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    prompt = data.get('prompt', 'a magical adventure')
    include_questions = data.get('include_questions', True)
    
    # Get child's age from database
    from models import Child
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
    from models import Child
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
    """API endpoint to get learning tips and answer questions for parents"""
    # Check if user is a parent
    if session.get('user_type') != 'parent':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    # Get request data
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    # We can handle both specific learning topics and general questions
    topic = data.get('topic', None)
    question = data.get('question', None)
    child_id = data.get('child_id')
    
    # If child_id is provided, get child's age
    child_age = 4
    if child_id:
        from models import Child
        child = Child.query.filter_by(id=child_id, parent_id=current_user.id).first()
        if child and hasattr(child, 'age') and child.age:
            child_age = child.age
    
    # Check if this is a question or a topic request
    if question:        
        # Add this interaction to the database for future reference
        try:
            # Track the parent's question
            from app import tracking
            tracking.track_custom_event(
                event_type='parent_assistant',
                event_name='question_asked',
                event_data={
                    'question': question,
                    'user_id': current_user.id
                }
            )
        except Exception as e:
            logging.error(f"Error tracking parent question: {e}")
        
        # Process specific question types
        if any(keyword in question.lower() for keyword in ['limit screen time', 'screen time', 'time limit']):
            response = chatgpt_helper.generate_parent_advice(
                "Here are some strategies for limiting screen time effectively: " +
                "Set clear boundaries with specific time limits. " +
                "Create screen-free zones in your home. " +
                "Use the parental controls in Children's Castle to set daily usage limits. " +
                "Offer engaging alternatives like reading physical books or outdoor play. " +
                "Be consistent with the rules you establish."
            )
        elif any(keyword in question.lower() for keyword in ['stories', 'read today', 'reading history']):
            response = "You can view your child's reading history in the Activity Summaries section of this dashboard. " + \
                       "Look for the 'Recent Activity' card to see which stories they've engaged with recently."
        elif any(keyword in question.lower() for keyword in ['bedtime', 'bedtime mode']):
            response = "To enable bedtime mode, go to the Control Center section of this dashboard. " + \
                       "In the 'Access Controls' card, you can set specific bedtime hours when the app will " + \
                       "automatically show calming content and gradually reduce stimulation."
        else:
            # Generate a response for any other question
            # It's a general question, so just generate advice
            response = chatgpt_helper.generate_parent_advice(question, child_age)
        
        return jsonify({
            'success': True,
            'response': response
        })
    elif topic:
        # It's a topic request, generate a learning tip
        tip = chatgpt_helper.generate_learning_tip(topic, child_age)
        return jsonify({
            'success': True,
            'response': tip
        })
    else:
        return jsonify({
            'success': False, 
            'message': 'No question or topic provided'
        }), 400
