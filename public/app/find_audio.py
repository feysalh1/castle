import os
import requests
import trafilatura
from urllib.parse import urlparse, unquote
import json
import re
import time

# List of stories to find audio for
stories = [
    {"id": "little_fox", "title": "The Little Fox", "filename": "little_fox.mp3"},
    {"id": "three_little_pigs", "title": "Three Little Pigs", "filename": "three_little_pigs.mp3"},
    {"id": "brown_bear", "title": "Brown Bear", "filename": "brown_bear.mp3"},
    {"id": "wild_things", "title": "Where the Wild Things Are", "filename": "wild_things.mp3"},
    {"id": "black_sheep", "title": "Baa Baa Black Sheep", "filename": "black_sheep.mp3"},
    {"id": "hickory_dickory", "title": "Hickory Dickory Dock", "filename": "hickory_dickory.mp3"},
    {"id": "bo_peep", "title": "Little Bo-Peep", "filename": "bo_peep.mp3"},
    {"id": "jack_jill", "title": "Jack and Jill", "filename": "jack_jill.mp3"}
]

def search_audio(story_title):
    """
    Search for audio files for a story using various methods.
    Returns a list of potential URLs.
    """
    print(f"Searching for audio files for: {story_title}")
    
    # List of sites that may have free nursery rhymes and children's stories
    search_terms = [
        f"{story_title} children's story audio mp3 free",
        f"{story_title} nursery rhyme audio for kids",
        f"{story_title} storytime free audio"
    ]
    
    # Add specific search queries for common nursery rhymes
    if "black sheep" in story_title.lower():
        search_terms.append("baa baa black sheep nursery rhyme free mp3")
    elif "bo-peep" in story_title.lower():
        search_terms.append("little bo peep nursery rhyme free mp3")
    elif "hickory" in story_title.lower():
        search_terms.append("hickory dickory dock nursery rhyme free mp3")
    elif "jack and jill" in story_title.lower():
        search_terms.append("jack and jill nursery rhyme free mp3")
    elif "three little pigs" in story_title.lower():
        search_terms.append("three little pigs story for children audio free")
    
    found_urls = []
    for term in search_terms:
        try:
            print(f"Searching with term: {term}")
            # Search sites that might have free audio files
            search_sites = [
                f"https://freekidsbooks.org/search/{'+'.join(term.split())}",
                f"https://www.storynory.com/?s={'+'.join(term.split())}",
                f"https://loyalbooks.com/search?q={'+'.join(term.split())}"
            ]
            
            for site in search_sites:
                try:
                    print(f"Checking site: {site}")
                    downloaded = trafilatura.fetch_url(site)
                    if downloaded:
                        html_content = downloaded.decode('utf-8', errors='ignore')
                        
                        # Look for mp3 links in the HTML content
                        mp3_pattern = r'https?://[^\s"\'<>]+\.mp3'
                        mp3_urls = re.findall(mp3_pattern, html_content)
                        
                        for url in mp3_urls:
                            print(f"Found potential audio URL: {url}")
                            found_urls.append(url)
                except Exception as e:
                    print(f"Error searching {site}: {e}")
                    continue
                
                # Don't overwhelm servers with requests
                time.sleep(1)
        except Exception as e:
            print(f"Error with search term {term}: {e}")
    
    return found_urls

def download_audio_file(url, filename, directory="downloads"):
    """Download an audio file from a URL."""
    try:
        print(f"Attempting to download: {url}")
        response = requests.get(url, stream=True, timeout=10)
        
        if response.status_code == 200:
            # Make sure we're getting audio content
            content_type = response.headers.get('Content-Type', '')
            if 'audio' in content_type or url.endswith('.mp3'):
                filepath = os.path.join(directory, filename)
                with open(filepath, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"Successfully downloaded: {filename}")
                return filepath
            else:
                print(f"Not an audio file. Content-Type: {content_type}")
        else:
            print(f"Failed to download. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")
    
    return None

