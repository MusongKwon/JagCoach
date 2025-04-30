window.addEventListener("DOMContentLoaded", () => {
  const emailField    = document.getElementById("email");
  const passwordField = document.getElementById("password");
  const signupBtn     = document.getElementById("signupBtn");
  const loginBtn      = document.getElementById("loginBtn");
  const message       = document.getElementById("authMessage");

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

  function validateInputs() {
    const email    = emailField.value.trim();
    const password = passwordField.value;

    if (!email) {
      console.log("Validation Failure: Email cannot be blank");
      message.textContent = "Error: Email cannot be blank";
      return null;
    }
    if (!emailRegex.test(email)) {
      console.log("Validation Failure: Email not valid");
      message.textContent = "Error: Please enter a valid email";
      return null;
    }
    if (!password) {
      console.log("Validation Failure: Password cannot be blank");
      message.textContent = "Error: Password cannot be blank";
      return null;
    }
    if (password.length < 6) {
      console.log("Validation Failure: Password is too short");
      message.textContent = "Error: Password must be at least 6 characters";
      return null;
    }

    // clear previous message
    message.textContent = "";
    return { email, password };
  }

    // <— new helper:
  function getFriendlyError(err) {
    switch (err.code) {
      case "auth/email-already-in-use":
        return "That email is already in use. Try logging in.";
      case "auth/invalid-email":
        return "That email address is not valid.";
      case "auth/weak-password":
        return "Your password is too weak.";
      case "auth/user-not-found":
      case "auth/wrong-password":
      case "auth/invalid-login-credentials":
        return "User does not exist or wrong login info. Please sign up or try again.";
      default:
        return err.message;
    }
  }

  signupBtn.addEventListener("click", () => {
    const creds = validateInputs();
    if (!creds) return;

    firebase
      .auth()
      .createUserWithEmailAndPassword(creds.email, creds.password)
      .then(userCredential => handleLogin(userCredential.user))
      .catch(err => {
        console.error(err);
        message.textContent = err.message;
      });
  });

  loginBtn.addEventListener("click", () => {
    const creds = validateInputs();
    if (!creds) return;

    firebase
      .auth()
      .signInWithEmailAndPassword(creds.email, creds.password)
      .then(userCredential => handleLogin(userCredential.user))
      .catch(err => {
        console.error(err);
        message.textContent = err.message;
      });
  });

  function handleLogin(user) {
    user
      .getIdToken()
      .then(idToken =>
        fetch("/sessionLogin", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ idToken }),
        })
      )
      .then(res => {
        if (res.ok) {
          window.location.href = "/";
        } else {
          message.textContent = "Login failed on server.";
        }
      })
      .catch(err => {
        console.error(err);
        message.textContent = "Error connecting to server.";
      });
  }
});
