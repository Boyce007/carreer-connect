// Initialize Firebase Authentication
const auth = firebase.auth();

// Get input fields and buttons
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const signUpButton = document.getElementById("sign-up");
const signInButton = document.getElementById("sign-in");
const signOutButton = document.getElementById("sign-out");
const authMessage = document.getElementById("auth-message");

// Sign Up
signUpButton.addEventListener("click", () => {
    const email = emailInput.value;
    const password = passwordInput.value;

    auth.createUserWithEmailAndPassword(email, password)
        .then(userCredential => {
            authMessage.textContent = "Account created successfully!";
            signOutButton.style.display = "block";
        })
        .catch(error => {
            authMessage.textContent = "Error: " + error.message;
        });
});

// Sign In
signInButton.addEventListener("click", () => {
    const email = emailInput.value;
    const password = passwordInput.value;

    auth.signInWithEmailAndPassword(email, password)
        .then(userCredential => {
            authMessage.textContent = "Signed in successfully!";
            setTimeout(() => {
                window.location.href = "course.html"; // Redirect to courses
            }, 1500);
        })
        .catch(error => {
            authMessage.textContent = "Error: " + error.message;
        });
});

// Sign Out
signOutButton.addEventListener("click", () => {
    auth.signOut()
        .then(() => {
            authMessage.textContent = "Signed out successfully!";
            signOutButton.style.display = "none";
        })
        .catch(error => {
            authMessage.textContent = "Error: " + error.message;
        });
});

const db = firebase.firestore();

// Save user data (e.g., profile info)
function saveUserData(userId, userData) {
    db.collection('users').doc(userId).set(userData)
        .then(() => {
            console.log("User data saved!");
        })
        .catch((error) => {
            console.error("Error saving user data: ", error);
        });
}

// Check Authentication State
auth.onAuthStateChanged(user => {
    if (user) {
        authMessage.textContent = `Logged in as ${user.email}`;
        signOutButton.style.display = "block";
    } else {
        authMessage.textContent = "Not logged in.";
        signOutButton.style.display = "none";
    }
});


// Save user data (e.g., profile info)
function saveUserData(userId, userData) {
    db.collection('users').doc(userId).set(userData)
        .then(() => {
            console.log("User data saved!");
        })
        .catch((error) => {
            console.error("Error saving user data: ", error);
        });
}

const storage = firebase.storage();

// Upload resume
function uploadResume(file) {
    const userId = firebase.auth().currentUser.uid;
    const storageRef = storage.ref().child(`resumes/${userId}/${file.name}`);
    
    storageRef.put(file).then((snapshot) => {
        console.log("Resume uploaded successfully!");
        // After uploading, you can get the file URL and save it to Firestore
        storageRef.getDownloadURL().then((url) => {
            saveResumeURLToUserProfile(userId, url);
        });
    }).catch((error) => {
        console.error("Error uploading resume: ", error);
    });
}

// Save resume URL to Firestore
function saveResumeURLToUserProfile(userId, resumeURL) {
    db.collection('users').doc(userId).update({
        resume: resumeURL
    }).then(() => {
        console.log("Resume URL saved to user profile!");
    }).catch((error) => {
        console.error("Error saving resume URL: ", error);
    });
}
