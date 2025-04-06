import os
import json
import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set the API key
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

# Voice character mapping using voice IDs (for different story characters)
CHARACTER_VOICES = {
    "narrator": "EXAVITQu4vr4xnSDxMaL",     # Sarah - Default storyteller
    "child": "pFZP5JQG7iQjIQuC4Bku",        # Lily - Child characters
    "animal": "CwhRBWXzGAHq8TQ4Fs17",       # Roger - Animal characters
    "adult_male": "JBFqnCBsd6RMkjVDRZzb",    # George - Adult male characters
    "adult_female": "XB0fDUnXU5powFXDhCwa",  # Charlotte - Adult female characters
    "fantasy": "N2lVS1w4EtoT3dr4eOWO"        # Callum - Fantasy/magical characters
}

def initialize_elevenlabs():
    """Check if ElevenLabs API key is set"""
    if not ELEVENLABS_API_KEY:
        logger.error("ELEVENLABS_API_KEY environment variable not set")
        return False
    
    logger.info("ElevenLabs API key is set")
    return True

def generate_audio_for_text(text, voice_id="EXAVITQu4vr4xnSDxMaL", output_path=None):
    """Generate audio for the given text using ElevenLabs REST API directly"""
    try:
        if not ELEVENLABS_API_KEY:
            logger.error("ElevenLabs API key not set")
            return None
        
        # Create output directory if it doesn't exist
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Direct API call to ElevenLabs
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": ELEVENLABS_API_KEY
        }
        
        # Set child-friendly voice settings
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.75,
                "similarity_boost": 0.75,
                "style": 0.3,
                "use_speaker_boost": True
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            if output_path:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
                logger.info(f"Audio saved to {output_path}")
                return output_path
            else:
                return response.content
        else:
            logger.error(f"Error from ElevenLabs API: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"Error generating audio: {str(e)}")
        return None

def list_available_voices():
    """List all available ElevenLabs voices with their IDs"""
    try:
        url = "https://api.elevenlabs.io/v1/voices"
        headers = {"xi-api-key": ELEVENLABS_API_KEY}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            voices_data = response.json()
            voices = [{"name": voice["name"], "id": voice["voice_id"]} for voice in voices_data.get("voices", [])]
            return voices
        else:
            logger.error(f"Error listing voices: {response.status_code} - {response.text}")
            return []
    except Exception as e:
        logger.error(f"Error listing voices: {str(e)}")
        return []

def generate_character_audio(text, character_type="narrator", output_path=None):
    """Generate audio for a specific character type"""
    voice_id = CHARACTER_VOICES.get(character_type, "EXAVITQu4vr4xnSDxMaL")  # Sarah voice ID as fallback
    return generate_audio_for_text(text, voice_id, output_path)

def generate_story_audio(story_text, story_title, output_dir="static/audio/stories"):
    """Generate audio for an entire story with character detection"""
    try:
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Clean filename for the story
        clean_title = "".join(c if c.isalnum() else "_" for c in story_title.lower())
        output_path = f"{output_dir}/{clean_title}.mp3"
        
        # Generate audio for the entire story (as narrator voice)
        result = generate_audio_for_text(story_text, CHARACTER_VOICES["narrator"], output_path)
        
        if result:
            logger.info(f"Story audio generated for '{story_title}' at {output_path}")
            return output_path
        else:
            logger.error(f"Failed to generate audio for '{story_title}'")
            return None
    except Exception as e:
        logger.error(f"Error generating story audio: {str(e)}")
        return None

def get_user_subscription_info():
    """Get user subscription info from ElevenLabs API"""
    try:
        url = "https://api.elevenlabs.io/v1/user/subscription"
        headers = {"xi-api-key": ELEVENLABS_API_KEY}
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Error getting subscription info: {response.status_code} - {response.text}")
            return {}
    except Exception as e:
        logger.error(f"Error getting subscription info: {str(e)}")
        return {}

def get_remaining_character_count():
    """Get the remaining character count for the ElevenLabs API"""
    try:
        subscription_info = get_user_subscription_info()
        return subscription_info.get("character_count", {}).get("remaining", 0)
    except Exception as e:
        logger.error(f"Error getting remaining character count: {str(e)}")
        return 0

def generate_all_story_audio(stories_data, output_dir="static/audio/stories"):
    """Generate audio for all stories"""
    results = {}
    
    for story_id, story_info in stories_data.items():
        title = story_info.get('title', f'Story {story_id}')
        text = story_info.get('text', '')
        
        if not text:
            results[story_id] = {'status': 'error', 'message': 'No text content'}
            continue
        
        try:
            output_path = generate_story_audio(text, title, output_dir)
            if output_path:
                results[story_id] = {
                    'status': 'success',
                    'path': output_path,
                    'title': title
                }
            else:
                results[story_id] = {'status': 'error', 'message': 'Generation failed'}
        except Exception as e:
            results[story_id] = {'status': 'error', 'message': str(e)}
    
    # Save results to a JSON file
    with open('audio_generation_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    return results

def main():
    """Main function to test the ElevenLabs integration"""
    if not initialize_elevenlabs():
        logger.error("Failed to initialize ElevenLabs API")
        return
    
    # List available voices
    available_voices = list_available_voices()
    voice_names = [f"{voice['name']} ({voice['id']})" for voice in available_voices]
    logger.info(f"Available voices: {', '.join(voice_names)}")
    
    # Test generating audio for a sample text
    sample_text = "Hello Menira! Welcome to Children's Castle. Let's read a fun story together!"
    output_path = "static/audio/welcome.mp3"
    
    if generate_audio_for_text(sample_text, CHARACTER_VOICES["narrator"], output_path):
        logger.info(f"Test audio generated successfully at {output_path}")
    else:
        logger.error("Failed to generate test audio")

if __name__ == "__main__":
    main()