document.addEventListener("DOMContentLoaded", function () {
    const videoElement = document.getElementById("cameraStream");
    const startButton = document.getElementById("startButton");
    const stopButton = document.getElementById("stopButton");
    const transcriptResult = document.getElementById("transcriptResult");
    const loadSpinner = document.getElementById("loadSpinner");
    const toggleButton = document.getElementById("toggleButton");
    const evaluationResult = document.getElementById("evaluationResult");
    const evaluationSpinner = document.getElementById("evaluationSpinner");
    const evaluationTabs = document.getElementById("evaluationTabs");
    
    transcriptResult.textContent = "Processing transcription...";
    loadSpinner.style.display = "block";

    evaluationResult.textContent = "Examining presentation...";
    evaluationSpinner.style.display = "block";

    let originalText = transcriptResult.textContent;
    let mediaStream = null;
    let mediaRecorder = null;
    let segmentCounter = 0;
    let segmentInterval = null;
    let recordingEnded = false;

    startButton.addEventListener("click", async () => {
        if (!stopButton.disabled) {
            // User hasn't stopped yet, prevent starting again
            return;
        }
    
        if (recordingEnded) {
            // If a previous recording ended, reset everything
            segmentCounter = 0;
            evaluationTabs.innerHTML = ""; // Clear all previous evaluation tabs
            transcriptResult.textContent = "Processing transcription...";
            loadSpinner.style.display = "block";
            evaluationResult.textContent = "Examining presentation...";
            evaluationSpinner.style.display = "block";
            recordingEnded = false;
        }
    
        try {
            mediaStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
            videoElement.srcObject = mediaStream;
            videoElement.style.transform = "scaleX(-1)";
    
            mediaRecorder = new MediaRecorder(mediaStream, { mimeType: "video/webm;codecs=vp8,opus" });
            
            mediaRecorder.onstop = async () => {
                const blob = new Blob(recordedChunks, { type: "video/webm" });
                const file = new File([blob], `${segmentCounter}_segment.webm`, { type: "video/webm" });
                const formData = new FormData();
                formData.append("video_file", file);
                formData.append("segment_number", segmentCounter);
    
                try {
                    await fetch("/live-index", { method: "POST", body: formData });
                    await fetch("/live-transcribe", { method: "POST", body: formData })
                        .then(response => response.json())
                        .then(transcription => {
                            originalText = transcription.transcription || "No transcription found.";
                            transcriptResult.textContent = originalText;
                            loadSpinner.style.display = "none";
                            toggleButton.onclick = toggleTranscript;
                        });
    
                    await fetch("/live-evaluate", { method: "POST", body: formData })
                        .then(response => response.json())
                        .then(evaluation => {
                            if (evaluationResult) {
                                if (evaluation.evaluation) {
                                    if (evaluationResult.textContent !== "Upload a video to begin analysis.") {
                                        const evaluationValue = evaluation.evaluation;
                                        const tabButton = document.createElement("button");
                                        tabButton.textContent = `Segment ${segmentCounter + 1}`;
                                        tabButton.className = "bg-gray-700 hover:bg-gray-600 text-white px-3 py-1 rounded text-sm";
                                        tabButton.addEventListener("click", () => {
                                            evaluationResult.textContent = evaluationValue;
                                        });
                                        evaluationTabs.appendChild(tabButton);
                                    }
                                    evaluationResult.textContent = evaluation.evaluation;
                                } else {
                                    evaluationResult.textContent = "No evaluation available.";
                                }
                            }
                        })
                        .finally(() => {
                            evaluationSpinner.style.display = "none";
                        });
    
                    recordedChunks = [];
                    segmentCounter++;
                    
                    // Important: If this is the very last chunk after Stop, call /live-stop
                    if (!startButton.disabled && stopButton.disabled) {
                        await fetch("/live-stop", { method: "POST" });
                        console.log("Final video merging initiated.");
                        recordingEnded = true; // Mark that recording has ended
                    }
    
                } catch (error) {
                    console.error("Error uploading segment:", error);
                }
            };
    
            mediaRecorder.ondataavailable = (event) => {
                if (event.data.size > 0) {
                    recordedChunks.push(event.data);
                }
            };
    
            let recordedChunks = [];
            mediaRecorder.start(); // Start recording
    
            segmentInterval = setInterval(() => {
                if (mediaRecorder && mediaRecorder.state === "recording") {
                    mediaRecorder.stop();
                    mediaRecorder.start();
                }
            }, 20000); // 20-second chunks
    
            startButton.disabled = true;
            stopButton.disabled = false;
        } catch (err) {
            console.error("Error accessing media devices:", err);
            alert("Camera/mic access denied.");
        }
    });    

    stopButton.addEventListener("click", async () => {
        stopButton.disabled = true;
        startButton.disabled = false;
        recordingEnded = true;
    
        clearInterval(segmentInterval);
        if (mediaRecorder && mediaRecorder.state === "recording") {
            mediaRecorder.requestData(); // flush last chunk
            mediaRecorder.stop();
        }
    
        if (mediaStream) {
            mediaStream.getTracks().forEach(track => track.stop());
            videoElement.srcObject = null;
            mediaStream = null;
        }
    });
});

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
