
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";

// Your Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDH687LJ8huxt_zpE4TYWqB9OsCLTH4HDw", // Firebase Web API key
  authDomain: "healthcare-77135.firebaseapp.com",
  projectId: "healthcare-77135",
  storageBucket: "healthcare-77135.appspot.com",
  messagingSenderId: "867221601164",
  appId: "1:867221601164:web:e094a34d9f052d58d2f41c"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firebase Authentication
export const auth = getAuth(app);
export default app;
