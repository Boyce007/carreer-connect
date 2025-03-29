// firebase-config.js
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-auth.js";
import { getAnalytics } from "https://www.gstatic.com/firebasejs/11.4.0/firebase-analytics.js";

// Firebase configuration


const firebaseConfig = {
  apiKey: "AIzaSyDkRqpz4hREQiAUKLFa3IiBtvQPf4mIPx8",
  authDomain: "careerconnect-cedf4.firebaseapp.com",
  projectId: "careerconnect-cedf4",
  storageBucket: "careerconnect-cedf4.firebasestorage.app",
  messagingSenderId: "668075698731",
  appId: "1:668075698731:web:eb73df6eb27dba07cbd86e",
  measurementId: "G-XBX9XK3H7H"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const auth = getAuth(app); // Authentication instance

export { auth };
