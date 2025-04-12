// Firebase configuration for Children's Castle
// This file initializes Firebase for the application

// Import the functions you need from the SDKs
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-analytics.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyAPTQO3lnt0GSyDgVCZjtj4i3gk3Qi6Vyo",
  authDomain: "story-time-fun.firebaseapp.com",
  projectId: "story-time-fun",
  storageBucket: "story-time-fun.firebasestorage.app",
  messagingSenderId: "225122848236",
  appId: "1:225122848236:web:b52d382202a2ce6a73c4c9",
  measurementId: "G-RM452TNB0W"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);

// Export the Firebase instances for use in other modules
export { app, analytics, auth };