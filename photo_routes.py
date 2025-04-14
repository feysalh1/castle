"""
Photo management routes for Children's Castle application.
This module provides routes for uploading, viewing, and managing photos.
"""
import os
import uuid
import datetime
from datetime import datetime
import secrets
from PIL import Image
from io import BytesIO
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app, send_file, abort
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from sqlalchemy import desc, func, extract
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

from models import db, Photo, Parent, Child, PhotoAlbum, PhotoAlbumItem

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
    
    # Journal features
    journal_entry = TextAreaField('Journal Entry', validators=[Optional(), Length(max=2000)])
    mood = StringField('Mood', validators=[Optional(), Length(max=50)])
    journal_date = StringField('Journal Date', validators=[Optional()])
    
    # Album fields
    album_id = StringField('Album', validators=[Optional()])
    create_new_album = BooleanField('Create New Album', default=False)
    new_album_name = StringField('New Album Name', validators=[Optional(), Length(max=100)])
    
    submit = SubmitField('Upload')

class AlbumForm(FlaskForm):
    """Form for creating/editing an album"""
    name = StringField('Album Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    is_private = BooleanField('Private', default=True)
    submit = SubmitField('Save Album')


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
    view_type = request.args.get('view', 'photos')  # 'photos', 'albums', 'journal', 'calendar'
    mood_filter = request.args.get('mood', 'all')
    date_filter = request.args.get('date', '')
    album_id = request.args.get('album', '')
    
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
    
    # Mood filter
    if mood_filter != 'all':
        query = query.filter(Photo.mood == mood_filter)
    
    # Date filter (for journal or calendar view)
    if date_filter:
        try:
            # Parse YYYY-MM format for month view
            if len(date_filter) == 7:
                year, month = map(int, date_filter.split('-'))
                start_date = datetime(year, month, 1)
                # Get end of month
                if month == 12:
                    end_date = datetime(year + 1, 1, 1)
                else:
                    end_date = datetime(year, month + 1, 1)
                
                # Filter by month
                query = query.filter(
                    (extract('year', Photo.uploaded_at) == year) &
                    (extract('month', Photo.uploaded_at) == month)
                )
            # Parse YYYY-MM-DD format for day view
            elif len(date_filter) == 10:
                date_obj = datetime.strptime(date_filter, '%Y-%m-%d').date()
                query = query.filter(
                    (func.date(Photo.uploaded_at) == date_obj) |
                    (Photo.journal_date == date_obj)
                )
        except (ValueError, TypeError):
            # Invalid date format, ignore filter
            pass
    
    # Album filter
    if album_id and album_id.isdigit():
        album = PhotoAlbum.query.get(int(album_id))
        if album and has_access_to_album(album):
            # Get photos from this album
            photos_in_album = [item.photo_id for item in PhotoAlbumItem.query.filter_by(album_id=album.id).all()]
            query = query.filter(Photo.id.in_(photos_in_album))
    
    # Search by title, description or tags
    if search_query:
        search_terms = f"%{search_query}%"
        query = query.filter((Photo.title.ilike(search_terms)) | 
                            (Photo.description.ilike(search_terms)) | 
                            (Photo.tags.ilike(search_terms)) |
                            (Photo.journal_entry.ilike(search_terms)))
    
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
    
    # Get albums for album view or selection
    albums = []
    if view_type == 'albums' or view_type == 'photos':
        albums_query = PhotoAlbum.query
        
        # Filter albums by owner
        if hasattr(current_user, 'type') and current_user.type == 'parent':
            # Parent can see their own albums and their children's albums
            child_ids = [child.id for child in Child.query.filter_by(parent_id=current_user.id).all()]
            albums_query = albums_query.filter((PhotoAlbum.parent_id == current_user.id) | 
                                            (PhotoAlbum.child_id.in_(child_ids)))
        else:
            # Child can see their own albums and their parent's albums
            albums_query = albums_query.filter((PhotoAlbum.child_id == current_user.id) | 
                                             (PhotoAlbum.parent_id == current_user.parent_id))
        
        # Get albums
        albums = albums_query.all()
        
        # Filter by access permission
        albums = [album for album in albums if has_access_to_album(album)]
    
    # Get available moods for the filter
    available_moods = db.session.query(Photo.mood).filter(
        Photo.mood != None, 
        Photo.mood != ''
    ).distinct().all()
    available_moods = [mood[0] for mood in available_moods]
    
    # Organize photos by date for calendar/journal view
    photos_by_date = {}
    if view_type in ['calendar', 'journal']:
        for photo in photos:
            # Use journal_date if available, otherwise use uploaded_at
            date_key = photo.journal_date if photo.journal_date else photo.uploaded_at.date()
            
            if date_key not in photos_by_date:
                photos_by_date[date_key] = []
            
            photos_by_date[date_key].append(photo)
        
        # Sort dates
        photos_by_date = {k: photos_by_date[k] for k in sorted(photos_by_date.keys(), reverse=True)}
    
    # Render template
    return render_template('photos/dashboard.html', 
                          photos=photos,
                          albums=albums,
                          owner_filter=owner_filter,
                          privacy_filter=privacy_filter,
                          sort_by=sort_by,
                          search_query=search_query,
                          view_type=view_type,
                          mood_filter=mood_filter,
                          date_filter=date_filter,
                          album_id=album_id,
                          available_moods=available_moods,
                          photos_by_date=photos_by_date)
                          
                          
def has_access_to_album(album):
    """Check if current user has access to an album"""
    # Admin access (for future use)
    if hasattr(current_user, 'is_admin') and current_user.is_admin:
        return True
    
    # Parent access to their own albums
    if hasattr(current_user, 'type') and current_user.type == 'parent':
        # Parent's own albums
        if album.parent_id == current_user.id:
            return True
        
        # Albums from their children
        if album.child_id and Child.query.filter_by(id=album.child_id, parent_id=current_user.id).first():
            return True
    
    # Child access to their own albums and parent's albums
    if hasattr(current_user, 'type') and current_user.type == 'child':
        # Child's own albums
        if album.child_id == current_user.id:
            return True
        
        # Albums from their parent
        if album.parent_id == current_user.parent_id:
            return True
    
    # Private albums are restricted to owner and linked parent/child
    if album.is_private:
        if album.parent_id and album.parent_id == current_user.id:
            return True
        if album.child_id and album.child_id == current_user.id:
            return True
        if hasattr(current_user, 'parent_id') and album.parent_id == current_user.parent_id:
            return True
        if hasattr(current_user, 'type') and current_user.type == 'parent':
            # Check if album belongs to one of the parent's children
            if album.child_id and Child.query.filter_by(id=album.child_id, parent_id=current_user.id).first():
                return True
    else:
        # Non-private albums are visible to family members
        # For a future family sharing model
        return True
    
    return False


@photo_routes.route('/upload', methods=['GET', 'POST'])
@login_required
def upload_photo():
    """Upload a new photo"""
    form = PhotoUploadForm()
    
    # Get available albums for the current user
    if hasattr(current_user, 'type') and current_user.type == 'parent':
        # Parent's own albums and children's albums
        child_ids = [child.id for child in Child.query.filter_by(parent_id=current_user.id).all()]
        albums = PhotoAlbum.query.filter(
            (PhotoAlbum.parent_id == current_user.id) | 
            (PhotoAlbum.child_id.in_(child_ids))
        ).all()
    else:
        # Child's own albums and parent's albums
        albums = PhotoAlbum.query.filter(
            (PhotoAlbum.child_id == current_user.id) | 
            (PhotoAlbum.parent_id == current_user.parent_id)
        ).all()
    
    # Get today's date for the journal date field
    today_date = datetime.now().strftime('%Y-%m-%d')
    
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
            # Add Firebase storage fields if applicable
            storage_type=storage_type,
            firebase_storage_path=firebase_storage_path,
            firebase_thumbnail_path=firebase_thumbnail_path,
            firebase_url=firebase_url,
            firebase_thumbnail_url=firebase_thumbnail_url,
            description=form.description.data,
            tags=form.tags.data,
            is_private=form.is_private.data,
            # Journal features
            journal_entry=form.journal_entry.data,
            mood=form.mood.data
        )
        
        # Handle journal date if provided
        if form.journal_date.data:
            try:
                journal_date = datetime.strptime(form.journal_date.data, '%Y-%m-%d').date()
                photo.journal_date = journal_date
            except ValueError:
                # If date format is invalid, use today's date
                photo.journal_date = datetime.now().date()
        
        # Set owner based on user type
        if hasattr(current_user, 'type') and current_user.type == 'parent':
            photo.parent_id = current_user.id
        else:
            photo.child_id = current_user.id
        
        # Save to database
        db.session.add(photo)
        db.session.commit()
        
        # Handle album selection or creation
        if form.create_new_album.data and form.new_album_name.data:
            # Create a new album
            album = PhotoAlbum(
                name=form.new_album_name.data,
                description=f"Album created from photo: {photo.title}",
                is_private=form.is_private.data,
                cover_photo_id=photo.id
            )
            
            # Set owner based on user type
            if hasattr(current_user, 'type') and current_user.type == 'parent':
                album.parent_id = current_user.id
            else:
                album.child_id = current_user.id
                
            db.session.add(album)
            db.session.commit()
            
            # Add photo to album
            album_item = PhotoAlbumItem(
                photo_id=photo.id,
                album_id=album.id,
                position=0
            )
            
            db.session.add(album_item)
            db.session.commit()
        elif form.album_id.data and form.album_id.data.isdigit():
            # Add to existing album
            album_id = int(form.album_id.data)
            album = PhotoAlbum.query.get(album_id)
            
            if album and has_access_to_album(album):
                # Get the highest position in the album
                max_position = db.session.query(func.max(PhotoAlbumItem.position)).filter_by(album_id=album.id).scalar() or 0
                
                # Add photo to album
                album_item = PhotoAlbumItem(
                    photo_id=photo.id,
                    album_id=album.id,
                    position=max_position + 1
                )
                
                db.session.add(album_item)
                db.session.commit()
        
        flash('Photo uploaded successfully!', 'success')
        return redirect(url_for('photos.photos_dashboard'))
    
    return render_template('photos/upload.html', form=form, albums=albums, today_date=today_date)


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
    
    # Check if this is a Firebase Storage photo
    if photo.storage_type == 'firebase' and photo.firebase_url:
        # For Firebase Storage, redirect to the proper URL
        if use_thumbnail and photo.firebase_thumbnail_url:
            return redirect(photo.firebase_thumbnail_url)
        else:
            return redirect(photo.firebase_url)
    
    # For local storage, serve the file directly
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
        
    # Journal fields
    if 'journal_entry' in data:
        photo.journal_entry = data['journal_entry']
        
    if 'journal_date' in data:
        try:
            journal_date = datetime.strptime(data['journal_date'], '%Y-%m-%d').date()
            photo.journal_date = journal_date
        except ValueError:
            pass
            
    if 'mood' in data:
        photo.mood = data['mood']
    
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