def check_librivox_api(story_title):
    """Search LibriVox API for public domain audio books."""
    try:
        base_url = "https://librivox.org/api/feed/audiobooks"
        params = {
            "title": story_title,
            "format": "json",
            "limit": 5
        }
        
        response = requests.get(base_url, params=params)
        if response.status_code == 200:
            data = response.json()
            results = []
            
            if 'books' in data:
                for book in data['books']:
                    if 'url_zip_file' in book:
                        results.append({
                            'title': book.get('title'),
                            'url': book.get('url_zip_file'),
                            'source': 'LibriVox'
                        })
            
            return results
    except Exception as e:
        print(f"Error checking LibriVox API: {e}")
    
    return []

def check_freepd_site(story_title):
    """Check freepd.com for free audio."""
    base_url = "https://freepd.com"
    try:
        downloaded = trafilatura.fetch_url(base_url)
        if downloaded:
            html_content = downloaded.decode('utf-8', errors='ignore')
            
            # Look for links to audio files
            mp3_pattern = r'href=["\'](https?://[^\s"\'<>]+\.mp3)["\']'
            mp3_links = re.findall(mp3_pattern, html_content)
            
            results = []
            for link in mp3_links:
                filename = os.path.basename(link)
                if any(keyword in filename.lower() for keyword in story_title.lower().split()):
                    results.append({
                        'title': filename,
                        'url': link,
                        'source': 'FreePD'
                    })
            
            return results
    except Exception as e:
        print(f"Error checking FreePD: {e}")
    
    return []

def main():
    """Main function to find and download audio files for all stories."""
    results = {}
    
    for story in stories:
        print(f"\n{'='*50}")
        print(f"Processing: {story['title']}")
        print(f"{'='*50}")
        
        # Search for audio files
        urls = search_audio(story['title'])
        
        # Check LibriVox
        print(f"Checking LibriVox for {story['title']}...")
        librivox_results = check_librivox_api(story['title'])
        for result in librivox_results:
            print(f"Found on LibriVox: {result['title']} - {result['url']}")
        
        # Check FreePD
        print(f"Checking FreePD for {story['title']}...")
        freepd_results = check_freepd_site(story['title'])
        for result in freepd_results:
            print(f"Found on FreePD: {result['title']} - {result['url']}")
        
        # Common nursery rhyme sites for specific stories
        if "black sheep" in story['title'].lower() or "bo-peep" in story['title'].lower() or "hickory" in story['title'].lower() or "jack and jill" in story['title'].lower():
            nursery_rhyme_sites = [
                "https://www.nurseryrhymes.org/audio/",
                "https://www.kididdles.com/mousic/"
            ]
            for site in nursery_rhyme_sites:
                try:
                    print(f"Checking nursery rhyme site: {site}")
                    downloaded = trafilatura.fetch_url(site)
                    if downloaded:
                        html_content = downloaded.decode('utf-8', errors='ignore')
                        
                        # Look for likely filenames based on story title
                        keywords = story['title'].lower().replace('-', '').split()
                        mp3_pattern = r'href=["\'](https?://[^\s"\'<>]+\.mp3)["\']'
                        mp3_links = re.findall(mp3_pattern, html_content)
                        
                        for link in mp3_links:
                            filename = os.path.basename(link).lower()
                            if any(keyword in filename for keyword in keywords):
                                print(f"Found potential nursery rhyme audio: {link}")
                                urls.append(link)
                except Exception as e:
                    print(f"Error checking nursery rhyme site {site}: {e}")
        
        # Download the first available audio file
        downloaded_file = None
        for url in urls:
            downloaded_file = download_audio_file(url, story['filename'])
            if downloaded_file:
                break
        
        results[story['id']] = {
            'title': story['title'],
            'urls_found': urls,
            'downloaded_file': downloaded_file
        }
        
        # Don't overwhelm servers
        time.sleep(2)
    
    # Write results to a JSON file for reference
    with open('audio_search_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\nResults summary:")
    for story_id, data in results.items():
        status = "✓ Downloaded" if data['downloaded_file'] else "❌ Not found"
        print(f"{data['title']}: {status}")

if __name__ == "__main__":
    print("Starting audio file search and download...")
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    main()