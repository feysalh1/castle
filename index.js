const functions = require('firebase-functions');
const { exec } = require('child_process');
const express = require('express');
const app = express();

// Set up Express middleware
app.use((req, res, next) => {
  // Forward requests to our Flask application
  const process = exec('python main.py', (error) => {
    if (error) {
      console.error(`Error executing Flask app: ${error}`);
      return res.status(500).send('Server Error');
    }
  });
  
  // Handle data events from Flask
  process.stdout.on('data', (data) => {
    res.write(data);
  });
  
  // Handle end event
  process.on('close', (code) => {
    if (code !== 0) {
      console.error(`Flask process exited with code ${code}`);
      return res.status(500).end();
    }
    return res.end();
  });
});

// Export the Express app as a Firebase Function
exports.app = functions.https.onRequest(app);