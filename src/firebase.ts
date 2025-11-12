// src/firebase.js
import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore"; // 👈 Adicione isto

const firebaseConfig = {
  apiKey: "AIzaSyDwo5ScsP8TiwiGPuZB-GBdxSrHrwb0n70",
  authDomain: "portal-assinaturas-ai.firebaseapp.com",
  projectId: "portal-assinaturas-ai",
  storageBucket: "portal-assinaturas-ai.appspot.com",
  messagingSenderId: "473640121277",
  appId: "1:473640121277:web:0b84a7acb609bcebe498d4"
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);
export const db = getFirestore(app); // 👈 Isso resolve o erro
export default app;
