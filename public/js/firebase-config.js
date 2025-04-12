
// Firebase configuration for Children's Castle
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

// Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyAPTQO3lnt0GSyDgVCZjtj4i3gk3Qi6Vyo",
  authDomain: "story-time-fun.firebaseapp.com",
  projectId: "story-time-fun",
  storageBucket: "story-time-fun.appspot.com",
  messagingSenderId: "225122848236",
  appId: "1:225122848236:web:b52d382202a2ce6a73c4c9"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);

export { app, auth };
