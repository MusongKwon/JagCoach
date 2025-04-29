window.addEventListener("DOMContentLoaded", () => {
    const emailField = document.getElementById("email");
    const passwordField = document.getElementById("password");
    const signupBtn = document.getElementById("signupBtn");
    const loginBtn = document.getElementById("loginBtn");
    const message = document.getElementById("authMessage");

    signupBtn.addEventListener("click", () => {
        const email = emailField.value;
        const password = passwordField.value;
        firebase.auth().createUserWithEmailAndPassword(email, password)
            .then(userCredential => handleLogin(userCredential.user))
            .catch(err => {
                console.error(err);
                message.textContent = err.message;
            });
    });

    loginBtn.addEventListener("click", () => {
        const email = emailField.value;
        const password = passwordField.value;
        firebase.auth().signInWithEmailAndPassword(email, password)
            .then(userCredential => handleLogin(userCredential.user))
            .catch(err => {
                console.error(err);
                message.textContent = err.message;
            });
    });

    function handleLogin(user) {
        user.getIdToken().then(idToken => {
            fetch("/sessionLogin", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ idToken })
            }).then(res => {
                if (res.ok) {
                    window.location.href = "/";
                } else {
                    message.textContent = "Login failed on server.";
                }
            }).catch(err => {
                console.error(err);
                message.textContent = "Error connecting to server.";
            });
        });
    }
});
