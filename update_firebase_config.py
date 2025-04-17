#!/usr/bin/env python3
"""
Update Firebase configuration files across the project.
This script ensures all Firebase configuration files are in sync with environment variables.
"""

import os
import sys
from datetime import datetime

def load_env_variables():
    """Load environment variables from .env file if not already set"""
    try:
        # Try to import dotenv
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        print("Warning: python-dotenv not installed. Using existing environment variables.")
    
    # Required Firebase configuration variables
    required_vars = [
        'FIREBASE_API_KEY',
        'FIREBASE_PROJECT_ID',
        'FIREBASE_APP_ID',
        'FIREBASE_MEASUREMENT_ID',
        'FIREBASE_MESSAGING_SENDER_ID',
        'FIREBASE_STORAGE_BUCKET',
        'FIREBASE_AUTH_DOMAIN'
    ]
    
    # Check for missing variables
    missing_vars = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease set these variables in your .env file or environment.")
        sys.exit(1)
    
    # Return configuration dict
    return {
        'apiKey': os.environ.get('FIREBASE_API_KEY'),
        'authDomain': os.environ.get('FIREBASE_AUTH_DOMAIN'),
        'projectId': os.environ.get('FIREBASE_PROJECT_ID'),
        'storageBucket': os.environ.get('FIREBASE_STORAGE_BUCKET'),
        'messagingSenderId': os.environ.get('FIREBASE_MESSAGING_SENDER_ID'),
        'appId': os.environ.get('FIREBASE_APP_ID'),
        'measurementId': os.environ.get('FIREBASE_MEASUREMENT_ID')
    }

def update_static_js_config(config):
    """Update static/js/firebase-config.js"""
    filepath = "static/js/firebase-config.js"
    
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            f.write(f"""// Firebase configuration for Children's Castle
// This file is generated automatically from environment variables
// Last updated: {datetime.now().strftime('%Y-%m-%d')}

const firebaseConfig = {{
  apiKey: "{config['apiKey']}",
  authDomain: "{config['authDomain']}",
  projectId: "{config['projectId']}",
  storageBucket: "{config['storageBucket']}",
  messagingSenderId: "{config['messagingSenderId']}",
  appId: "{config['appId']}",
  measurementId: "{config['measurementId']}"
}};

// Initialize Firebase
try {{
  const app = firebase.initializeApp(firebaseConfig);
  console.log("Firebase config loaded successfully");
  console.log("Firebase initialized with project ID:", firebaseConfig.projectId);
  console.log("Loading system initialized");
}} catch (e) {{
  console.error("Firebase initialization error:", e);
}}
""")
        print(f"Updated {filepath}")
        return True
    except Exception as e:
        print(f"Error updating {filepath}: {e}")
        return False

def update_public_config(config):
    """Update public/firebase-config.js"""
    filepath = "public/firebase-config.js"
    
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w') as f:
            f.write(f"""// Firebase configuration for Children's Castle
// This file is generated automatically from environment variables
// Last updated: {datetime.now().strftime('%Y-%m-%d')}

const firebaseConfig = {{
  apiKey: "{config['apiKey']}",
  authDomain: "{config['authDomain']}",
  projectId: "{config['projectId']}",
  storageBucket: "{config['storageBucket']}",
  messagingSenderId: "{config['messagingSenderId']}",
  appId: "{config['appId']}",
  measurementId: "{config['measurementId']}"
}};

// Initialize Firebase
try {{
  const app = firebase.initializeApp(firebaseConfig);
  console.log("Firebase config loaded successfully in static hosting");
}} catch (e) {{
  console.error("Firebase initialization error:", e);
}}
""")
        print(f"Updated {filepath}")
        return True
    except Exception as e:
        print(f"Error updating {filepath}: {e}")
        return False

def main():
    """Main function to update all Firebase configuration files"""
    print("Updating Firebase configuration files...")
    
    # Load environment variables
    config = load_env_variables()
    
    # Update configuration files
    success = []
    success.append(update_static_js_config(config))
    success.append(update_public_config(config))
    
    # Print results
    if all(success):
        print("\nAll Firebase configuration files updated successfully!")
        print("Project: " + config['projectId'])
        print("Storage Bucket: " + config['storageBucket'])
        print("App ID: " + config['appId'])
    else:
        print("\nSome configuration files could not be updated. Check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()