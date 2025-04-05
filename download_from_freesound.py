import requests
import os
import json
import time

# List of stories we need audio for
stories = [
    {"id": "little_fox", "title": "The Little Fox", "filename": "little_fox.mp3", "keywords": ["fox", "story", "children"]},
    {"id": "three_little_pigs", "title": "Three Little Pigs", "filename": "three_little_pigs.mp3", "keywords": ["three", "pigs", "story", "children", "nursery"]},
    {"id": "brown_bear", "title": "Brown Bear", "filename": "brown_bear.mp3", "keywords": ["brown", "bear", "story", "children"]},
    {"id": "wild_things", "title": "Where the Wild Things Are", "filename": "wild_things.mp3", "keywords": ["wild", "things", "story", "children"]},
    {"id": "black_sheep", "title": "Baa Baa Black Sheep", "filename": "black_sheep.mp3", "keywords": ["black", "sheep", "baa", "nursery", "rhyme"]},
    {"id": "hickory_dickory", "title": "Hickory Dickory Dock", "filename": "hickory_dickory.mp3", "keywords": ["hickory", "dickory", "nursery", "rhyme"]},
    {"id": "bo_peep", "title": "Little Bo-Peep", "filename": "bo_peep.mp3", "keywords": ["bo", "peep", "nursery", "rhyme"]},
    {"id": "jack_jill", "title": "Jack and Jill", "filename": "jack_jill.mp3", "keywords": ["jack", "jill", "nursery", "rhyme"]}
]

# Free children's stories from Librivox - direct download URLs
LIBRIVOX_URLS = {
    "three_little_pigs": "https://ia800203.us.archive.org/15/items/three_little_pigs_librivox/threelittlepigs_01_jacobs.mp3",
    "little_red_riding_hood": "https://ia801408.us.archive.org/34/items/little_red_riding_hood_1101_librivox/littleredridinghood_01_grimm.mp3",
    "jack_and_the_beanstalk": "https://ia800809.us.archive.org/24/items/jack_beanstalk_librivox/jackbeanstalk_1_jacobs.mp3"
}

# Public domain nursery rhymes from Archive.org
ARCHIVE_NURSERY_RHYMES = {
    "black_sheep": "https://ia801406.us.archive.org/24/items/NurseryRhymesKidsAudio/Baa%20Baa%20Black%20Sheep.mp3",
    "hickory_dickory": "https://ia801406.us.archive.org/24/items/NurseryRhymesKidsAudio/Hickory%20Dickory%20Dock.mp3",
    "bo_peep": "https://ia801406.us.archive.org/24/items/NurseryRhymesKidsAudio/Little%20Bo%20Peep.mp3",
    "jack_jill": "https://ia801406.us.archive.org/24/items/NurseryRhymesKidsAudio/Jack%20And%20Jill.mp3"
}

def download_audio_file(url, filename, directory="static/audio"):
    """Download an audio file from a URL."""
    try:
        print(f"Attempting to download: {url}")
        response = requests.get(url, stream=True, timeout=30)
        
        if response.status_code == 200:
            # Check if it seems to be audio content
            content_type = response.headers.get('Content-Type', '')
            if 'audio' in content_type or '.mp3' in url.lower() or '.wav' in url.lower():
                filepath = os.path.join(directory, filename)
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                # Verify file size is reasonable
                if os.path.getsize(filepath) > 10000:  # More than 10KB
                    print(f"✓ Successfully downloaded: {filename}")
                    return filepath
                else:
                    print(f"✗ File too small, might not be valid audio: {filepath}")
                    os.remove(filepath)
            else:
                print(f"✗ Not an audio file. Content-Type: {content_type}")
        else:
            print(f"✗ Failed to download. Status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Error downloading {url}: {e}")
    
    return None

def attempt_archive_download():
    """Try to download from Internet Archive's public domain audio collections."""
    results = {}
    
    # Ensure the audio directory exists
    if not os.path.exists("static/audio"):
        os.makedirs("static/audio")
    
    for story in stories:
        print(f"\n{'='*50}")
        print(f"Processing: {story['title']}")
        print(f"{'='*50}")
        
        downloaded_file = None
        story_id = story['id']
        
        # Check nursery rhymes from Archive.org
        if story_id in ARCHIVE_NURSERY_RHYMES:
            url = ARCHIVE_NURSERY_RHYMES[story_id]
            print(f"Found a nursery rhyme URL for {story['title']}")
            downloaded_file = download_audio_file(url, story['filename'])
        
        # Check LibriVox stories
        elif story_id in LIBRIVOX_URLS:
            url = LIBRIVOX_URLS[story_id]
            print(f"Found a LibriVox URL for {story['title']}")
            downloaded_file = download_audio_file(url, story['filename'])
        
        # For files we don't have direct URLs, mark as not found
        if not downloaded_file:
            print(f"✗ No audio found for: {story['title']}")
            results[story_id] = {
                'title': story['title'],
                'status': 'Not found',
                'source': None
            }
        else:
            results[story_id] = {
                'title': story['title'],
                'status': 'Downloaded',
                'source': url if 'url' in locals() else None
            }
        
        # Don't overwhelm the server
        time.sleep(1)
    
    # Write results to a JSON file
    with open('download_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("\nDownload Summary:")
    for story_id, info in results.items():
        status_icon = "✓" if info['status'] == 'Downloaded' else "✗"
        print(f"{status_icon} {info['title']}: {info['status']}")
    
    return results

if __name__ == "__main__":
    print("Starting audio download from Internet Archive...")
    attempt_archive_download()