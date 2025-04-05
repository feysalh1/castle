import requests
import os
import time
import json
from urllib.parse import quote

# List of stories to find audio for
stories = [
    {"id": "little_fox", "title": "The Little Fox", "filename": "little_fox.mp3", "search_terms": ["fox story for children audio"]},
    {"id": "three_little_pigs", "title": "Three Little Pigs", "filename": "three_little_pigs.mp3", "search_terms": ["three little pigs story nursery rhyme audio"]},
    {"id": "brown_bear", "title": "Brown Bear", "filename": "brown_bear.mp3", "search_terms": ["brown bear brown bear what do you see audio", "eric carle brown bear audio"]},
    {"id": "wild_things", "title": "Where the Wild Things Are", "filename": "wild_things.mp3", "search_terms": ["where the wild things are audio story"]},
    {"id": "black_sheep", "title": "Baa Baa Black Sheep", "filename": "black_sheep.mp3", "search_terms": ["baa baa black sheep nursery rhyme audio"]},
    {"id": "hickory_dickory", "title": "Hickory Dickory Dock", "filename": "hickory_dickory.mp3", "search_terms": ["hickory dickory dock nursery rhyme audio"]},
    {"id": "bo_peep", "title": "Little Bo-Peep", "filename": "bo_peep.mp3", "search_terms": ["little bo peep nursery rhyme audio"]},
    {"id": "jack_jill", "title": "Jack and Jill", "filename": "jack_jill.mp3", "search_terms": ["jack and jill nursery rhyme audio"]}
]

# Direct URLs for common nursery rhymes from free sources
KNOWN_AUDIO_URLS = {
    "baa_baa_black_sheep": [
        "https://www.nurseryrhymes.org/audio/baa-baa-black-sheep.mp3"
    ],
    "hickory_dickory_dock": [
        "https://www.nurseryrhymes.org/audio/hickory-dickory-dock.mp3"
    ],
    "little_bo_peep": [
        "https://www.nurseryrhymes.org/audio/little-bo-peep.mp3"
    ],
    "jack_and_jill": [
        "https://www.nurseryrhymes.org/audio/jack-and-jill.mp3"
    ],
    "three_little_pigs": [
        "https://www.storynory.com/wp-content/uploads/2006/12/three-pigs.mp3"
    ]
}

def download_audio_file(url, filename, directory="static/audio"):
    """Download an audio file from a URL to the specified directory."""
    try:
        print(f"Attempting to download: {url} to {filename}")
        response = requests.get(url, stream=True, timeout=15)
        
        if response.status_code == 200:
            # Make sure we're getting audio content
            content_type = response.headers.get('Content-Type', '')
            if 'audio' in content_type or url.lower().endswith('.mp3'):
                filepath = os.path.join(directory, filename)
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"✓ Successfully downloaded: {filename} to {filepath}")
                return filepath
            else:
                print(f"✗ Not an audio file. Content-Type: {content_type}")
        else:
            print(f"✗ Failed to download. Status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Error downloading {url}: {e}")
    
    return None

def check_common_sources():
    """Check common sources for the specified stories."""
    results = {}
    
    # Create directories if they don't exist
    if not os.path.exists("static/audio"):
        os.makedirs("static/audio")
    
    for story in stories:
        print(f"\n{'='*50}")
        print(f"Processing: {story['title']}")
        print(f"{'='*50}")
        
        # Check if we have direct URLs for this story type
        story_key = None
        for key in KNOWN_AUDIO_URLS:
            if key.replace("_", " ") in story['title'].lower():
                story_key = key
                break
        
        if story_key:
            print(f"Found known URLs for {story['title']}")
            urls = KNOWN_AUDIO_URLS[story_key]
            
            # Try each URL until one works
            downloaded_file = None
            for url in urls:
                downloaded_file = download_audio_file(url, story['filename'])
                if downloaded_file:
                    break
                time.sleep(1)
            
            if downloaded_file:
                results[story['id']] = {
                    'title': story['title'],
                    'status': 'Downloaded',
                    'source': url
                }
                continue
        
        # If no direct URL worked, mark as not found
        print(f"✗ Could not find audio for: {story['title']}")
        results[story['id']] = {
            'title': story['title'],
            'status': 'Not found',
            'source': None
        }
        
        # Don't overwhelm with requests
        time.sleep(1)
    
    # Write results to a file
    with open('audio_download_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    return results

if __name__ == "__main__":
    print("Starting search for audio files...")
    results = check_common_sources()
    
    # Print summary
    print("\nDownload Summary:")
    for story_id, info in results.items():
        status_icon = "✓" if info['status'] == 'Downloaded' else "✗"
        print(f"{status_icon} {info['title']}: {info['status']}")