import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getAnalytics, isSupported } from "firebase/analytics";

const firebaseConfig = {
  apiKey: "AIzaSyApMVCWKshC7c-vhB0HFLh9fgQIGbjdk6M",
  authDomain: "model-a2906.firebaseapp.com",
  projectId: "model-a2906",
  storageBucket: "model-a2906.firebasestorage.app",
  messagingSenderId: "982989826476",
  appId: "1:982989826476:web:cd96fa45ae65e8a263b209",
  measurementId: "G-CFN3QR66GK",
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication
export const auth = getAuth(app);

// Initialize Analytics only when supported by the browser
isSupported().then((supported) => {
  if (supported) {
    getAnalytics(app);
  }
});

export default app;