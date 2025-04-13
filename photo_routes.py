"""
Photo management routes for Children's Castle
Allows secure photo uploads, viewing, and sharing between children and parents.
"""
import os
import secrets
from datetime import datetime
from PIL import Image
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, send_file
from flask import current_app as app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import jwt

from models import db, Photo, Parent, Child
from app import csrf

# Create blueprint
photo_routes = Blueprint('photos', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(original_filename):
    """Generate a secure, unique filename"""
    # First secure the filename to remove potentially dangerous characters
    filename = secure_filename(original_filename)
    # Add timestamp and random token to make it unique
    random_hex = secrets.token_hex(8)
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    _, file_ext = os.path.splitext(filename)
    return f"{timestamp}_{random_hex}{file_ext}"

def save_and_resize_image(file, filename, max_size=(1200, 1200)):
    """
    Save the uploaded image and create a thumbnail version
    Returns file path and size
    """
    # Create upload directory if it doesn't exist
    upload_folder = os.path.join(app.static_folder, 'uploads', 'photos')
    os.makedirs(upload_folder, exist_ok=True)
    
    # Generate path for the full-size image
    file_path = os.path.join(upload_folder, filename)
    
    # Save the original file
    file.save(file_path)
    file_size = os.path.getsize(file_path)
    
    # Create a thumbnail
    try:
        with Image.open(file_path) as img:
            # Resize if needed
            if img.height > max_size[1] or img.width > max_size[0]:
                img.thumbnail(max_size)
                img.save(file_path)
    except Exception as e:
        app.logger.error(f"Error resizing image: {str(e)}")
    
    return file_path, file_size

@photo_routes.route('/photos')
@login_required
def photos_dashboard():
    """Main photos dashboard"""
    user_type = getattr(current_user, 'role', None)
    
    # Get photos based on user type
    if user_type == 'parent':
        # For parents, show their photos and all photos from their children
        parent_photos = Photo.query.filter_by(parent_id=current_user.id).all()
        
        # Get all children for this parent
        children = Child.query.filter_by(parent_id=current_user.id).all()
        child_ids = [child.id for child in children]
        
        # Get photos from all children
        children_photos = Photo.query.filter(Photo.child_id.in_(child_ids)).all()
        
        # Combine the two lists
        photos = parent_photos + children_photos
        
    elif user_type == 'child':
        # For children, show only their photos
        photos = Photo.query.filter_by(child_id=current_user.id).all()
        
        # Also get parent's photos, but only if they're marked as shared
        parent = Parent.query.get(current_user.parent_id)
        if parent:
            parent_photos = Photo.query.filter_by(
                parent_id=parent.id, 
                is_private=False
            ).all()
            photos += parent_photos
    else:
        # Guest users or unrecognized roles get an empty list
        photos = []
    
    return render_template('photos/dashboard.html', 
                          photos=photos, 
                          user_type=user_type)

@photo_routes.route('/photos/upload', methods=['GET', 'POST'])
@login_required
def upload_photo():
    """Upload a new photo"""
    if request.method == 'POST':
        # Check if a file was uploaded
        if 'photo' not in request.files:
            flash('No file part', 'error')
            return redirect(request.url)
        
        file = request.files['photo']
        
        # Check if the filename is empty
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(request.url)
        
        # Check file type
        if not allowed_file(file.filename):
            flash(f'File type not allowed. Please upload: {", ".join(ALLOWED_EXTENSIONS)}', 'error')
            return redirect(request.url)
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            flash(f'File too large. Maximum size is {MAX_FILE_SIZE/1024/1024}MB', 'error')
            return redirect(request.url)
        
        # Generate a secure filename
        filename = generate_unique_filename(file.filename)
        
        # Save and resize the image
        file_path, file_size = save_and_resize_image(file, filename)
        
        # Create the database record
        photo = Photo(
            filename=filename,
            original_filename=file.filename,
            file_path=file_path,
            file_size=file_size,
            mime_type=file.content_type,
            title=request.form.get('title', ''),
            description=request.form.get('description', ''),
            tags=request.form.get('tags', ''),
            is_private=request.form.get('is_private', 'true') == 'true'
        )
        
        # Set the owner based on user type
        if getattr(current_user, 'role', None) == 'parent':
            photo.parent_id = current_user.id
        else:
            photo.child_id = current_user.id
        
        db.session.add(photo)
        db.session.commit()
        
        flash('Photo uploaded successfully!', 'success')
        return redirect(url_for('photos.photos_dashboard'))
    
    return render_template('photos/upload.html')

@photo_routes.route('/photos/view/<int:photo_id>')
@login_required
def view_photo(photo_id):
    """View a single photo with secure access control"""
    # Get the photo
    photo = Photo.query.get_or_404(photo_id)
    
    # Check if the user has permission to view this photo
    user_type = getattr(current_user, 'role', None)
    
    has_permission = False
    
    if user_type == 'parent':
        # Parents can view their own photos
        if photo.parent_id == current_user.id:
            has_permission = True
        # Parents can also view photos from their children
        elif photo.child_id:
            child = Child.query.get(photo.child_id)
            if child and child.parent_id == current_user.id:
                has_permission = True
    
    elif user_type == 'child':
        # Children can view their own photos
        if photo.child_id == current_user.id:
            has_permission = True
        # Children can view their parent's photos if they're not private
        elif photo.parent_id:
            parent = Parent.query.get(photo.parent_id)
            if parent and parent.id == current_user.parent_id and not photo.is_private:
                has_permission = True
    
    if not has_permission:
        flash('You do not have permission to view this photo', 'error')
        return redirect(url_for('photos.photos_dashboard'))
    
    # Serve the actual photo file
    return render_template('photos/view.html', photo=photo)

@photo_routes.route('/photos/raw/<int:photo_id>')
@login_required
def get_raw_photo(photo_id):
    """Serve the actual photo file with security checks"""
    # Get the photo
    photo = Photo.query.get_or_404(photo_id)
    
    # Check if the user has permission to view this photo
    user_type = getattr(current_user, 'role', None)
    
    has_permission = False
    
    if user_type == 'parent':
        # Parents can view their own photos
        if photo.parent_id == current_user.id:
            has_permission = True
        # Parents can also view photos from their children
        elif photo.child_id:
            child = Child.query.get(photo.child_id)
            if child and child.parent_id == current_user.id:
                has_permission = True
    
    elif user_type == 'child':
        # Children can view their own photos
        if photo.child_id == current_user.id:
            has_permission = True
        # Children can view their parent's photos if they're not private
        elif photo.parent_id:
            parent = Parent.query.get(photo.parent_id)
            if parent and parent.id == current_user.parent_id and not photo.is_private:
                has_permission = True
    
    if not has_permission:
        return jsonify({'error': 'Permission denied'}), 403
    
    # Serve the actual photo file
    return send_file(photo.file_path, mimetype=photo.mime_type)

@photo_routes.route('/photos/delete/<int:photo_id>', methods=['POST'])
@login_required
@csrf.exempt
def delete_photo(photo_id):
    """Delete a photo"""
    photo = Photo.query.get_or_404(photo_id)
    
    # Check if the user has permission to delete this photo
    user_type = getattr(current_user, 'role', None)
    
    has_permission = False
    
    if user_type == 'parent':
        # Parents can delete their own photos
        if photo.parent_id == current_user.id:
            has_permission = True
        # Parents can also delete photos from their children
        elif photo.child_id:
            child = Child.query.get(photo.child_id)
            if child and child.parent_id == current_user.id:
                has_permission = True
    
    elif user_type == 'child':
        # Children can only delete their own photos
        if photo.child_id == current_user.id:
            has_permission = True
    
    if not has_permission:
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    
    # Delete the actual file
    try:
        if os.path.exists(photo.file_path):
            os.remove(photo.file_path)
    except Exception as e:
        app.logger.error(f"Error deleting photo file: {str(e)}")
    
    # Delete from database
    db.session.delete(photo)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Photo deleted successfully'})

@photo_routes.route('/photos/toggle-favorite/<int:photo_id>', methods=['POST'])
@login_required
@csrf.exempt
def toggle_favorite(photo_id):
    """Toggle favorite status for a photo"""
    photo = Photo.query.get_or_404(photo_id)
    
    # Check if the user has permission
    user_type = getattr(current_user, 'role', None)
    
    has_permission = False
    
    if user_type == 'parent':
        # Parents can favorite their own photos
        if photo.parent_id == current_user.id:
            has_permission = True
        # Parents can also favorite photos from their children
        elif photo.child_id:
            child = Child.query.get(photo.child_id)
            if child and child.parent_id == current_user.id:
                has_permission = True
    
    elif user_type == 'child':
        # Children can only favorite their own photos
        if photo.child_id == current_user.id:
            has_permission = True
    
    if not has_permission:
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    
    # Toggle favorite status
    photo.is_favorite = not photo.is_favorite
    db.session.commit()
    
    return jsonify({
        'success': True, 
        'is_favorite': photo.is_favorite,
        'message': f"Photo {'added to' if photo.is_favorite else 'removed from'} favorites"
    })

@photo_routes.route('/photos/update/<int:photo_id>', methods=['POST'])
@login_required
@csrf.exempt
def update_photo(photo_id):
    """Update photo metadata"""
    photo = Photo.query.get_or_404(photo_id)
    
    # Check if the user has permission
    user_type = getattr(current_user, 'role', None)
    
    has_permission = False
    
    if user_type == 'parent':
        # Parents can update their own photos
        if photo.parent_id == current_user.id:
            has_permission = True
        # Parents can also update photos from their children
        elif photo.child_id:
            child = Child.query.get(photo.child_id)
            if child and child.parent_id == current_user.id:
                has_permission = True
    
    elif user_type == 'child':
        # Children can only update their own photos
        if photo.child_id == current_user.id:
            has_permission = True
    
    if not has_permission:
        return jsonify({'success': False, 'message': 'Permission denied'}), 403
    
    # Update photo data
    if 'title' in request.form:
        photo.title = request.form['title']
    
    if 'description' in request.form:
        photo.description = request.form['description']
    
    if 'tags' in request.form:
        photo.tags = request.form['tags']
    
    if 'is_private' in request.form:
        photo.is_private = request.form['is_private'] == 'true'
    
    photo.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Photo updated successfully'
    })