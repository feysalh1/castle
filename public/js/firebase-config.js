// Firebase configuration for Children's Castle
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-analytics.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";

const firebaseConfig = {
  apiKey: process.env.FIREBASE_API_KEY,
  authDomain: "story-time-fun.firebaseapp.com",
  projectId: "story-time-fun",
  storageBucket: "story-time-fun.appspot.com",
  messagingSenderId: "952095451786",
  appId: "1:952095451786:web:b3d6229418a1fd06972693",
  measurementId: "G-TW65TD3GJ5"
};

const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app);

export { app, analytics, auth };