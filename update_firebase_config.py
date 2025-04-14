#!/usr/bin/env python3
"""
Script to update Firebase configuration files with the current environment variables.
This ensures that both the static and public versions of firebase-config.js
have the same, correct configuration.
"""

import os
import sys


def update_firebase_config():
    """
    Update Firebase configuration files with the current environment variables.
    """
    # Default values from our current configuration
    default_config = {
        "apiKey": "AIzaSyAPTQO3lnt0GSyDgVCZjtj4i3gk3Qi6Vyo",
        "authDomain": "story-time-fun.firebaseapp.com",
        "projectId": "story-time-fun",
        "storageBucket": "story-time-fun.firebasestorage.app",
        "messagingSenderId": "225122848236",
        "appId": "1:225122848236:web:b52d382202a2ce6a73c4c9",
        "measurementId": "G-RM452TNB0W"
    }
    
    # Get environment variables with defaults from our configuration
    firebase_api_key = os.environ.get("FIREBASE_API_KEY", default_config["apiKey"])
    firebase_auth_domain = os.environ.get("FIREBASE_AUTH_DOMAIN", default_config["authDomain"])
    firebase_project_id = os.environ.get("FIREBASE_PROJECT_ID", default_config["projectId"])
    firebase_storage_bucket = os.environ.get("FIREBASE_STORAGE_BUCKET", default_config["storageBucket"])
    firebase_messaging_sender_id = os.environ.get("FIREBASE_MESSAGING_SENDER_ID", default_config["messagingSenderId"])
    firebase_app_id = os.environ.get("FIREBASE_APP_ID", default_config["appId"])
    firebase_measurement_id = os.environ.get("FIREBASE_MEASUREMENT_ID", default_config["measurementId"])

    # Create the template with proper formatting
    firebase_config_template = f"""// Firebase configuration for Children's Castle
// This file is generated automatically from environment variables
// Last updated: {sys.argv[1] if len(sys.argv) > 1 else "manually"}

const firebaseConfig = {{
  apiKey: "{firebase_api_key}",
  authDomain: "{firebase_auth_domain}",
  projectId: "{firebase_project_id}",
  storageBucket: "{firebase_storage_bucket}",
  messagingSenderId: "{firebase_messaging_sender_id}",
  appId: "{firebase_app_id}",
  measurementId: "{firebase_measurement_id}"
}};

// Initialize Firebase
const app = firebase.initializeApp(firebaseConfig);
console.log("Firebase config loaded successfully");
console.log("Firebase initialized with project ID:", firebaseConfig.projectId);
console.log("Loading system initialized");
"""

    # List of files to update
    config_files = [
        "static/js/firebase-config.js",
        "public/firebase-config.js"
    ]

    # Update all config files
    for file_path in config_files:
        try:
            with open(file_path, "w") as f:
                f.write(firebase_config_template)
            print(f"Updated {file_path}")
        except Exception as e:
            print(f"Error updating {file_path}: {e}")
            return False

    return True


if __name__ == "__main__":
    if update_firebase_config():
        print("Firebase configuration updated successfully")
        sys.exit(0)
    else:
        print("Failed to update Firebase configuration")
        sys.exit(1)