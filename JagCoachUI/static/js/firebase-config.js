const firebaseConfig = {
  apiKey: "",
  authDomain: "jagcoach-25bd3.firebaseapp.com",
  projectId: "jagcoach-25bd3",
  storageBucket: "jagcoach-25bd3.firebasestorage.app",
  messagingSenderId: "441954661380",
  appId: "1:441954661380:web:f2c27dfe43d76ebd9fb151",
  measurementId: "G-P5TMQJWLQS"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
firebase.auth().setPersistence(firebase.auth.Auth.Persistence.LOCAL);
const db = firebase.firestore();
const storage = firebase.storage();
