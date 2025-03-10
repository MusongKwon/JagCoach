document.getElementById("fileInput").addEventListener("change", function () {
    const file = this.files[0];
    const transcriptResult = document.getElementById("transcriptResult");
    const loadSpinner = document.getElementById("loadSpinner");
    const toggleButton = document.getElementById("toggleButton");
    const ellipsis = document.getElementById("ellipsis");
    let originalText = transcriptResult.textContent;
    const evaluationResult = document.getElementById("evaluationResult");
    const evaluationSpinner = document.getElementById("evaluationSpinner");

    // Show the loading spinner and update the text for trascription
    transcriptResult.textContent = "Processing transcription...";
    loadSpinner.style.display = "block";

    // Show the loading spinner and update the text for evaluation
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
            originalText = transcription.transcription || "No transcription found.";
            transcriptResult.textContent = originalText;
            loadSpinner.style.display = "none";
            toggleButton.onclick = function() {
                if (transcriptResult.style.display === "none") {
                    transcriptResult.style.display = "block";
                    ellipsis.style.display = "none"; // Hide ellipsis
                } else {
                    transcriptResult.style.display = "none";
                    ellipsis.style.display = "block"; // Show ellipsis
                }
            };

            // call /evaluate endpoint
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
