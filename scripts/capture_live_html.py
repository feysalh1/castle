#!/usr/bin/env python3
"""
Script to capture live HTML from the running Flask application and prepare it for Firebase deployment.
This ensures the deployed version looks identical to the actual application.
"""

import os
import re
import json
import shutil
import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup

# Configuration
FLASK_APP_URL = "http://localhost:5000"
OUTPUT_DIR = "public"
PAGES_TO_CAPTURE = [
    # Main pages
    {"url": "/", "output": "index.html"},
    {"url": "/child/dashboard", "output": "story-mode.html"},
    {"url": "/game_mode", "output": "game-mode.html"},
    
    # Additional pages for a more complete experience
    {"url": "/parent/login", "output": "parent-login.html"},
    {"url": "/child/login", "output": "child-login.html"},
    
    # Add more pages as needed
    # {"url": "/other_page", "output": "other-page.html"},
]

# Make sure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_html_for_static(html, page_url):
    """Clean HTML and adjust URLs for static hosting"""
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove Flask-specific elements
    for form in soup.find_all('form'):
        # Remove CSRF tokens
        for input_tag in form.find_all('input', {'name': 'csrf_token'}):
            input_tag.decompose()
    
    # Replace any hardcoded API keys with placeholders
    html_str = str(soup)
    api_key_pattern = r'apiKey: "([A-Za-z0-9_\-]+)"'
    app_id_pattern = r'appId: "([0-9:\-]+)"'
    
    # Replace API keys with placeholder
    html_str = re.sub(api_key_pattern, 'apiKey: "FIREBASE_API_KEY"', html_str)
    html_str = re.sub(app_id_pattern, 'appId: "FIREBASE_APP_ID"', html_str)
    
    # Parse the modified HTML
    soup = BeautifulSoup(html_str, 'html.parser')
    
    # Replace Flask URL patterns
    for tag in soup.find_all(['a', 'link', 'script', 'img']):
        if tag.has_attr('href') and "{{ url_for" in tag['href']:
            # Handle url_for patterns
            match = re.search(r"url_for\('static', filename='(.+?)'\)", tag['href'])
            if match:
                tag['href'] = f"/{match.group(1)}"
        
        if tag.has_attr('src') and "{{ url_for" in tag['src']:
            # Handle url_for patterns in src attributes
            match = re.search(r"url_for\('static', filename='(.+?)'\)", tag['src'])
            if match:
                tag['src'] = f"/{match.group(1)}"
    
    # Fix static directory paths
    for tag in soup.find_all(['a', 'link', 'script', 'img']):
        for attr in ['href', 'src']:
            if tag.has_attr(attr) and '/static/' in tag[attr]:
                tag[attr] = tag[attr].replace('/static/', '/')
    
    # Modify all relative URLs to be Firebase-friendly
    for tag in soup.find_all(['a', 'link', 'script', 'img']):
        for attr in ['href', 'src']:
            if tag.has_attr(attr) and not tag[attr].startswith(('http://', 'https://', '#', 'javascript:', 'data:')):
                # Skip url_for patterns - already handled
                if "{{" in tag[attr] or "}}" in tag[attr]:
                    continue
                
                # For relative URLs, prepend with /
                if not tag[attr].startswith('/'):
                    tag[attr] = f"/{tag[attr]}"
    
    # Remap URLs for the Firebase static site
    for tag in soup.find_all('a'):
        if tag.has_attr('href'):
            # Convert internal links to the static versions
            href = tag['href']
            
            # Handle core routes
            if href == '/parent/login' or href == '/parent/dashboard':
                tag['href'] = '/parent-login.html'
            elif href == '/child/login':
                tag['href'] = '/child-login.html'
            elif href == '/child/dashboard':
                tag['href'] = '/story-mode.html'
            elif href == '/game_mode':
                tag['href'] = '/game-mode.html'
            # Add more route mappings as needed
    
    # Add Firebase configuration
    head = soup.find('head')
    if head:
        firebase_script = soup.new_tag('script')
        firebase_script['type'] = 'module'
        firebase_script.string = """
            // Import the functions you need from the SDKs
            import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
            import { getAuth } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";
            
            // Firebase configuration with environment variable placeholders
            const firebaseConfig = {
                apiKey: "FIREBASE_API_KEY",
                authDomain: "story-time-fun.firebaseapp.com",
                projectId: "story-time-fun",
                storageBucket: "story-time-fun.firebasestorage.app",
                messagingSenderId: "225122848236",
                appId: "FIREBASE_APP_ID",
            };
            
            // Initialize Firebase
            const app = initializeApp(firebaseConfig);
            const auth = getAuth(app);
            
            // Redirect to login if not authenticated (for protected pages)
            if ("REQUIRE_AUTH" === "true") {
                auth.onAuthStateChanged(user => {
                    if (!user && window.location.pathname !== '/index.html' && window.location.pathname !== '/') {
                        window.location.href = '/index.html';
                    }
                });
            }
        """
        head.append(firebase_script)
    
    # Add a modified Firebase adapter for functionality
    body = soup.find('body')
    if body:
        adapter_script = soup.new_tag('script')
        adapter_script.string = """
            // Firebase adapter for static hosting
            window.handleFirebaseAction = function(action, returnUrl) {
                // In the static deployment, log actions rather than performing them
                console.log('Firebase action:', action);
                
                // For demonstration, simulate the action feedback
                alert('This would perform ' + action + ' in the full application.');
                
                // For login/logout, simulate the navigation
                if (action === 'login') {
                    window.location.href = returnUrl || '/story-mode.html';
                } else if (action === 'logout') {
                    window.location.href = '/index.html';
                }
                
                return false; // Prevent form submission
            };
        """
        body.append(adapter_script)
    
    return str(soup)

