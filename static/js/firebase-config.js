// Firebase configuration for Children's Castle
// This file initializes Firebase for the application

// Import the functions you need from the SDKs
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-analytics.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
// Configuration is loaded from the window object which gets values from the server
const firebaseConfig = {
  apiKey: window.FIREBASE_API_KEY || '',
  authDomain: window.FIREBASE_AUTH_DOMAIN || '',
  projectId: window.FIREBASE_PROJECT_ID || '',
  storageBucket: window.FIREBASE_STORAGE_BUCKET || '',
  messagingSenderId: window.FIREBASE_MESSAGING_SENDER_ID || '',
  appId: window.FIREBASE_APP_ID || '',
  measurementId: window.FIREBASE_MEASUREMENT_ID || ''
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);

// Export the Firebase instances for use in other modules
export { app, analytics, auth };