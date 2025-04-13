"""
Photo management routes for Children's Castle application.
This module provides routes for uploading, viewing, and managing photos.
"""
import os
import uuid
import datetime
import secrets
from PIL import Image
from io import BytesIO
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app, send_file, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from sqlalchemy import desc
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

from models import db, Photo, Parent, Child

# Create a blueprint for photos
photo_routes = Blueprint('photos', __name__, url_prefix='/photos')

# Constants
UPLOAD_FOLDER = 'static/uploads/photos'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Forms
class PhotoUploadForm(FlaskForm):
    """Form for uploading a photo"""
    photo = FileField('Photo', validators=[
        FileRequired(),
        FileAllowed(list(ALLOWED_EXTENSIONS), 'Images only!')
    ])
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    tags = StringField('Tags', validators=[Optional(), Length(max=200)])
    is_private = BooleanField('Private', default=True)
    submit = SubmitField('Upload')


def allowed_file(filename):
    """Check if filename has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def has_access_to_photo(photo):
    """Check if current user has access to a photo"""
    # Admin access (for future use)
    if hasattr(current_user, 'is_admin') and current_user.is_admin:
        return True
    
    # Parent access to their own photos
    if hasattr(current_user, 'type') and current_user.type == 'parent':
        # Parent's own photos
        if photo.parent_id == current_user.id:
            return True
        
        # Photos from their children
        if photo.child_id and Child.query.filter_by(id=photo.child_id, parent_id=current_user.id).first():
            return True
    
    # Child access to their own photos and parent's photos
    if hasattr(current_user, 'type') and current_user.type == 'child':
        # Child's own photos
        if photo.child_id == current_user.id:
            return True
        
        # Photos from their parent
        if photo.parent_id == current_user.parent_id:
            return True
    
    # Private photos are restricted to owner and linked parent/child
    if photo.is_private:
        if photo.parent_id and photo.parent_id == current_user.id:
            return True
        if photo.child_id and photo.child_id == current_user.id:
            return True
        if hasattr(current_user, 'parent_id') and photo.parent_id == current_user.parent_id:
            return True
        if hasattr(current_user, 'type') and current_user.type == 'parent':
            # Check if photo belongs to one of the parent's children
            if photo.child_id and Child.query.filter_by(id=photo.child_id, parent_id=current_user.id).first():
                return True
    else:
        # Non-private photos are visible to family members
        # For a future family sharing model
        return True
    
    return False


@photo_routes.route('/')
@login_required
def photos_dashboard():
    """Photo gallery dashboard"""
    # Get filters from query parameters
    owner_filter = request.args.get('owner', 'all')
    privacy_filter = request.args.get('privacy', 'all')
    sort_by = request.args.get('sort', 'date_desc')
    search_query = request.args.get('search', '')
    
    # Base query
    query = Photo.query
    
    # Owner filter
    if owner_filter == 'mine':
        if hasattr(current_user, 'type') and current_user.type == 'parent':
            query = query.filter(Photo.parent_id == current_user.id)
        else:
            query = query.filter(Photo.child_id == current_user.id)
    elif owner_filter == 'family':
        if hasattr(current_user, 'type') and current_user.type == 'parent':
            # Get all children IDs for this parent
            child_ids = [child.id for child in Child.query.filter_by(parent_id=current_user.id).all()]
            query = query.filter((Photo.parent_id == current_user.id) | 
                                (Photo.child_id.in_(child_ids)))
        else:
            # Child viewing family photos (their own and parent's)
            query = query.filter((Photo.child_id == current_user.id) | 
                                (Photo.parent_id == current_user.parent_id))
    
    # Privacy filter
    if privacy_filter == 'private':
        query = query.filter(Photo.is_private == True)
    elif privacy_filter == 'shared':
        query = query.filter(Photo.is_private == False)
    
    # Search by title, description or tags
    if search_query:
        search_terms = f"%{search_query}%"
        query = query.filter((Photo.title.ilike(search_terms)) | 
                            (Photo.description.ilike(search_terms)) | 
                            (Photo.tags.ilike(search_terms)))
    
    # Apply sorting
    if sort_by == 'date_asc':
        query = query.order_by(Photo.uploaded_at.asc())
    elif sort_by == 'date_desc':
        query = query.order_by(Photo.uploaded_at.desc())
    elif sort_by == 'title_asc':
        query = query.order_by(Photo.title.asc())
    elif sort_by == 'title_desc':
        query = query.order_by(Photo.title.desc())
    elif sort_by == 'favorites':
        query = query.filter(Photo.is_favorite == True).order_by(Photo.uploaded_at.desc())
    
    # Get photos
    photos = query.all()
    
    # Filter by access permission (security layer)
    photos = [photo for photo in photos if has_access_to_photo(photo)]
    
    # Render template
    return render_template('photos/dashboard.html', 
                          photos=photos,
                          owner_filter=owner_filter,
                          privacy_filter=privacy_filter,
                          sort_by=sort_by,
                          search_query=search_query)


@photo_routes.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_photo():
    """Upload a new photo"""
    form = PhotoUploadForm()
    
    if form.validate_on_submit():
        photo_file = form.photo.data
        
        # Check if file is allowed
        if not allowed_file(photo_file.filename):
            flash('File type not allowed. Please upload a JPG, PNG, or GIF image.', 'error')
            return redirect(request.url)
        
        # Check file size
        if len(photo_file.read()) > MAX_FILE_SIZE:
            photo_file.seek(0)  # Reset file pointer
            flash('File is too large. Maximum size is 10MB.', 'error')
            return redirect(request.url)
        
        # Reset file pointer
        photo_file.seek(0)
        
        # Generate a secure filename with UUID
        original_filename = secure_filename(photo_file.filename)
        file_ext = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}.{file_ext}"
        
        # Create file path
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
        
        # Get file size
        photo_file.seek(0, os.SEEK_END)
        file_size = photo_file.tell()
        photo_file.seek(0)
        
        # Save the file
        photo_file.save(filepath)
        
        # Create thumbnail
        try:
            with Image.open(filepath) as img:
                img.thumbnail((300, 300))
                thumb_filename = f"thumb_{unique_filename}"
                thumb_path = os.path.join(UPLOAD_FOLDER, thumb_filename)
                img.save(thumb_path)
        except Exception as e:
            # If thumbnail creation fails, continue without it
            thumb_filename = None
            print(f"Error creating thumbnail: {e}")
        
        # Create database entry
        photo = Photo(
            filename=unique_filename,
            thumbnail_filename=thumb_filename,
            original_filename=original_filename,
            file_size=file_size,
            file_type=file_ext,
            title=form.title.data,
            description=form.description.data,
            tags=form.tags.data,
            is_private=form.is_private.data
        )
        
        # Set owner based on user type
        if hasattr(current_user, 'type') and current_user.type == 'parent':
            photo.parent_id = current_user.id
        else:
            photo.child_id = current_user.id
        
        # Save to database
        db.session.add(photo)
        db.session.commit()
        
        flash('Photo uploaded successfully!', 'success')
        return redirect(url_for('photos.photos_dashboard'))
    
    return render_template('photos/upload.html', form=form)


@photo_routes.route('/view/<int:photo_id>')
@login_required
def view_photo(photo_id):
    """View a single photo"""
    photo = Photo.query.get_or_404(photo_id)
    
    # Check access permission
    if not has_access_to_photo(photo):
        flash('You do not have permission to view this photo.', 'error')
        return redirect(url_for('photos.photos_dashboard'))
    
    return render_template('photos/view.html', photo=photo)


@photo_routes.route('/get-photo/<int:photo_id>')
@login_required
def get_raw_photo(photo_id):
    """Get the raw photo file (with proper access control)"""
    photo = Photo.query.get_or_404(photo_id)
    
    # Check access permission
    if not has_access_to_photo(photo):
        abort(403)
    
    # Full-size image by default, thumbnail if requested
    use_thumbnail = request.args.get('thumbnail', '').lower() == 'true'
    
    # Determine file path
    if use_thumbnail and photo.thumbnail_filename:
        filepath = os.path.join(UPLOAD_FOLDER, photo.thumbnail_filename)
    else:
        filepath = os.path.join(UPLOAD_FOLDER, photo.filename)
    
    # Check if file exists
    if not os.path.isfile(filepath):
        abort(404)
    
    # Send the file
    return send_file(filepath, mimetype=f'image/{photo.file_type}')


@photo_routes.route('/update/<int:photo_id>', methods=['POST'])
@login_required
def update_photo(photo_id):
    """Update photo details"""
    photo = Photo.query.get_or_404(photo_id)
    
    # Check ownership
    if (photo.parent_id and photo.parent_id != current_user.id) and \
       (photo.child_id and photo.child_id != current_user.id):
        return jsonify({'success': False, 'error': 'You do not have permission to edit this photo.'}), 403
    
    # Get data from request
    data = request.json
    
    # Update fields
    if 'title' in data:
        photo.title = data['title']
    
    if 'description' in data:
        photo.description = data['description']
    
    if 'tags' in data:
        photo.tags = data['tags']
    
    if 'is_private' in data:
        photo.is_private = data['is_private']
    
    # Save changes
    db.session.commit()
    
    return jsonify({'success': True})


@photo_routes.route('/toggle-favorite/<int:photo_id>', methods=['POST'])
@login_required
def toggle_favorite(photo_id):
    """Toggle favorite status for a photo"""
    photo = Photo.query.get_or_404(photo_id)
    
    # Check access permission
    if not has_access_to_photo(photo):
        return jsonify({'success': False, 'error': 'You do not have permission to access this photo.'}), 403
    
    # Toggle favorite status
    photo.is_favorite = not photo.is_favorite
    db.session.commit()
    
    return jsonify({
        'success': True,
        'is_favorite': photo.is_favorite
    })


@photo_routes.route('/delete/<int:photo_id>', methods=['POST'])
@login_required
def delete_photo(photo_id):
    """Delete a photo"""
    photo = Photo.query.get_or_404(photo_id)
    
    # Check ownership (only owner can delete)
    if (photo.parent_id and photo.parent_id != current_user.id) and \
       (photo.child_id and photo.child_id != current_user.id):
        return jsonify({'success': False, 'error': 'You do not have permission to delete this photo.'}), 403
    
    # Delete files
    try:
        # Delete main file
        filepath = os.path.join(UPLOAD_FOLDER, photo.filename)
        if os.path.isfile(filepath):
            os.remove(filepath)
        
        # Delete thumbnail if it exists
        if photo.thumbnail_filename:
            thumb_path = os.path.join(UPLOAD_FOLDER, photo.thumbnail_filename)
            if os.path.isfile(thumb_path):
                os.remove(thumb_path)
    except Exception as e:
        print(f"Error deleting files: {e}")
    
    # Delete database entry
    db.session.delete(photo)
    db.session.commit()
    
    return jsonify({'success': True})