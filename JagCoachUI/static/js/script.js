document.getElementById("fileInput").addEventListener("change", function () {
    const file = this.files[0];
    const transcriptResult = document.getElementById("transcriptResult");
    const loadSpinner = document.getElementById("loadSpinner");

    // Show the loading spinner and update the text
    transcriptResult.textContent = "Processing transcription...";
    loadSpinner.style.display = "block";

    const fileURL = URL.createObjectURL(file);
    const vElement = document.getElementById("vPlayback");
    const sElement = vElement.querySelector("source");

    sElement.src = fileURL;
    vElement.load();

    if (file) {
        const formData = new FormData();
        formData.append("video_file", file);

        fetch("/", {
            method: "POST",
            body: formData,
        })
        .then(response => response.text())
        .then(data => {
            console.log("Server Response:", data);
            return fetch("/transcribe", { method: "POST" });
        })
        .then(response => response.json())
        .then(transcription => {
            console.log("Transcription:", transcription);
            transcriptResult.textContent = transcription.transcription || "No transcription found.";
        })
        .catch(error => {
            console.error("Upload/Transcription Error:", error);
            transcriptResult.textContent = "Error in transcription.";
        })
        .finally(() => {
            loadSpinner.style.display = "none";
        });
    }
});