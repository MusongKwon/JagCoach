// Initialize Firebase Authentication & Firestore (already done in firebase-config.js)

function openEditProfile() {
  document.getElementById("editProfileModal").classList.remove("hidden");
}

function closeEditProfile() {
  document.getElementById("editProfileModal").classList.add("hidden");
}

async function saveProfileChanges() {
  const newUsername = document.getElementById("newUsername").value.trim();
  const profilePicFile = document.getElementById("profilePicUpload").files[0];

  try {
    // Get user from Firebase Auth
    const user = firebase.auth().currentUser;
    if (!user) {
      alert("No user logged in.");
      return;
    }

    let photoURL = null;

    // 1. Upload profile picture (if provided)
    if (profilePicFile) {
      const storageRef = firebase.storage().ref();
      const profilePicRef = storageRef.child(`profile_pictures/${user.email}/profile.jpg`);
      await profilePicRef.put(profilePicFile);
      photoURL = await profilePicRef.getDownloadURL();
    }

    // 2. Save updated info to Firestore
    const db = firebase.firestore();
    const userDocRef = db.collection("users").doc(user.email);

    const updateData = {};
    if (newUsername) updateData.username = newUsername;
    if (photoURL) updateData.photoURL = photoURL;

    await userDocRef.set(updateData, { merge: true });

    alert("Profile updated!");
    closeEditProfile();
    location.reload();  // Optional: force refresh to show changes
  } catch (error) {
    console.error("Error saving profile:", error);
    alert("Failed to save profile changes.");
  }
}

window.openEditProfile = openEditProfile;
window.closeEditProfile = closeEditProfile;



// Add this OUTSIDE the DOMContentLoaded block
async function viewUpload(filename) {
  try {
    const response = await fetch(`/get_presentation_details/${filename}`);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Unknown error");
    }

    document.getElementById("presentationVideo").src = data.video_url || "";
    document.getElementById("presentationTranscript").textContent = data.transcript || "No transcript available.";
    document.getElementById("presentationEvaluation").textContent = data.evaluation || "No evaluation available.";

    document.getElementById("viewPresentationModal").classList.remove("hidden");
  } catch (error) {
    console.error("Error viewing upload:", error);
    alert("Error retrieving presentation data.");
  }
}

// 👇 Expose it globally so inline `onclick` can call it
window.viewUpload = viewUpload;

function closeViewModal() {
  document.getElementById("viewPresentationModal").classList.add("hidden");
}
window.closeViewModal = closeViewModal;



async function deleteUpload(filename, buttonElement) {
  if (!confirm("Are you sure you want to delete this upload?")) {
    return;
  }

  try {
    const response = await fetch("/delete_upload", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ filename: filename })
    });

    const result = await response.json();

    if (response.ok) {
      alert("Upload deleted successfully!");

      // Remove the parent card from the page
      const card = buttonElement.closest(".glass-card");
      if (card) {
        card.remove();
      }
    } else {
      alert("Error deleting upload: " + result.error);
    }
  } catch (error) {
    console.error("Error deleting upload:", error);
    alert("Error deleting upload.");
  }
}



document.addEventListener("DOMContentLoaded", () => {
  // put your viewUpload() function inside here
  async function viewUpload(filename) {
    try {
      const response = await fetch(`/get_presentation_details/${filename}`);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Unknown error");
      }

      document.getElementById("presentationVideo").src = data.video_url || "";
      document.getElementById("presentationTranscript").textContent = data.transcript || "No transcript available.";
      document.getElementById("presentationEvaluation").textContent = data.evaluation || "No evaluation available.";

      document.getElementById("viewPresentationModal").classList.remove("hidden");
    } catch (error) {
      console.error("Error viewing upload:", error);
      alert("Error retrieving presentation data.");
    }
  }
});
