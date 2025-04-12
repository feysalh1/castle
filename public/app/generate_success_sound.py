from gtts import gTTS
import os

def generate_success_sound():
    """Generate a success sound using Text-to-Speech"""
    
    # Create the audio directory if it doesn't exist
    os.makedirs('static/audio', exist_ok=True)
    
    # Success message text
    success_text = "Great job! You did it!"
    
    # Create Text-to-Speech object with a slower rate and higher pitch
    tts = gTTS(text=success_text, lang='en', slow=False)
    
    # Save as MP3
    tts.save('static/audio/success.mp3')
    
    print("Success sound generated at static/audio/success.mp3")

if __name__ == "__main__":
    generate_success_sound()