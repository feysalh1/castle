#!/usr/bin/env python3
"""
Create multi-page stories from the existing single-text stories in generate_natural_voice.py.
This script will generate structured JSON files for each story, create SVG illustrations,
and prepare the file structure for audio generation.
"""

import os
import json
import random
import logging
import argparse
from pathlib import Path
from generate_natural_voice import stories

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Directory paths
STORIES_DIR = "static/stories"
IMAGES_DIR = "static/images/stories"
SVG_TEMPLATES_DIR = "static/images/templates"

# Create directories if they don't exist
os.makedirs(STORIES_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(SVG_TEMPLATES_DIR, exist_ok=True)

# Color palette for SVG backgrounds
COLOR_PALETTES = {
    "forest": ["#e8f5e9", "#c8e6c9", "#a5d6a7", "#81c784", "#66bb6a"],
    "ocean": ["#e3f2fd", "#bbdefb", "#90caf9", "#64b5f6", "#42a5f5"],
    "sunset": ["#fff8e1", "#ffecb3", "#ffe082", "#ffd54f", "#ffca28"],
    "fantasy": ["#f3e5f5", "#e1bee7", "#ce93d8", "#ba68c8", "#ab47bc"],
    "farm": ["#fffde7", "#fff9c4", "#fff59d", "#fff176", "#ffee58"]
}

# SVG templates for different story types
SVG_TEMPLATES = {
    "default": """
    <svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
        <rect width="800" height="600" fill="{bg_color}" />
        <text x="400" y="300" font-family="Arial" font-size="24" text-anchor="middle" fill="#333">{page_title}</text>
        <text x="400" y="340" font-family="Arial" font-size="18" text-anchor="middle" fill="#555">Page {page_number}</text>
    </svg>
    """,
    "forest": """
    <svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
        <rect width="800" height="600" fill="{bg_color}" />
        <circle cx="400" cy="300" r="150" fill="#4CAF50" opacity="0.2" />
        <path d="M300,400 Q400,300 500,400" stroke="#2E7D32" stroke-width="5" fill="none" />
        <text x="400" y="250" font-family="Arial" font-size="24" text-anchor="middle" fill="#333">{page_title}</text>
        <text x="400" y="480" font-family="Arial" font-size="18" text-anchor="middle" fill="#555">Page {page_number}</text>
    </svg>
    """,
    "animal": """
    <svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
        <rect width="800" height="600" fill="{bg_color}" />
        <circle cx="400" cy="250" r="100" fill="#FFEB3B" opacity="0.3" />
        <circle cx="360" cy="230" r="15" fill="#333" />
        <circle cx="440" cy="230" r="15" fill="#333" />
        <path d="M350,290 Q400,330 450,290" stroke="#333" stroke-width="5" fill="none" />
        <text x="400" y="420" font-family="Arial" font-size="24" text-anchor="middle" fill="#333">{page_title}</text>
        <text x="400" y="460" font-family="Arial" font-size="18" text-anchor="middle" fill="#555">Page {page_number}</text>
    </svg>
    """
}

def get_svg_template(story_id):
    """Get an appropriate SVG template based on the story_id"""
    if "fox" in story_id or "bear" in story_id or "wild" in story_id:
        return SVG_TEMPLATES["animal"]
    elif "forest" in story_id or "tree" in story_id:
        return SVG_TEMPLATES["forest"]
    else:
        return SVG_TEMPLATES["default"]

def create_svg_illustration(story_id, page_number, page_title, template=None):
    """
    Create an SVG illustration for a story page
    
    Args:
        story_id (str): The ID of the story
        page_number (int): The page number
        page_title (str): Title or short description for the page
        template (str): Optional SVG template to use
        
    Returns:
        str: Path to the created SVG file
    """
    # Create directory for this story's images
    story_images_dir = os.path.join(IMAGES_DIR, story_id)
    os.makedirs(story_images_dir, exist_ok=True)
    
    # Choose a color palette based on the story_id
    if "fox" in story_id or "bear" in story_id or "wild" in story_id:
        palette = COLOR_PALETTES["forest"]
    elif "fish" in story_id or "duck" in story_id:
        palette = COLOR_PALETTES["ocean"]
    elif "peep" in story_id or "pig" in story_id:
        palette = COLOR_PALETTES["farm"]
    else:
        palette = random.choice(list(COLOR_PALETTES.values()))
    
    # Choose a background color from the palette
    bg_color = palette[page_number % len(palette)]
    
    # Use the specified template or get one based on the story_id
    svg_template = template or get_svg_template(story_id)
    
    # Fill in the template
    svg_content = svg_template.format(
        bg_color=bg_color,
        page_title=page_title,
        page_number=page_number
    )
    
    # Write the SVG file
    svg_file_path = os.path.join(story_images_dir, f"page{page_number}.svg")
    with open(svg_file_path, 'w') as f:
        f.write(svg_content)
    
    return svg_file_path

def split_text_into_pages(text, pages=3):
    """
    Split a story text into separate pages
    
    Args:
        text (str): The full story text
        pages (int): Number of pages to split into
        
    Returns:
        list: List of text segments for each page
    """
    # Split by sentences (simple version - a real app would use NLP)
    sentences = []
    # Split on periods, question marks, and exclamation points
    for part in text.replace('!', '.').replace('?', '.').split('.'):
        if part.strip():
            sentences.append(part.strip() + '.')
    
    # Group sentences into pages
    if not sentences:
        return []
    
    # Adjust page count if we have fewer sentences
    page_count = min(pages, len(sentences))
    sentences_per_page = max(1, len(sentences) // page_count)
    
    page_texts = []
    for i in range(0, len(sentences), sentences_per_page):
        page_sentences = sentences[i:i + sentences_per_page]
        page_texts.append(' '.join(page_sentences))
        
        # Stop if we've created enough pages
        if len(page_texts) >= page_count:
            # Add any remaining sentences to the last page
            if i + sentences_per_page < len(sentences):
                remaining = ' '.join(sentences[i + sentences_per_page:])
                page_texts[-1] = page_texts[-1] + ' ' + remaining
            break
    
    return page_texts

def create_story_json(story_id, title, text, pages=3):
    """
    Create a JSON file for a story with multiple pages
    
    Args:
        story_id (str): The ID of the story
        title (str): The title of the story
        text (str): The full text of the story
        pages (int): Number of pages to split the text into
        
    Returns:
        str: Path to the created JSON file
    """
    # Split the text into pages
    page_texts = split_text_into_pages(text, pages)
    
    # Create the story structure
    story_data = {
        "title": title,
        "author": "Children's Castle",
        "pages": []
    }
    
    # Generate pages with placeholder images and audio
    for i, page_text in enumerate(page_texts):
        page_number = i + 1
        page_summary = f"{title} - Part {page_number}"
        
        # Create SVG illustration
        svg_path = create_svg_illustration(story_id, page_number, page_summary)
        
        # Add page to story data
        story_data["pages"].append({
            "image": f"page{page_number}.svg",
            "text": page_text,
            "audio": None  # Will be filled in when audio is generated
        })
    
    # Write the JSON file
    json_file_path = os.path.join(STORIES_DIR, f"{story_id}.json")
    with open(json_file_path, 'w') as f:
        json.dump(story_data, f, indent=2)
    
    return json_file_path

def process_all_stories(page_count=3, force=False):
    """
    Process all stories from the natural_voice script
    
    Args:
        page_count (int): Number of pages to create for each story
        force (bool): Whether to overwrite existing files
        
    Returns:
        dict: Results of the processing
    """
    results = {}
    
    for story_id, story in stories.items():
        title = story.get('title', f"Story {story_id}")
        text = story.get('text', '')
        
        if not text:
            logger.warning(f"No text for story: {title}")
            results[story_id] = {"status": "skipped", "reason": "No text"}
            continue
        
        # Check if this story already exists
        json_path = os.path.join(STORIES_DIR, f"{story_id}.json")
        if os.path.exists(json_path) and not force:
            logger.info(f"Story already exists: {title}")
            results[story_id] = {"status": "skipped", "reason": "Already exists"}
            continue
        
        try:
            logger.info(f"Processing story: {title}")
            
            # Create the JSON file with pages
            json_file = create_story_json(story_id, title, text, page_count)
            
            # Check if all expected image files were created
            story_images_dir = os.path.join(IMAGES_DIR, story_id)
            expected_images = [f"page{i+1}.svg" for i in range(page_count)]
            missing_images = [img for img in expected_images 
                             if not os.path.exists(os.path.join(story_images_dir, img))]
            
            if missing_images:
                logger.warning(f"Some images are missing for {title}: {missing_images}")
                results[story_id] = {
                    "status": "partial",
                    "json_file": json_file,
                    "missing_images": missing_images
                }
            else:
                logger.info(f"Successfully created story: {title}")
                results[story_id] = {
                    "status": "success",
                    "json_file": json_file,
                    "pages": page_count
                }
                
        except Exception as e:
            logger.error(f"Error processing story {title}: {str(e)}")
            results[story_id] = {"status": "error", "error": str(e)}
    
    # Save the results
    with open('story_creation_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    return results

def create_svg_templates():
    """
    Create SVG templates for different story themes
    """
    os.makedirs(SVG_TEMPLATES_DIR, exist_ok=True)
    
    for name, template in SVG_TEMPLATES.items():
        with open(os.path.join(SVG_TEMPLATES_DIR, f"{name}_template.svg"), 'w') as f:
            # Use a placeholder for the template variables
            svg = template.format(bg_color="#f0f0f0", page_title="Template", page_number=1)
            f.write(svg)
    
    logger.info(f"Created {len(SVG_TEMPLATES)} SVG templates in {SVG_TEMPLATES_DIR}")

def main():
    """Main function to parse arguments and run story creation"""
    parser = argparse.ArgumentParser(description='Create multi-page stories from text')
    parser.add_argument('--story-id', type=str, help='Process a specific story by ID')
    parser.add_argument('--pages', type=int, default=3, help='Number of pages per story')
    parser.add_argument('--force', action='store_true', help='Overwrite existing files')
    parser.add_argument('--templates', action='store_true', help='Create SVG templates')
    
    args = parser.parse_args()
    
    if args.templates:
        create_svg_templates()
    
    if args.story_id:
        if args.story_id not in stories:
            logger.error(f"Story not found: {args.story_id}")
            return
        
        story = stories[args.story_id]
        logger.info(f"Processing single story: {story['title']}")
        
        create_story_json(
            args.story_id, 
            story['title'], 
            story['text'], 
            args.pages
        )
        
        logger.info(f"Completed processing {story['title']}")
        
    else:
        logger.info(f"Processing all stories with {args.pages} pages each")
        results = process_all_stories(args.pages, args.force)
        
        # Print summary
        success_count = sum(1 for r in results.values() if r['status'] == 'success')
        partial_count = sum(1 for r in results.values() if r['status'] == 'partial')
        skipped_count = sum(1 for r in results.values() if r['status'] == 'skipped')
        error_count = sum(1 for r in results.values() if r['status'] == 'error')
        
        logger.info(f"Processed {len(results)} stories:")
        logger.info(f"  Success: {success_count}")
        logger.info(f"  Partial: {partial_count}")
        logger.info(f"  Skipped: {skipped_count}")
        logger.info(f"  Errors: {error_count}")

if __name__ == "__main__":
    main()