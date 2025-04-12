// Firebase SDK - Using the latest version
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.6.0/firebase-app.js";
import {
    getAuth,
    signInWithPopup,
    GoogleAuthProvider,
    getAdditionalUserInfo
} from "https://www.gstatic.com/firebasejs/11.6.0/firebase-auth.js";

// Your web app's Firebase configuration - Updated with the new project config
const firebaseConfig = {
    apiKey: "AIzaSyAPTQO3lnt0GSyDgVCZjtj4i3gk3Qi6Vyo",
    authDomain: "story-time-fun.firebaseapp.com",
    projectId: "story-time-fun",
    storageBucket: "story-time-fun.appspot.com",
    messagingSenderId: "225122848236",
    appId: "1:952095451786:web:b3d6229418a1fd06972693"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
console.log("Firebase initialized successfully!");
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

/**
 * Sign in with Google and handle the authentication flow
 * @returns {Promise} Promise that resolves when the sign-in process is complete
 */
export async function signInWithGoogle() {
    try {
        // Sign in with Google popup
        const result = await signInWithPopup(auth, provider);
        
        // Get the user token
        const credential = GoogleAuthProvider.credentialFromResult(result);
        const token = credential.accessToken;
        
        // Get user info
        const user = result.user;
        const isNewUser = getAdditionalUserInfo(result)?.isNewUser;
        
        // Get the Firebase ID token
        const idToken = await user.getIdToken();
        
        // Send the token to the server
        const response = await fetch('/firebase-auth', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                idToken: idToken,
                displayName: user.displayName,
                email: user.email,
                isNewUser: isNewUser
            })
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Failed to authenticate with server');
        }
        
        const data = await response.json();
        
        // Redirect based on the server response
        if (data.redirect) {
            window.location.href = data.redirect;
        }
        
        return data;
    } catch (error) {
        console.error("Firebase authentication error:", error);
        throw error;
    }
}