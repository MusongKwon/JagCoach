document.getElementById("fileInput").addEventListener("change", function () {
    const file = this.files[0]
    document.getElementById("fileName").textContent = "Selected file: " + file.name;

    const fileURL = URL.createObjectURL(file); // Create a temporary URL for the file
    const vElement = document.getElementById("vPlayback"); // Get the video element
    const sElement = vElement.querySelector("source"); // Get the <source> tag inside <video>

    sElement.src = fileURL; // New video source
    vElement.load(); // Reload the video to reflect the new source
});