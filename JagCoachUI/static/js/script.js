document.getElementById("fileInput").addEventListener("change", function () {
    const file = this.files[0];
    const transcriptResult = document.getElementById("transcriptResult");
    const loadSpinner = document.getElementById("loadSpinner");
    const toggleButton = document.getElementById("toggleButton");
    let originalText = transcriptResult.textContent;
    const evaluationResult = document.getElementById("evaluationResult");
    const evaluationSpinner = document.getElementById("evaluationSpinner");

    // Show loading spinners
    transcriptResult.textContent = "Processing transcription...";
    loadSpinner.style.display = "block";

    evaluationResult.textContent = "Examining presentation...";
    evaluationSpinner.style.display = "block";

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
            // Below is the JS implementation to show the transcript lines. Just makes it easier to read. For extra
            // credit we could have the user be able to download the transcript with highlights of where
            // improvements could be.
            const lines = transcription.lines || [];
            if (lines.length > 0){
                transcriptResult.innerHTML = lines.map((line, index) => {
                    // Starts at line 1 and defaults to a space of 2 then returnes the number line and then the
                    // sentence.
                    const lineNumber = String(index + 1).padStart(2, ' ');
                    return `<p>${lineNumber}. ${line}</p>`;
                }).join("");
            } else {
                transcriptResult.innerHTML = "<p>No transcription found.</p>";
            }

            loadSpinner.style.display = "none";

            toggleButton.onclick = toggleTranscript;

            return fetch("/evaluate", { method: "POST" });
        })
        .then(response => response.json())
        .then(evaluation => {
            console.log("Evaluation:", evaluation);
            evaluationResult.textContent = evaluation.evaluation || "No evaluation available.";
        })
        .catch(error => {
            console.error("Upload/Transcription Error:", error);
            transcriptResult.textContent = "Error in transcription.";
            loadSpinner.style.display = "none";
        })
        .catch(error => {
            console.error("Evaluation Error:", error);
            evaluationResult.textContent = "Error in evaluation.";
        })
        .finally(() => {
            evaluationSpinner.style.display = "none";
        });
    }
});


// A simple function that allows the user to hide and show the transcript.

function toggleTranscript() {
    const transcriptContainer = document.getElementById("transcriptContainer");
    const toggleButton = document.getElementById("toggleButton");
    const ellipsis = document.getElementById("ellipsis");

    transcriptContainer.classList.toggle("hidden");

    if (transcriptContainer.classList.contains("hidden")) {
        toggleButton.textContent = "Show Transcript";
        ellipsis.style.display = "block";
    } else {
        toggleButton.textContent = "Hide Transcript";
        ellipsis.style.display = "none";
    }
}
