"""
Story enhancement routes for Children's Castle application.
These routes handle enhanced story generation, preview, and audio features.
"""

import os
import json
import logging
from flask import (
    Blueprint, render_template, redirect, url_for, request, 
    jsonify, current_app, flash, abort
)
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, Progress, Child
from generate_elevenlabs_audio import (
    initialize_elevenlabs, 
    generate_audio_for_text,
    list_available_voices,
    CHARACTER_VOICES
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create Blueprint
story_enhancement = Blueprint('story_enhancement', __name__)

# Constants
STORIES_DIR = "static/stories"
IMAGES_DIR = "static/images/stories"
AUDIO_DIR = "static/audio"

@story_enhancement.route('/story-preview/<story_id>')
@login_required
def story_preview(story_id):
    """Preview a story with enhanced features"""
    # Sanitize the story_id to prevent path traversal
    story_id = secure_filename(story_id)
    
    # Load the story data
    story_path = os.path.join(STORIES_DIR, f"{story_id}.json")
    
    if not os.path.exists(story_path):
        flash("Story not found", "error")
        return redirect(url_for('story_mode'))
    
    try:
        with open(story_path, 'r') as f:
            story = json.load(f)
            
        # Render the preview template
        return render_template('story_preview.html', 
                              story=story, 
                              story_id=story_id)
    except Exception as e:
        logger.error(f"Error loading story {story_id}: {str(e)}")
        flash("Error loading story data", "error")
        return redirect(url_for('story_mode'))

@story_enhancement.route('/api/available-stories')
@login_required
def available_stories():
    """Get a list of available enhanced stories"""
    try:
        if not os.path.exists(STORIES_DIR):
            return jsonify([])
        
        stories = []
        for file in os.listdir(STORIES_DIR):
            if file.endswith('.json'):
                story_id = os.path.splitext(file)[0]
                
                # Load the story data
                try:
                    with open(os.path.join(STORIES_DIR, file), 'r') as f:
                        story_data = json.load(f)
                        
                    # Check if the story has audio files
                    has_audio = all('audio' in page and page['audio'] 
                                    for page in story_data.get('pages', []))
                    
                    stories.append({
                        'id': story_id,
                        'title': story_data.get('title', f"Story {story_id}"),
                        'pages': len(story_data.get('pages', [])),
                        'has_audio': has_audio
                    })
                except Exception as e:
                    logger.warning(f"Error reading story file {file}: {str(e)}")
        
        return jsonify(stories)
    except Exception as e:
        logger.error(f"Error getting available stories: {str(e)}")
        return jsonify([])

@story_enhancement.route('/api/generate-audio', methods=['POST'])
@login_required
def generate_audio():
    """Generate audio for text using ElevenLabs API"""
    # Initialize ElevenLabs API
    if not initialize_elevenlabs():
        return jsonify({
            'success': False,
            'error': 'ElevenLabs API key not configured'
        })
    
    # Get request data
    data = request.json
    text = data.get('text')
    voice_type = data.get('voice_type', 'narrator')
    
    if not text:
        return jsonify({
            'success': False,
            'error': 'No text provided'
        })
    
    # Get voice ID based on voice type
    voice_id = CHARACTER_VOICES.get(voice_type, CHARACTER_VOICES['narrator'])
    
    try:
        # Generate audio
        audio_data = generate_audio_for_text(text, voice_id)
        
        if not audio_data:
            return jsonify({
                'success': False,
                'error': 'Failed to generate audio'
            })
        
        # Return base64-encoded audio data
        import base64
        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
        
        return jsonify({
            'success': True,
            'audio_data': audio_base64
        })
    except Exception as e:
        logger.error(f"Error generating audio: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

@story_enhancement.route('/api/voices')
@login_required
def get_voices():
    """Get available ElevenLabs voices"""
    # Initialize ElevenLabs API
    if not initialize_elevenlabs():
        return jsonify({
            'success': False,
            'error': 'ElevenLabs API key not configured'
        })
    
    try:
        # Get available voices
        voices = list_available_voices()
        
        # Also include our character mapping
        character_voices = []
        for char_type, voice_id in CHARACTER_VOICES.items():
            # Find the voice name if available
            voice_name = next((v['name'] for v in voices if v['id'] == voice_id), "Unknown")
            character_voices.append({
                'character_type': char_type,
                'voice_id': voice_id,
                'voice_name': voice_name
            })
        
        return jsonify({
            'success': True,
            'voices': voices,
            'character_voices': character_voices
        })
    except Exception as e:
        logger.error(f"Error getting voices: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        })

@story_enhancement.route('/run-story-enhancement')
@login_required
def run_enhancement():
    """Run the story enhancement process (admin only)"""
    # Check if user is an admin
    if not hasattr(current_user, 'is_admin') or not current_user.is_admin:
        flash("Admin access required", "error")
        return redirect(url_for('parent_dashboard'))
    
    try:
        # Import the script and run it
        from generate_enhanced_stories import process_all
        
        # Run the process
        result = process_all(pages=3, force=False)
        
        if result:
            flash("Story enhancement completed successfully", "success")
        else:
            flash("Story enhancement failed", "error")
            
        return redirect(url_for('parent_dashboard'))
    except Exception as e:
        logger.error(f"Error running story enhancement: {str(e)}")
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for('parent_dashboard'))

# For child users, track progress when they view enhanced stories
@story_enhancement.route('/api/track-enhanced-story', methods=['POST'])
@login_required
def track_enhanced_story():
    """Track child's progress with enhanced stories"""
    if not hasattr(current_user, 'type') or current_user.type != 'child':
        return jsonify({
            'success': False,
            'error': 'Only child users can track story progress'
        })
    
    # Get request data
    data = request.json
    story_id = data.get('story_id')
    page_number = data.get('page_number', 1)
    completed = data.get('completed', False)
    time_spent = data.get('time_spent', 0)
    
    if not story_id:
        return jsonify({
            'success': False,
            'error': 'No story ID provided'
        })
    
    try:
        # Get the story info to record the title
        story_path = os.path.join(STORIES_DIR, f"{story_id}.json")
        story_title = f"Story {story_id}"
        
        if os.path.exists(story_path):
            with open(story_path, 'r') as f:
                story_data = json.load(f)
                story_title = story_data.get('title', story_title)
        
        # Create a progress record
        progress = Progress(
            child_id=current_user.id,
            content_type='enhanced_story',
            content_id=story_id,
            content_title=story_title,
            page_number=page_number,
            completed=completed,
            time_spent=time_spent
        )
        
        db.session.add(progress)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Progress tracked successfully'
        })
    except Exception as e:
        logger.error(f"Error tracking story progress: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        })