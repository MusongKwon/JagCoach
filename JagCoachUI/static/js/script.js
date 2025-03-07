document.getElementById("fileInput").addEventListener("change", function () {
    const file = this.files[0]
    document.getElementById("fileName").textContent = "Selected file: " + file.name;

    const fileURL = URL.createObjectURL(file);
    const vElement = document.getElementById("vPlayback");
    const sElement = vElement.querySelector("source");

    sElement.src = fileURL;
    vElement.load();

// Redhouse - this is to automatically submit the file when selected so it goes back to uploads
// Added another functionality to automatically begin transcribing when uploaded. It just takes awhile.

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
            document.getElementById("transcriptResult").textContent = transcription.transcription || "No transcription found.";
        })
        .catch(error => {
            console.error("Upload/Transcription Error:", error);
            document.getElementById("transcriptResult").textContent = "Error in transcription.";
        });
    }
});