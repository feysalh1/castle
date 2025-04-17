#!/usr/bin/env python3
"""
Environment variable setup script for Children's Castle
This script helps set up environment variables for different deployment environments.
"""

import os
import sys
import argparse
from dotenv import load_dotenv

def setup_environment():
    """
    Load environment variables from .env file and set up the environment.
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Check required environment variables
    required_vars = [
        'FIREBASE_API_KEY',
        'FIREBASE_PROJECT_ID',
        'FIREBASE_APP_ID',
        'FIREBASE_MEASUREMENT_ID',
        'FIREBASE_MESSAGING_SENDER_ID',
        'FIREBASE_STORAGE_BUCKET',
        'FIREBASE_AUTH_DOMAIN'
    ]
    
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
    
    # Print environment information
    print("Environment configured successfully!")
    print(f"Firebase Project: {os.environ.get('FIREBASE_PROJECT_ID')}")
    print(f"Firebase Storage: {'Enabled' if os.environ.get('FIREBASE_STORAGE_ENABLED') == 'true' else 'Disabled'}")

def export_env_for_deployment(output_file='.env.production'):
    """
    Export environment variables to a production .env file
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Get environment variables
    env_vars = {
        'FIREBASE_API_KEY': os.environ.get('FIREBASE_API_KEY', ''),
        'FIREBASE_PROJECT_ID': os.environ.get('FIREBASE_PROJECT_ID', ''),
        'FIREBASE_APP_ID': os.environ.get('FIREBASE_APP_ID', ''),
        'FIREBASE_MEASUREMENT_ID': os.environ.get('FIREBASE_MEASUREMENT_ID', ''),
        'FIREBASE_MESSAGING_SENDER_ID': os.environ.get('FIREBASE_MESSAGING_SENDER_ID', ''),
        'FIREBASE_STORAGE_BUCKET': os.environ.get('FIREBASE_STORAGE_BUCKET', ''),
        'FIREBASE_AUTH_DOMAIN': os.environ.get('FIREBASE_AUTH_DOMAIN', ''),
        'FIREBASE_STORAGE_ENABLED': 'true'
    }
    
    # Write environment variables to output file
    with open(output_file, 'w') as f:
        f.write("# Production environment configuration for Children's Castle\n")
        f.write("# Generated automatically by setup_env.py\n\n")
        
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
    
    print(f"Production environment variables exported to {output_file}")

def export_firebase_json(output_file='firebase-env.json'):
    """
    Export Firebase configuration to a JSON file
    """
    # Load environment variables from .env file
    load_dotenv()
    
    # Get Firebase environment variables
    firebase_config = {
        'apiKey': os.environ.get('FIREBASE_API_KEY', ''),
        'authDomain': os.environ.get('FIREBASE_AUTH_DOMAIN', ''),
        'projectId': os.environ.get('FIREBASE_PROJECT_ID', ''),
        'storageBucket': os.environ.get('FIREBASE_STORAGE_BUCKET', ''),
        'messagingSenderId': os.environ.get('FIREBASE_MESSAGING_SENDER_ID', ''),
        'appId': os.environ.get('FIREBASE_APP_ID', ''),
        'measurementId': os.environ.get('FIREBASE_MEASUREMENT_ID', '')
    }
    
    # Write Firebase configuration to output file
    with open(output_file, 'w') as f:
        f.write("{\n")
        
        # Write each key-value pair
        for i, (key, value) in enumerate(firebase_config.items()):
            comma = ',' if i < len(firebase_config) - 1 else ''
            f.write(f'  "{key}": "{value}"{comma}\n')
        
        f.write("}\n")
    
    print(f"Firebase configuration exported to {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Environment variable setup for Children\'s Castle')
    
    # Add subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Setup command
    setup_parser = subparsers.add_parser('setup', help='Set up environment variables')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export environment variables')
    export_parser.add_argument('--output', '-o', default='.env.production', help='Output file path')
    
    # Firebase JSON export command
    firebase_parser = subparsers.add_parser('firebase-json', help='Export Firebase configuration as JSON')
    firebase_parser.add_argument('--output', '-o', default='firebase-env.json', help='Output file path')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Run appropriate command
    if args.command == 'setup':
        setup_environment()
    elif args.command == 'export':
        export_env_for_deployment(args.output)
    elif args.command == 'firebase-json':
        export_firebase_json(args.output)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()