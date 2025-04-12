#!/usr/bin/env python3
"""
Enhance story illustrations by incorporating diverse character elements.
This script modifies generated SVG illustrations to include diverse character
elements and enhance visual representation in the stories.
"""

import os
import re
import json
import base64
import logging
import argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Directory paths
STORIES_DIR = "static/stories"
IMAGES_DIR = "static/images/stories"
TEMPLATES_DIR = "static/images/templates"
ASSETS_DIR = "static/images/assets"

# Create directories if they don't exist
os.makedirs(ASSETS_DIR, exist_ok=True)

# Define character SVG elements for diverse representation
DIVERSE_CHARACTER_ELEMENTS = {
    "child_diverse": """
    <g transform="translate({x}, {y}) scale({scale})">
        <circle cx="50" cy="50" r="40" fill="#8D5524" />
        <circle cx="35" cy="40" r="5" fill="#333333" />
        <circle cx="65" cy="40" r="5" fill="#333333" />
        <path d="M40,60 Q50,70 60,60" stroke="#333333" stroke-width="3" fill="none" />
        <path d="M30,30 Q50,15 70,30" stroke="#333333" stroke-width="3" fill="none" />
    </g>
    """,
    "child_reader": """
    <g transform="translate({x}, {y}) scale({scale})">
        <circle cx="50" cy="50" r="40" fill="#8D5524" />
        <circle cx="35" cy="40" r="5" fill="#333333" />
        <circle cx="65" cy="40" r="5" fill="#333333" />
        <path d="M40,60 Q50,70 60,60" stroke="#333333" stroke-width="3" fill="none" />
        <rect x="20" y="90" width="60" height="40" fill="#3F51B5" />
        <rect x="25" y="95" width="50" height="30" fill="#FFF" />
    </g>
    """,
    "fox_character": """
    <g transform="translate({x}, {y}) scale({scale})">
        <path d="M50,20 L30,60 L70,60 Z" fill="#FF9800" />
        <circle cx="35" cy="45" r="5" fill="#333333" />
        <circle cx="65" cy="45" r="5" fill="#333333" />
        <path d="M45,55 Q50,60 55,55" stroke="#333333" stroke-width="2" fill="none" />
        <path d="M30,30 L20,10 L25,30 Z" fill="#FF9800" />
        <path d="M70,30 L80,10 L75,30 Z" fill="#FF9800" />
        <path d="M50,60 L40,80 L60,80 Z" fill="#FF9800" />
    </g>
    """,
    "bear_character": """
    <g transform="translate({x}, {y}) scale({scale})">
        <circle cx="50" cy="50" r="40" fill="#795548" />
        <circle cx="30" cy="40" r="10" fill="#5D4037" />
        <circle cx="70" cy="40" r="10" fill="#5D4037" />
        <circle cx="35" cy="40" r="3" fill="#333333" />
        <circle cx="65" cy="40" r="3" fill="#333333" />
        <ellipse cx="50" cy="55" rx="10" ry="5" fill="#5D4037" />
        <path d="M40,55 Q50,65 60,55" stroke="#333333" stroke-width="2" fill="none" />
    </g>
    """
}

def process_image_for_svg(image_path, output_size=(200, 200), output_format="png"):
    """
    Process an image for inclusion in SVG (resizing, etc.)
    
    Args:
        image_path (str): Path to the source image
        output_size (tuple): Desired output size (width, height)
        output_format (str): Output format ('png' or 'jpg')
        
    Returns:
        str: Base64-encoded image data
    """
    try:
        img = Image.open(image_path)
        
        # Resize the image
        img = img.resize(output_size, Image.Resampling.LANCZOS)
        
        # Create an in-memory file
        from io import BytesIO
        buffer = BytesIO()
        
        # Save the image to the buffer
        img.save(buffer, format=output_format.upper())
        
        # Get the base64-encoded data
        img_data = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        mime_type = f"image/{output_format.lower()}"
        return f"data:{mime_type};base64,{img_data}"
        
    except Exception as e:
        logger.error(f"Error processing image {image_path}: {str(e)}")
        return None

