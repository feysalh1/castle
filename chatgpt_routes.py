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
    """AI Assistant page for children and guests"""
    # Check if user is a child or guest
    if session.get('user_type') not in ['child', 'guest']:
        flash('Access denied. This page is for children and guests only.', 'error')
        return redirect(url_for('index'))
    
    # Record AI assistant access in session activity log
    from models import Session
    user_session = Session.query.filter_by(
        user_type=session.get('user_type'),
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
    # Check if user is a child or guest
    if session.get('user_type') not in ['child', 'guest']:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    # Get request data
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    question = data.get('question')
    if not question:
        return jsonify({'success': False, 'message': 'No question provided'}), 400
    
    # Get child's age from database
    from models import Child, ChatHistory
    child = Child.query.get(current_user.id)
    child_age = child.age if hasattr(child, 'age') and child.age else 4
    
    try:
        # Generate response using ChatGPT
        response = chatgpt_helper.generate_kid_friendly_response(question, child_age)
        
        # Check if we received the default error response
        if "I'm having a little nap" in response:
            logging.warning("AI assistant failed to generate a response. OpenAI API may be unavailable.")
            # Add an error message to the database to track API issues
            chat_entry = ChatHistory(
                child_id=current_user.id,
                question=question,
                response="ERROR: AI assistant unavailable",
                topic="error",
                flagged_for_review=True
            )
            db.session.add(chat_entry)
            db.session.commit()
            
            return jsonify({
                'success': False, 
                'message': 'The AI assistant is unavailable right now. Please try again later.',
                'response': "I'm taking a nap right now. Please ask me again in a little while when I'm awake!"
            })
        
        # Determine the topic for analytics
        topic = 'general'
        if 'dinosaur' in question.lower():
            topic = 'dinosaurs'
        elif any(word in question.lower() for word in ['space', 'planet', 'star', 'moon']):
            topic = 'space'
        elif any(word in question.lower() for word in ['rain', 'weather', 'cloud', 'snow']):
            topic = 'weather'
        elif any(word in question.lower() for word in ['animal', 'animals', 'dog', 'cat', 'lion']):
            topic = 'animals'
        elif any(word in question.lower() for word in ['math', 'number', 'count', 'add', 'subtract']):
            topic = 'math'
        
        # Save the chat history for parent review
        chat_entry = ChatHistory(
            child_id=current_user.id,
            question=question,
            response=response,
            topic=topic,
            # Flag sensitive topics for parent review
            flagged_for_review=any(word in question.lower() for word in [
                'hurt', 'scared', 'afraid', 'bad', 'sad', 'angry', 'mad',
                'hate', 'die', 'kill', 'death', 'adult', 'alone'
            ])
        )
        db.session.add(chat_entry)
        db.session.commit()
        
        # Track this interaction
        from app import tracking
        tracking.track_custom_event(
            event_type='ai_assistant',
            event_name='question_asked',
            event_data={
                'question': question,
                'topic': topic,
                'chat_history_id': chat_entry.id
            }
        )
        
        return jsonify({
            'success': True,
            'response': response,
            'topic': topic
        })
        
    except Exception as e:
        logging.error(f"Error in ask_assistant endpoint: {e}")
        # Record the error in chat history for monitoring
        try:
            error_entry = ChatHistory(
                child_id=current_user.id,
                question=question,
                response=f"ERROR: {str(e)}",
                topic="error",
                flagged_for_review=True
            )
            db.session.add(error_entry)
            db.session.commit()
        except Exception as db_error:
            logging.error(f"Failed to save error to chat history: {db_error}")
        
        return jsonify({
            'success': False,
            'message': 'An error occurred processing your request.',
            'response': "I'm taking a nap right now. Please ask me again in a little while when I'm awake!"
        })

@chatgpt_bp.route('/api/generate-story', methods=['POST'])
@login_required
@csrf.exempt
def generate_story():
    """API endpoint to generate an interactive story"""
    # Check if user is a child or guest
    if session.get('user_type') not in ['child', 'guest']:
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
    
    try:
        # Generate interactive story
        story = chatgpt_helper.generate_interactive_story(
            prompt, 
            child_age=child_age,
            include_questions=include_questions
        )
        
        # Check if we got the default backup story (error case)
        if story.get('title') == "The Adventure of the Curious Child" and not prompt.lower().startswith("curious child"):
            logging.warning("Failed to generate story. OpenAI API may be unavailable.")
            return jsonify({
                'success': False,
                'message': 'The story creator is taking a break. Please try again later!',
                'story': story  # Still return the backup story so the UI can show something
            })
        
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
        
    except Exception as e:
        logging.error(f"Error in generate_story endpoint: {e}")
        
        # Create a backup story
        backup_story = {
            "title": "The Adventure of the Curious Child",
            "pages": [
                {
                    "content": "Once upon a time, there was a curious child who loved to explore the castle.",
                    "question": "What do you think the child found in the castle?"
                },
                {
                    "content": "The child found magical friends who taught them about kindness and friendship.",
                    "question": None
                },
                {
                    "content": "Together, they had wonderful adventures and learned important lessons. The End!",
                    "question": "What was your favorite part of the story?"
                }
            ]
        }
        
        return jsonify({
            'success': False,
            'message': 'Could not create your story right now. Here is another story instead!',
            'story': backup_story
        })

@chatgpt_bp.route('/api/answer-question', methods=['POST'])
@login_required
@csrf.exempt
def answer_question():
    """API endpoint to respond to a child's answer to a story question"""
    # Check if user is a child or guest
    if session.get('user_type') not in ['child', 'guest']:
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
    
    try:
        # Generate response to the child's answer
        response = chatgpt_helper.answer_story_question(
            story_context=story_context,
            question=question,
            child_age=child_age
        )
        
        # Check if we received the default encouraging response
        if response == "That's a wonderful answer! You're so creative and smart!":
            # This could indicate an API error as it's the default fallback response
            if not answer.lower().startswith("that's a wonderful"):  # Make sure not an echo
                logging.warning("Received default response from answer_story_question, possible API error")
        
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
        
    except Exception as e:
        logging.error(f"Error in answer_question endpoint: {e}")
        
        # Return a default encouraging response
        default_response = "That's a wonderful answer! You're so creative and smart!"
        
        return jsonify({
            'success': True,  # Still return success to not disrupt the UX for the child
            'response': default_response
        })

@chatgpt_bp.route('/parent/chat-history/<int:child_id>')
@login_required
def parent_chat_history(child_id):
    """Parent view of child's chat history with AI assistant"""
    # Check if user is a parent
    if session.get('user_type') != 'parent':
        flash('Access denied. This page is for parents only.', 'error')
        return redirect(url_for('index'))
    
    # Verify this child belongs to the current parent
    from models import Child, ChatHistory
    child = Child.query.filter_by(id=child_id, parent_id=current_user.id).first()
    if not child:
        flash('Child not found', 'error')
        return redirect(url_for('parent_dashboard'))
    
    # Get the chat history
    chat_history = ChatHistory.query.filter_by(child_id=child_id).order_by(ChatHistory.created_at.desc()).all()
    
    # Mark all entries as reviewed by parent
    for entry in chat_history:
        if not entry.parent_reviewed:
            entry.parent_reviewed = True
    db.session.commit()
    
    # Get flagged entries
    flagged_entries = [entry for entry in chat_history if entry.flagged_for_review]
    
    # Get topic stats
    from collections import Counter
    topics = [entry.topic for entry in chat_history]
    topic_counts = Counter(topics)
    sorted_topics = sorted(topic_counts.items(), key=lambda x: x[1], reverse=True)
    
    # Track this page view
    from app import tracking
    tracking.track_custom_event(
        event_type='parent_dashboard',
        event_name='view_chat_history',
        event_data={
            'child_id': child_id,
            'entries_count': len(chat_history)
        }
    )
    
    # Render the template
    return render_template(
        'parent_chat_history.html', 
        child=child, 
        chat_history=chat_history,
        flagged_entries=flagged_entries,
        sorted_topics=sorted_topics
    )


@chatgpt_bp.route('/api/parent/chat-history/<int:chat_id>/add-note', methods=['POST'])
@login_required
def add_chat_note(chat_id):
    """API endpoint for parents to add notes to chat entries"""
    # Check if user is a parent
    if session.get('user_type') != 'parent':
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    # Get request data
    data = request.json
    if not data:
        return jsonify({'success': False, 'message': 'No data provided'}), 400
    
    note = data.get('note')
    if not note:
        return jsonify({'success': False, 'message': 'No note provided'}), 400
    
    # Get the chat entry
    from models import ChatHistory
    chat_entry = ChatHistory.query.get(chat_id)
    if not chat_entry:
        return jsonify({'success': False, 'message': 'Chat entry not found'}), 404
    
    # Verify this child belongs to the current parent
    from models import Child
    child = Child.query.filter_by(id=chat_entry.child_id, parent_id=current_user.id).first()
    if not child:
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    # Add the note
    chat_entry.parent_note = note
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Note added successfully'
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
    
    # Track analytics for this request
    try:
        from app import tracking
        tracking.track_custom_event(
            event_type='parent_assistant',
            event_name='tip_requested' if topic else 'question_asked',
            event_data={
                'question': question,
                'topic': topic,
                'user_id': current_user.id
            }
        )
    except Exception as e:
        logging.error(f"Error tracking parent tip request: {e}")
    
    # Check if this is a question or a topic request
    try:
        if question:        
            # Process specific question types that don't require API
            if any(keyword in question.lower() for keyword in ['limit screen time', 'screen time', 'time limit']):
                response = "Here are some strategies for limiting screen time effectively: " + \
                           "Set clear boundaries with specific time limits. " + \
                           "Create screen-free zones in your home. " + \
                           "Use the parental controls in Children's Castle to set daily usage limits. " + \
                           "Offer engaging alternatives like reading physical books or outdoor play. " + \
                           "Be consistent with the rules you establish."
            elif any(keyword in question.lower() for keyword in ['stories', 'read today', 'reading history']):
                response = "You can view your child's reading history in the Activity Summaries section of this dashboard. " + \
                           "Look for the 'Recent Activity' card to see which stories they've engaged with recently."
            elif any(keyword in question.lower() for keyword in ['bedtime', 'bedtime mode']):
                response = "To enable bedtime mode, go to the Control Center section of this dashboard. " + \
                           "In the 'Access Controls' card, you can set specific bedtime hours when the app will " + \
                           "automatically show calming content and gradually reduce stimulation."
            elif any(keyword in question.lower() for keyword in ['asked', 'questions', 'chat history']):
                response = "You can view your child's chat history with the AI assistant by clicking on 'Chat History' " + \
                           "in the child's section of the dashboard. This shows all questions your child has asked, " + \
                           "the responses they received, and any content that might need your attention."
            else:
                # It's a general question, so use the GPT-4o API
                response = chatgpt_helper.generate_parent_advice(question, child_age)
                
                # Check if the API failed (default response)
                if "I recommend focusing on your child's interests" in response and not question.lower().startswith("what interests"):
                    logging.warning("Parent advice API may have failed - received default response")
            
            return jsonify({
                'success': True,
                'response': response
            })
            
        elif topic:
            # It's a topic request, generate a learning tip
            tip = chatgpt_helper.generate_learning_tip(topic, child_age)
            
            # Check if we got a default tip (API error)
            default_tip = f"Try incorporating {topic} into everyday activities through play."
            if default_tip in tip:
                logging.warning("Learning tip API may have failed - received default response")
            
            return jsonify({
                'success': True,
                'response': tip
            })
            
        else:
            return jsonify({
                'success': False, 
                'message': 'No question or topic provided'
            }), 400
            
    except Exception as e:
        logging.error(f"Error in parent_tip endpoint: {e}")
        
        # Provide a helpful response even if the API fails
        if topic:
            # Default tip response that doesn't require API
            response = f"Integrate {topic} learning into everyday activities. Use real-life situations to teach concepts naturally. Keep it fun and build on your child's interests. The most effective learning happens when children are engaged and enjoying themselves."
        else:
            # Default advice response that doesn't require API
            response = "Focus on creating consistent routines and setting clear expectations. Encourage your child's natural curiosity by asking open-ended questions. Remember that children learn best through play and exploration. The Children's Castle app offers personalized content based on your child's interests and learning style."
        
        return jsonify({
            'success': True,  # Still return success to avoid disrupting the UX
            'response': response
        })
