"""
Generate audio narration for story pages using ElevenLabs API.
This script processes JSON story files and generates audio files for each page.
"""

import os
import json
import argparse
import logging
from generate_elevenlabs_audio import (
    initialize_elevenlabs, 
    generate_audio_for_text,
    CHARACTER_VOICES
)

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
STORIES_DIR = "static/stories"
AUDIO_DIR = "static/audio/stories"

def ensure_directories_exist():
    """Ensure the necessary directories exist"""
    os.makedirs(STORIES_DIR, exist_ok=True)
    os.makedirs(AUDIO_DIR, exist_ok=True)

def get_story_files():
    """Get a list of all story JSON files"""
    if not os.path.exists(STORIES_DIR):
        return []
        
    return [f for f in os.listdir(STORIES_DIR) if f.endswith('.json')]

def load_story(story_id):
    """Load a story JSON file by ID"""
    story_path = os.path.join(STORIES_DIR, f"{story_id}.json")
    
    if not os.path.exists(story_path):
        logger.error(f"Story file not found: {story_path}")
        return None
        
    try:
        with open(story_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Error parsing JSON from {story_path}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Error loading story {story_path}: {str(e)}")
        return None

def save_story(story_data):
    """Save a story JSON file"""
    if not story_data or 'id' not in story_data:
        logger.error("Invalid story data, cannot save")
        return False
        
    story_path = os.path.join(STORIES_DIR, f"{story_data['id']}.json")
    
    try:
        with open(story_path, 'w') as f:
            json.dump(story_data, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error saving story to {story_path}: {str(e)}")
        return False

def generate_audio_for_page(page, story_id, force=False):
    """Generate audio for a single story page"""
    if not page or 'text' not in page:
        logger.warning("Invalid page data, skipping audio generation")
        return False
        
    # Check if this page already has audio and we're not forcing regeneration
    if 'audio' in page and os.path.exists(page['audio']) and not force:
        logger.info(f"Audio already exists for {story_id} page {page.get('page_number', '?')}")
        return True
        
    # Determine the audio filename
    page_number = page.get('page_number', 1)
    audio_filename = f"{story_id}_page{page_number}.mp3"
    audio_path = os.path.join(AUDIO_DIR, audio_filename)
    
    # Determine character voice to use
    character = page.get('character', 'narrator')
    voice_id = CHARACTER_VOICES.get(character, CHARACTER_VOICES['narrator'])
    
    # Generate the audio
    try:
        audio_data = generate_audio_for_text(page['text'], voice_id, output_path=audio_path)
        
        if not audio_data:
            logger.error(f"Failed to generate audio for {story_id} page {page_number}")
            return False
            
        # Update the page with the audio path
        page['audio'] = f"audio/stories/{audio_filename}"
        
        logger.info(f"Successfully generated audio for {story_id} page {page_number}")
        return True
    except Exception as e:
        logger.error(f"Error generating audio for {story_id} page {page_number}: {str(e)}")
        return False

def process_story(story_id, force=False):
    """Process all pages of a story and generate audio"""
    story = load_story(story_id)
    
    if not story:
        return False
        
    if 'pages' not in story or not story['pages']:
        logger.warning(f"Story {story_id} has no pages")
        return False
        
    # Initialize ElevenLabs API
    if not initialize_elevenlabs():
        logger.error("Failed to initialize ElevenLabs API")
        return False
        
    changes_made = False
    
    # Process each page
    for page in story['pages']:
        result = generate_audio_for_page(page, story_id, force)
        changes_made = changes_made or result
        
    # Save changes if any were made
    if changes_made:
        save_story(story)
        
    return changes_made

def process_all_stories(force=False):
    """Process all stories in the STORIES_DIR"""
    story_files = get_story_files()
    
    if not story_files:
        logger.warning("No story files found")
        return False
        
    results = {}
    
    for story_file in story_files:
        story_id = os.path.splitext(story_file)[0]
        logger.info(f"Processing story: {story_id}")
        
        result = process_story(story_id, force)
        results[story_id] = "Success" if result else "Failed or no changes needed"
        
    logger.info("Story processing results:")
    for story_id, status in results.items():
        logger.info(f"- {story_id}: {status}")
        
    return True

def main():
    """Main function to parse arguments and run audio generation"""
    parser = argparse.ArgumentParser(description="Generate audio for story pages using ElevenLabs")
    parser.add_argument("--story", help="ID of a specific story to process (omit for all)")
    parser.add_argument("--force", action="store_true", help="Force regeneration of existing audio files")
    args = parser.parse_args()
    
    ensure_directories_exist()
    
    if args.story:
        process_story(args.story, args.force)
    else:
        process_all_stories(args.force)
        
if __name__ == "__main__":
    main()