def enhance_svg(svg_path, character_elements=None, position=(400, 300), scale=1.0):
    """
    Enhance an SVG with character elements
    
    Args:
        svg_path (str): Path to the SVG file
        character_elements (list): List of character element keys to add
        position (tuple): Position to place the character element (x, y)
        scale (float): Scale of the character element
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Read the SVG file
        with open(svg_path, 'r') as f:
            svg_content = f.read()
        
        # Check if SVG already has a closing tag
        if '</svg>' not in svg_content:
            logger.error(f"Invalid SVG file: {svg_path}")
            return False
        
        # Choose a character element if none provided
        if not character_elements:
            # Default to diverse child character
            character_elements = ['child_diverse']
        
        # Build the new elements to insert
        new_elements = []
        for element_key in character_elements:
            if element_key in DIVERSE_CHARACTER_ELEMENTS:
                # Calculate x and y position with some randomness
                x, y = position
                x += (hash(svg_path) % 100) - 50  # Add some randomness
                y += (hash(svg_path + element_key) % 60) - 30
                
                element = DIVERSE_CHARACTER_ELEMENTS[element_key].format(
                    x=x, y=y, scale=scale
                )
                new_elements.append(element)
        
        # Insert the new elements before the closing SVG tag
        modified_svg = svg_content.replace('</svg>', ''.join(new_elements) + '</svg>')
        
        # Write the modified SVG back to the file
        with open(svg_path, 'w') as f:
            f.write(modified_svg)
        
        logger.info(f"Enhanced SVG: {svg_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error enhancing SVG {svg_path}: {str(e)}")
        return False

def add_photo_to_svg(svg_path, photo_path, position=(50, 50), size=(150, 150)):
    """
    Add a photo to an SVG file using embedded base64 encoding
    
    Args:
        svg_path (str): Path to the SVG file
        photo_path (str): Path to the photo
        position (tuple): Position to place the photo (x, y)
        size (tuple): Size of the photo in the SVG
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Process the image
        img_data = process_image_for_svg(photo_path, output_size=size)
        if not img_data:
            return False
        
        # Create the image element
        x, y = position
        width, height = size
        image_element = f"""
        <image x="{x}" y="{y}" width="{width}" height="{height}"
               href="{img_data}" />
        """
        
        # Read the SVG file
        with open(svg_path, 'r') as f:
            svg_content = f.read()
        
        # Insert the image element before the closing SVG tag
        modified_svg = svg_content.replace('</svg>', image_element + '</svg>')
        
        # Write the modified SVG back to the file
        with open(svg_path, 'w') as f:
            f.write(modified_svg)
        
        logger.info(f"Added photo to SVG: {svg_path}")
        return True
        
    except Exception as e:
        logger.error(f"Error adding photo to SVG {svg_path}: {str(e)}")
        return False

def get_character_for_story(story_id):
    """
    Determine which character elements to use based on the story ID
    
    Args:
        story_id (str): The ID of the story
        
    Returns:
        list: List of character element keys to use
    """
    if "fox" in story_id:
        return ["fox_character"]
    elif "bear" in story_id:
        return ["bear_character"]
    elif "pig" in story_id:
        return ["fox_character", "child_diverse"]  # Mix characters
    else:
        return ["child_diverse"]

