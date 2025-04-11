"""
Firebase Authentication integration for Children's Castle application.
This module provides functionality to verify Firebase tokens and authenticate users.
"""
import os
import json
import requests
from flask import Blueprint, request, jsonify, session, redirect, url_for
from flask_login import login_user, logout_user, current_user
import firebase_admin
from firebase_admin import auth, credentials
from models import db, Parent, ParentSettings

# Initialize Firebase Admin SDK
cred = None
firebase_initialized = False

try:
    # Try to initialize Firebase Admin SDK
    firebase_project_id = os.environ.get("FIREBASE_PROJECT_ID")
    if firebase_project_id:
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {
            'projectId': firebase_project_id,
        })
        firebase_initialized = True
        print("Firebase Admin SDK initialized successfully")
    else:
        print("FIREBASE_PROJECT_ID environment variable not set")
except Exception as e:
    print(f"Failed to initialize Firebase Admin SDK: {e}")

firebase_auth = Blueprint('firebase_auth', __name__)

@firebase_auth.route('/auth/firebase-login', methods=['POST'])
def firebase_login():
    """Handle Firebase authentication"""
    # Check if Firebase Admin SDK is initialized
    if not firebase_initialized:
        return jsonify({'success': False, 'message': 'Firebase not configured'}), 500
    
    # Get the ID token from the request
    data = request.json
    id_token = data.get('idToken')
    if not id_token:
        return jsonify({'success': False, 'message': 'No ID token provided'}), 400
    
    try:
        # Verify the ID token
        decoded_token = auth.verify_id_token(id_token)
        
        # Get user info
        uid = decoded_token.get('uid')
        email = decoded_token.get('email')
        display_name = decoded_token.get('name', 'User')  # Default to 'User' if name not provided
        
        # Check if the user exists in our database
        parent = Parent.query.filter_by(email=email).first()
        
        if not parent:
            # Create a new parent account
            parent = Parent(
                username=email.split('@')[0],  # Use email prefix as username
                email=email,
                firebase_uid=uid
            )
            db.session.add(parent)
            db.session.commit()
            
            # Create default parent settings
            settings = ParentSettings(parent_id=parent.id)
            db.session.add(settings)
            db.session.commit()
        else:
            # Update Firebase UID if it's not set
            if not parent.firebase_uid:
                parent.firebase_uid = uid
                db.session.commit()
        
        # Log in the parent
        login_user(parent)
        session['user_type'] = 'parent'
        
        return jsonify({'success': True, 'message': 'Login successful', 'redirect': url_for('parent_dashboard')})
    
    except Exception as e:
        print(f"Firebase authentication error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 401

@firebase_auth.route('/firebase-auth', methods=['POST'])
def handle_firebase_auth():
    """Handle Firebase authentication from client-side request"""
    # Check if Firebase Admin SDK is initialized
    if not firebase_initialized:
        return jsonify({'success': False, 'message': 'Firebase not configured'}), 500
    
    # Get the ID token and user info from the request
    data = request.json
    id_token = data.get('idToken')
    display_name = data.get('displayName')
    email = data.get('email')
    is_new_user = data.get('isNewUser', False)
    
    if not id_token or not email:
        return jsonify({'success': False, 'message': 'Invalid request data'}), 400
    
    try:
        # Verify the ID token
        decoded_token = auth.verify_id_token(id_token)
        
        # Get Firebase UID
        uid = decoded_token.get('uid')
        
        # Check if the user exists in our database
        parent = Parent.query.filter_by(email=email).first()
        
        if not parent:
            # Create a new parent account
            username = email.split('@')[0]  # Use email prefix as username
            # Make sure username is unique
            base_username = username
            counter = 1
            while Parent.query.filter_by(username=username).first():
                username = f"{base_username}{counter}"
                counter += 1
                
            parent = Parent(
                username=username,
                email=email,
                firebase_uid=uid,
                display_name=display_name or username
            )
            db.session.add(parent)
            db.session.commit()
            
            # Create default parent settings
            settings = ParentSettings(parent_id=parent.id)
            db.session.add(settings)
            db.session.commit()
            
            print(f"Created new parent account for {email} with Firebase UID {uid}")
        else:
            # Update Firebase UID if it's not set
            if not parent.firebase_uid:
                parent.firebase_uid = uid
                db.session.commit()
                print(f"Updated Firebase UID for {email}")
        
        # Log in the parent
        login_user(parent)
        session['user_type'] = 'parent'
        
        # Record login session with additional metadata
        from app import Session, detect_device_type
        
        new_session = Session(
            user_type='parent', 
            user_id=parent.id,
            ip_address=request.remote_addr,
            user_agent=request.user_agent.string,
            device_type=detect_device_type(request.user_agent.string)
        )
        new_session.record_activity('login')
        db.session.add(new_session)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Login successful', 
            'redirect': url_for('parent_dashboard'),
            'is_new_user': is_new_user
        })
    
    except Exception as e:
        print(f"Firebase authentication error: {e}")
        return jsonify({'success': False, 'message': str(e)}), 401


@firebase_auth.route('/auth/google-signin')
def google_signin():
    """Redirect to Google Sign-in page"""
    return redirect(url_for('index', google_signin='true'))