# Album routes

@photo_routes.route('/albums')
@login_required
def list_albums():
    """List albums for the current user"""
    # Get albums
    if hasattr(current_user, 'type') and current_user.type == 'parent':
        # Parent's own albums and children's albums
        child_ids = [child.id for child in Child.query.filter_by(parent_id=current_user.id).all()]
        albums = PhotoAlbum.query.filter(
            (PhotoAlbum.parent_id == current_user.id) | 
            (PhotoAlbum.child_id.in_(child_ids))
        ).all()
    else:
        # Child's own albums and parent's albums
        albums = PhotoAlbum.query.filter(
            (PhotoAlbum.child_id == current_user.id) | 
            (PhotoAlbum.parent_id == current_user.parent_id)
        ).all()
    
    # Filter by access
    albums = [album for album in albums if has_access_to_album(album)]
    
    return render_template('photos/albums.html', albums=albums)


@photo_routes.route('/albums/create', methods=['GET', 'POST'])
@login_required
def create_album():
    """Create a new album"""
    form = AlbumForm()
    
    if form.validate_on_submit():
        album = PhotoAlbum(
            name=form.name.data,
            description=form.description.data,
            is_private=form.is_private.data
        )
        
        # Set owner based on user type
        if hasattr(current_user, 'type') and current_user.type == 'parent':
            album.parent_id = current_user.id
        else:
            album.child_id = current_user.id
        
        db.session.add(album)
        db.session.commit()
        
        flash('Album created successfully!', 'success')
        return redirect(url_for('photos.list_albums'))
    
    return render_template('photos/create_album.html', form=form)