def process_story_illustrations(story_id, photo_path=None):
    """
    Process all illustrations for a given story
    
    Args:
        story_id (str): The ID of the story
        photo_path (str): Optional path to a photo to include
        
    Returns:
        dict: Results of the processing
    """
    story_dir = os.path.join(IMAGES_DIR, story_id)
    if not os.path.exists(story_dir):
        logger.error(f"Story directory not found: {story_dir}")
        return {"status": "error", "message": "Story directory not found"}
    
    # Get all SVG files in the story directory
    svg_files = [f for f in os.listdir(story_dir) if f.endswith('.svg')]
    
    if not svg_files:
        logger.warning(f"No SVG files found for story: {story_id}")
        return {"status": "warning", "message": "No SVG files found"}
    
    results = {}
    character_elements = get_character_for_story(story_id)
    
    for svg_file in svg_files:
        svg_path = os.path.join(story_dir, svg_file)
        
        # Get page number from filename
        match = re.search(r'page(\d+)\.svg', svg_file)
        if not match:
            logger.warning(f"Couldn't determine page number for: {svg_file}")
            page_num = 0
        else:
            page_num = int(match.group(1))
        
        # Different character positions for variety
        position = (400, 300)  # Default center position
        scale = 1.0
        
        # Page-specific adjustments
        if page_num == 1:
            # First page - center character
            position = (400, 350)
            scale = 1.5
        elif page_num % 2 == 0:
            # Even pages - right side
            position = (600, 300)
            scale = 1.2
        else:
            # Odd pages - left side
            position = (200, 300)
            scale = 1.2
        
        # Enhance the SVG
        success = enhance_svg(svg_path, character_elements, position, scale)
        
        # Add photo to the first page if provided
        if photo_path and page_num == 1:
            photo_position = (50, 50)
            photo_size = (150, 150)
            add_photo_to_svg(svg_path, photo_path, photo_position, photo_size)
        
        results[svg_file] = {
            "status": "enhanced" if success else "error",
            "character": character_elements
        }
    
    return results

def process_all_stories(photo_path=None):
    """
    Process illustrations for all stories
    
    Args:
        photo_path (str): Optional path to a photo to include
        
    Returns:
        dict: Results of the processing
    """
    if not os.path.exists(IMAGES_DIR):
        logger.error(f"Images directory not found: {IMAGES_DIR}")
        return {"status": "error", "message": "Images directory not found"}
    
    # Get all story directories
    story_dirs = [d for d in os.listdir(IMAGES_DIR) 
                 if os.path.isdir(os.path.join(IMAGES_DIR, d))]
    
    if not story_dirs:
        logger.warning("No story directories found")
        return {"status": "warning", "message": "No story directories found"}
    
    results = {}
    for story_id in story_dirs:
        logger.info(f"Processing illustrations for story: {story_id}")
        results[story_id] = process_story_illustrations(story_id, photo_path)
    
    # Save the results
    with open('illustration_enhancement_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    return results

def main():
    """Main function to parse arguments and run illustration enhancement"""
    parser = argparse.ArgumentParser(description='Enhance story illustrations')
    parser.add_argument('--story-id', type=str, help='Process a specific story by ID')
    parser.add_argument('--photo', type=str, help='Path to a photo to include in the illustrations')
    
    args = parser.parse_args()
    
    # Validate photo path if provided
    if args.photo and not os.path.exists(args.photo):
        logger.error(f"Photo not found: {args.photo}")
        return
    
    # Process a specific story if requested
    if args.story_id:
        logger.info(f"Processing illustrations for story: {args.story_id}")
        results = process_story_illustrations(args.story_id, args.photo)
        
        # Print summary
        success_count = sum(1 for r in results.values() if r['status'] == 'enhanced')
        error_count = sum(1 for r in results.values() if r['status'] == 'error')
        
        logger.info(f"Processed {len(results)} illustrations: {success_count} enhanced, {error_count} errors")
    else:
        # Process all stories
        logger.info("Processing illustrations for all stories")
        results = process_all_stories(args.photo)
        
        # Print summary
        story_count = len(results)
        illustration_count = sum(len(story_results) for story_results in results.values())
        
        logger.info(f"Processed {illustration_count} illustrations across {story_count} stories")

if __name__ == "__main__":
    main()