
const firebaseConfig = {
  apiKey: process.env.FIREBASE_API_KEY,
  projectId: "story-time-fun",
  appId: "1:225122848236:web:5c0cd7632ce0f09973c4c9",
  authDomain: "story-time-fun.firebaseapp.com",
  storageBucket: "story-time-fun.appspot.com",
  messagingSenderId: "225122848236",
  measurementId: "G-RM452TNB0W"
};

// Initialize Firebase
const app = firebase.initializeApp(firebaseConfig);
console.log("Firebase initialized with project ID:", firebaseConfig.projectId);
console.log("Loading system initialized");