@photo_routes.route('/albums/<int:album_id>')
@login_required
def view_album(album_id):
    """View an album"""
    album = PhotoAlbum.query.get_or_404(album_id)
    
    # Check access
    if not has_access_to_album(album):
        flash('You do not have permission to view this album.', 'error')
        return redirect(url_for('photos.list_albums'))
    
    # Get photos in this album
    photo_items = PhotoAlbumItem.query.filter_by(album_id=album.id).order_by(PhotoAlbumItem.position).all()
    photos = []
    
    for item in photo_items:
        photo = Photo.query.get(item.photo_id)
        if photo and has_access_to_photo(photo):
            photos.append(photo)
    
    return render_template('photos/view_album.html', album=album, photos=photos)


@photo_routes.route('/albums/<int:album_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_album(album_id):
    """Edit an album"""
    album = PhotoAlbum.query.get_or_404(album_id)
    
    # Check ownership
    if (album.parent_id and album.parent_id != current_user.id) and \
       (album.child_id and album.child_id != current_user.id):
        flash('You do not have permission to edit this album.', 'error')
        return redirect(url_for('photos.list_albums'))
    
    form = AlbumForm(obj=album)
    
    if form.validate_on_submit():
        album.name = form.name.data
        album.description = form.description.data
        album.is_private = form.is_private.data
        
        db.session.commit()
        
        flash('Album updated successfully!', 'success')
        return redirect(url_for('photos.view_album', album_id=album.id))
    
    return render_template('photos/edit_album.html', form=form, album=album)


@photo_routes.route('/albums/<int:album_id>/delete', methods=['POST'])
@login_required
def delete_album(album_id):
    """Delete an album"""
    album = PhotoAlbum.query.get_or_404(album_id)
    
    # Check ownership
    if (album.parent_id and album.parent_id != current_user.id) and \
       (album.child_id and album.child_id != current_user.id):
        return jsonify({'success': False, 'error': 'You do not have permission to delete this album.'}), 403
    
    # Delete album items
    PhotoAlbumItem.query.filter_by(album_id=album.id).delete()
    
    # Delete album
    db.session.delete(album)
    db.session.commit()
    
    return jsonify({'success': True})


@photo_routes.route('/journal')
@login_required
def journal():
    """Journal view (photos with journal entries)"""
    # Get photos with journal entries
    if hasattr(current_user, 'type') and current_user.type == 'parent':
        # Parent's own photos and children's photos
        child_ids = [child.id for child in Child.query.filter_by(parent_id=current_user.id).all()]
        photos = Photo.query.filter(
            ((Photo.parent_id == current_user.id) | (Photo.child_id.in_(child_ids))) &
            ((Photo.journal_entry != None) & (Photo.journal_entry != ''))
        ).order_by(Photo.journal_date.desc() if Photo.journal_date else Photo.uploaded_at.desc()).all()
    else:
        # Child's own photos and parent's photos
        photos = Photo.query.filter(
            ((Photo.child_id == current_user.id) | (Photo.parent_id == current_user.parent_id)) &
            ((Photo.journal_entry != None) & (Photo.journal_entry != ''))
        ).order_by(Photo.journal_date.desc() if Photo.journal_date else Photo.uploaded_at.desc()).all()
    
    # Filter by access
    photos = [photo for photo in photos if has_access_to_photo(photo)]
    
    # Group by date
    photos_by_date = {}
    for photo in photos:
        date_key = photo.journal_date if photo.journal_date else photo.uploaded_at.date()
        
        if date_key not in photos_by_date:
            photos_by_date[date_key] = []
        
        photos_by_date[date_key].append(photo)
    
    # Sort dates (most recent first)
    photos_by_date = {k: photos_by_date[k] for k in sorted(photos_by_date.keys(), reverse=True)}
    
    return render_template('photos/journal.html', photos_by_date=photos_by_date)