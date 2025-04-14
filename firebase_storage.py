"""
Firebase Storage integration for Children's Castle application.
This module provides helper functions to store, retrieve, and manage photos in Firebase Storage.
"""
import os
import uuid
import tempfile
import logging
from datetime import datetime
from io import BytesIO

import firebase_admin
from firebase_admin import credentials, storage
from PIL import Image

# Initialize Firebase Admin SDK if not already initialized
if not firebase_admin._apps:
    try:
        # Use environment variables for Firebase credentials
        project_id = os.environ.get('FIREBASE_PROJECT_ID')
        
        # Use application default credentials 
        # (which will work in both local development and Cloud Run)
        firebase_admin.initialize_app(options={
            'projectId': project_id,
            'storageBucket': f"{project_id}.appspot.com"
        })
        
        print(f"Firebase Storage initialized for project: {project_id}")
    except Exception as e:
        logging.error(f"Error initializing Firebase Admin SDK: {e}")
        print(f"Error initializing Firebase Storage: {e}")

def get_storage_bucket():
    """Get Firebase Storage bucket"""
    try:
        bucket = storage.bucket()
        return bucket
    except Exception as e:
        logging.error(f"Error getting storage bucket: {e}")
        return None

def upload_photo_to_firebase(file_data, original_filename, photo_id):
    """
    Upload a photo to Firebase Storage
    
    Args:
        file_data: File-like object or bytes of the image
        original_filename: Original filename
        photo_id: ID to use for the storage path
        
    Returns:
        tuple: (storage_path, public_url, thumbnail_path, thumbnail_url)
    """
    bucket = get_storage_bucket()
    if not bucket:
        raise Exception("Firebase Storage not initialized")
        
    # Generate a unique filename
    file_ext = original_filename.rsplit('.', 1)[1].lower() if '.' in original_filename else 'jpg'
    storage_filename = f"{photo_id}.{file_ext}"
    thumbnail_filename = f"{photo_id}_thumb.{file_ext}"
    
    # Set paths in Firebase Storage
    storage_path = f"photos/{storage_filename}"
    thumbnail_path = f"photos/thumbnails/{thumbnail_filename}"
    
    # If file_data is a file-like object, read it
    if hasattr(file_data, 'read'):
        file_bytes = file_data.read()
    else:
        file_bytes = file_data
        
    # Upload original file
    blob = bucket.blob(storage_path)
    blob.upload_from_string(
        file_bytes,
        content_type=f"image/{file_ext}"
    )
    
    # Make file publicly accessible with the proper CORS settings
    blob.make_public()
    public_url = blob.public_url
    
    # Create and upload thumbnail
    try:
        image = Image.open(BytesIO(file_bytes))
        image.thumbnail((300, 300))
        
        thumb_bytes = BytesIO()
        image.save(thumb_bytes, format=image.format)
        thumb_bytes.seek(0)
        
        thumb_blob = bucket.blob(thumbnail_path)
        thumb_blob.upload_from_string(
            thumb_bytes.read(),
            content_type=f"image/{file_ext}"
        )
        
        # Make thumbnail publicly accessible
        thumb_blob.make_public()
        thumbnail_url = thumb_blob.public_url
    except Exception as e:
        logging.error(f"Error creating thumbnail: {e}")
        thumbnail_url = public_url  # Use original as fallback
        
    return storage_path, public_url, thumbnail_path, thumbnail_url

def delete_photo_from_firebase(storage_path, thumbnail_path=None):
    """
    Delete a photo from Firebase Storage
    
    Args:
        storage_path: Path in Firebase Storage
        thumbnail_path: Path to thumbnail in Firebase Storage (optional)
        
    Returns:
        bool: Success status
    """
    bucket = get_storage_bucket()
    if not bucket:
        return False
        
    try:
        # Delete original file
        blob = bucket.blob(storage_path)
        blob.delete()
        
        # Delete thumbnail if provided
        if thumbnail_path:
            thumb_blob = bucket.blob(thumbnail_path)
            thumb_blob.delete()
            
        return True
    except Exception as e:
        logging.error(f"Error deleting from Firebase Storage: {e}")
        return False

def get_firebase_photo_url(storage_path):
    """
    Get the public URL for a photo in Firebase Storage
    
    Args:
        storage_path: Path in Firebase Storage
        
    Returns:
        str: Public URL
    """
    bucket = get_storage_bucket()
    if not bucket:
        return None
        
    try:
        blob = bucket.blob(storage_path)
        blob.make_public()  # Ensure it's publicly accessible
        return blob.public_url
    except Exception as e:
        logging.error(f"Error getting Firebase Storage URL: {e}")
        return None