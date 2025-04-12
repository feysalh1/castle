#!/usr/bin/env node

/**
 * This script injects Firebase config environment variables into static files
 * during the build process for Firebase deployment.
 * 
 * Run this script before deploying to Firebase to ensure API keys are not hardcoded
 * in the repository but are injected from environment variables during build.
 */

const fs = require('fs');
const path = require('path');

// Files to process
const FILES_TO_PROCESS = [
  '../public/js/firebase-config.js',
  '../public/js/firebase-init.js',
];

// Environment variables to inject
const ENV_VARS = {
  'FIREBASE_API_KEY': process.env.FIREBASE_API_KEY,
  'FIREBASE_APP_ID': process.env.FIREBASE_APP_ID,
};

// Check if all required environment variables are present
const missingVars = Object.entries(ENV_VARS)
  .filter(([key, value]) => !value)
  .map(([key]) => key);

if (missingVars.length > 0) {
  console.error(`Error: Missing required environment variables: ${missingVars.join(', ')}`);
  console.error('Make sure these variables are set before running this script.');
  process.exit(1);
}

// Process each file
FILES_TO_PROCESS.forEach(relativeFilePath => {
  const filePath = path.join(__dirname, relativeFilePath);
  
  try {
    // Read file content
    let content = fs.readFileSync(filePath, 'utf8');
    
    // Replace placeholders with actual values
    Object.entries(ENV_VARS).forEach(([key, value]) => {
      const placeholder = new RegExp(`"${key}"`, 'g');
      content = content.replace(placeholder, `"${value}"`);
    });
    
    // Write modified content back to file
    fs.writeFileSync(filePath, content);
    console.log(`Successfully updated ${relativeFilePath}`);
  } catch (error) {
    console.error(`Error processing ${relativeFilePath}: ${error.message}`);
  }
});

console.log('Firebase configuration updated successfully.');