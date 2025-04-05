import os
import subprocess
import glob

def convert_wav_to_mp3():
    """Convert WAV files to MP3 format"""
    print("Converting audio files to MP3 format...")
    
    # Create a temporary directory for the conversion
    os.makedirs("temp_audio", exist_ok=True)
    
    # Get all audio files in the static/audio directory
    wav_files = glob.glob("static/audio/*.mp3")
    
    for wav_file in wav_files:
        base_name = os.path.basename(wav_file)
        mp3_file = os.path.join("temp_audio", base_name)
        
        try:
            # Use ffmpeg to convert WAV to MP3
            print(f"Converting {wav_file} to MP3...")
            cmd = [
                "ffmpeg",
                "-i", wav_file,
                "-acodec", "libmp3lame",
                "-q:a", "2",  # High quality
                mp3_file
            ]
            
            subprocess.run(cmd, check=True)
            print(f"✓ Converted: {base_name}")
        except Exception as e:
            print(f"✗ Error converting {base_name}: {e}")
    
    # Move the converted files back to the original location
    for mp3_file in glob.glob("temp_audio/*"):
        base_name = os.path.basename(mp3_file)
        dest_path = os.path.join("static/audio", base_name)
        
        # Remove the original file
        if os.path.exists(dest_path):
            os.remove(dest_path)
        
        # Move the converted file
        os.rename(mp3_file, dest_path)
    
    # Clean up the temporary directory
    os.rmdir("temp_audio")
    
    print("All files converted successfully!")

if __name__ == "__main__":
    convert_wav_to_mp3()