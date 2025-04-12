#!/usr/bin/env python3
"""
Master script to generate enhanced stories with audio.
This script orchestrates the entire process of:
1. Creating multi-page stories from text files
2. Enhancing story illustrations with diverse characters
3. Generating audio narration for each page using ElevenLabs
"""

import os
import sys
import logging
import argparse
import subprocess
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import necessary functions from other scripts
try:
    from create_story_pages import process_all_stories as create_all_stories
    from enhance_story_illustrations import process_all_stories as enhance_all_illustrations
    from generate_story_page_audio import process_all_stories as generate_all_audio
    from generate_elevenlabs_audio import initialize_elevenlabs
except ImportError as e:
    logger.error(f"Failed to import functions: {e}")
    logger.info("Running scripts as separate processes instead")

def run_script(script_name, args=None):
    """
    Run a Python script as a subprocess
    
    Args:
        script_name (str): Name of the script to run
        args (list): Arguments to pass to the script
        
    Returns:
        bool: True if successful, False otherwise
    """
    cmd = [sys.executable, script_name]
    if args:
        cmd.extend(args)
    
    logger.info(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        logger.info(f"Script output: {result.stdout.strip()}")
        if result.stderr:
            logger.warning(f"Script errors: {result.stderr.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Script failed with code {e.returncode}")
        logger.error(f"Output: {e.stdout}")
        logger.error(f"Error: {e.stderr}")
        return False

def run_step(step_name, script_name, args=None, direct_function=None, direct_args=None):
    """
    Run a step in the process, either via direct function call or subprocess
    
    Args:
        step_name (str): Name of the step for logging
        script_name (str): Name of the script to run
        args (list): Arguments to pass to the script
        direct_function (callable): Function to call directly instead of script
        direct_args (dict): Arguments to pass to the direct function
        
    Returns:
        bool: True if successful, False otherwise
    """
    logger.info(f"Starting step: {step_name}")
    
    success = False
    if direct_function and callable(direct_function):
        try:
            logger.info(f"Running function directly: {direct_function.__name__}")
            result = direct_function(**(direct_args or {}))
            success = True
        except Exception as e:
            logger.error(f"Function failed: {e}")
            success = False
    else:
        success = run_script(script_name, args)
    
    if success:
        logger.info(f"Completed step: {step_name}")
    else:
        logger.error(f"Failed step: {step_name}")
    
    return success

def process_story(story_id, pages=3, photo_path=None, force=False):
    """
    Process a single story through all steps
    
    Args:
        story_id (str): The ID of the story to process
        pages (int): Number of pages to create
        photo_path (str): Path to a photo to include
        force (bool): Force regeneration of existing files
        
    Returns:
        bool: True if all steps were successful
    """
    logger.info(f"Processing story: {story_id}")
    
    # Build command-line arguments for each script
    create_args = ["--story-id", story_id, "--pages", str(pages)]
    if force:
        create_args.append("--force")
    
    enhance_args = ["--story-id", story_id]
    if photo_path:
        enhance_args.extend(["--photo", photo_path])
    
    audio_args = ["--story-id", story_id]
    if force:
        audio_args.append("--force")
    
    # Run each step in sequence
    create_success = run_step(
        "Create story pages", 
        "create_story_pages.py", 
        create_args
    )
    
    if not create_success:
        logger.error(f"Failed to create story pages for {story_id}")
        return False
    
    enhance_success = run_step(
        "Enhance illustrations", 
        "enhance_story_illustrations.py", 
        enhance_args
    )
    
    if not enhance_success:
        logger.warning(f"Failed to enhance illustrations for {story_id}")
        # Continue anyway since this is not critical
    
    audio_success = run_step(
        "Generate audio", 
        "generate_story_page_audio.py", 
        audio_args
    )
    
    if not audio_success:
        logger.error(f"Failed to generate audio for {story_id}")
        return False
    
    logger.info(f"Successfully processed story: {story_id}")
    return True

def process_all(pages=3, photo_path=None, force=False):
    """
    Process all stories through all steps
    
    Args:
        pages (int): Number of pages to create
        photo_path (str): Path to a photo to include
        force (bool): Force regeneration of existing files
        
    Returns:
        bool: True if all steps were successful
    """
    logger.info("Processing all stories")
    
    # Build command-line arguments for each script
    create_args = ["--pages", str(pages)]
    if force:
        create_args.append("--force")
    
    enhance_args = []
    if photo_path:
        enhance_args.extend(["--photo", photo_path])
    
    audio_args = []
    if force:
        audio_args.append("--force")
    
    # Run each step in sequence for all stories
    create_success = run_step(
        "Create all story pages", 
        "create_story_pages.py", 
        create_args
    )
    
    if not create_success:
        logger.error("Failed to create story pages")
        return False
    
    enhance_success = run_step(
        "Enhance all illustrations", 
        "enhance_story_illustrations.py", 
        enhance_args
    )
    
    if not enhance_success:
        logger.warning("Failed to enhance illustrations")
        # Continue anyway since this is not critical
    
    audio_success = run_step(
        "Generate all audio", 
        "generate_story_page_audio.py", 
        audio_args
    )
    
    if not audio_success:
        logger.error("Failed to generate audio")
        return False
    
    logger.info("Successfully processed all stories")
    return True

def check_elevenlabs_api():
    """
    Check if the ElevenLabs API key is set and valid
    
    Returns:
        bool: True if the API key is valid
    """
    try:
        # Try to import and initialize the ElevenLabs API
        return initialize_elevenlabs()
    except Exception as e:
        logger.error(f"Failed to initialize ElevenLabs API: {e}")
        return False

def main():
    """Main function to parse arguments and run the enhancement process"""
    parser = argparse.ArgumentParser(description='Generate enhanced stories with audio')
    parser.add_argument('--story-id', type=str, help='Process a specific story by ID')
    parser.add_argument('--pages', type=int, default=3, help='Number of pages per story')
    parser.add_argument('--photo', type=str, help='Path to a photo to include in illustrations')
    parser.add_argument('--force', action='store_true', help='Force regeneration of existing files')
    
    args = parser.parse_args()
    
    # Check if ElevenLabs API key is configured
    if not check_elevenlabs_api():
        logger.error("ElevenLabs API key not configured or invalid")
        logger.error("Please check your ELEVENLABS_API_KEY environment variable")
        return
    
    # Create necessary directories
    os.makedirs("static/stories", exist_ok=True)
    os.makedirs("static/images/stories", exist_ok=True)
    os.makedirs("static/audio", exist_ok=True)
    
    # Validate photo path if provided
    if args.photo and not os.path.exists(args.photo):
        logger.error(f"Photo not found: {args.photo}")
        return
    
    # Process a specific story or all stories
    if args.story_id:
        success = process_story(args.story_id, args.pages, args.photo, args.force)
    else:
        success = process_all(args.pages, args.photo, args.force)
    
    if success:
        logger.info("Story enhancement completed successfully!")
    else:
        logger.error("Story enhancement process failed")

if __name__ == "__main__":
    main()