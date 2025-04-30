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

  // TODO: Implement saving logic!
  alert("Saving: " + newUsername + (profilePicFile ? " with new profile picture." : ""));

  // Close modal after save
  closeEditProfile();
}

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
