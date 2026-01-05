// src/firebase.ts
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
  apiKey: "AIzaSyA4W90PteeQ5-_osTyioZgMofRdUT9cEs4",
  authDomain: "portal-assinaturas-ai.firebaseapp.com",
  projectId: "portal-assinaturas-ai",
  storageBucket: "portal-assinaturas-ai.firebasestorage.app",
  messagingSenderId: "473640121277",
  appId: "1:473640121277:web:0b84a7acb609bcebe498d4"
};


console.log("🔥 firebase.ts carregado com API KEY:", firebaseConfig.apiKey);

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
export const db = getFirestore(app);
export default app;