def download_asset(url, output_path):
    """Download an asset from the Flask application"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Make sure the directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Write the content to the file
        with open(output_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        print(f"Downloaded asset: {output_path}")
        return True
    except Exception as e:
        print(f"Error downloading asset {url}: {e}")
        return False

def ensure_directory(directory):
    """Ensure a directory exists, creating it if necessary"""
    os.makedirs(directory, exist_ok=True)

def main():
    print("Starting to capture live HTML from Flask application...")
    
    # Create needed directories
    ensure_directory(os.path.join(OUTPUT_DIR, 'css'))
    ensure_directory(os.path.join(OUTPUT_DIR, 'js'))
    ensure_directory(os.path.join(OUTPUT_DIR, 'images'))
    ensure_directory(os.path.join(OUTPUT_DIR, 'audio'))
    ensure_directory(os.path.join(OUTPUT_DIR, 'data'))
    
    # First, copy static assets
    if os.path.exists('static'):
        print("Copying static assets...")
        shutil.copytree('static', OUTPUT_DIR, dirs_exist_ok=True)
    
    # Capture HTML pages
    for page in PAGES_TO_CAPTURE:
        try:
            page_url = urljoin(FLASK_APP_URL, page['url'])
            output_file = os.path.join(OUTPUT_DIR, page['output'])
            
            print(f"Capturing {page_url} to {output_file}...")
            
            # Get the HTML content
            response = requests.get(page_url)
            response.raise_for_status()
            
            # Clean the HTML
            cleaned_html = clean_html_for_static(response.text, page_url)
            
            # Write it to the output file
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(cleaned_html)
            
            # Find and download any missing static assets referenced in the HTML
            soup = BeautifulSoup(cleaned_html, 'html.parser')
            for tag in soup.find_all(['link', 'script', 'img']):
                for attr in ['href', 'src']:
                    if tag.has_attr(attr):
                        # Check if this is a static resource path
                        if any(path_type in tag[attr] for path_type in ['/css/', '/js/', '/images/']):
                            asset_url = urljoin(FLASK_APP_URL, tag[attr])
                            local_path = os.path.normpath(os.path.join(OUTPUT_DIR, tag[attr].lstrip('/')))
                            
                            # Only download if the file doesn't exist
                            if not os.path.exists(local_path):
                                try:
                                    download_asset(asset_url, local_path)
                                except Exception as e:
                                    print(f"  Warning: Could not download asset {asset_url}: {e}")
            
            print(f"Captured and processed {page_url}")
            
        except Exception as e:
            print(f"Error capturing {page['url']}: {e}")
    
    # Fix for common paths in Firebase hosting
    print("Creating common redirects for Firebase hosting...")
    
    # Create a 404 page that redirects to index.html
    not_found_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Page Not Found</title>
        <meta http-equiv="refresh" content="0;URL='/'">
    </head>
    <body>
        <p>If you are not redirected, <a href="/">click here</a>.</p>
        <script>window.location.href = "/";</script>
    </body>
    </html>
    """
    with open(os.path.join(OUTPUT_DIR, '404.html'), 'w') as f:
        f.write(not_found_html)
    
    print("HTML capture complete!")

if __name__ == "__main__":
    main()