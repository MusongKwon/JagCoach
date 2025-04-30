document.getElementById("fileInput").addEventListener("change", function () {
    const file = this.files[0];
    const evaluationResult = document.getElementById("customEvaluationText");
    const evaluationSpinner = document.getElementById("evaluationSpinner");
    evaluationResult.textContent = "Examining presentation...";
    evaluationSpinner.style.display = "block";
  
    if (file) {
        console.log("file found")  
        const formData = new FormData();
        formData.append("rubric_file", file);
  
        fetch("/rubric-evaluate", {method: "POST", body: formData})
        .then(res => res.json())
        .then(data => {
          evaluationResult.textContent = data.custom_evaluation || "No result returned.";
        })
        .catch(err => {
          console.error("Error evaluating rubric:", err);
        })
        .finally(() => {
          evaluationSpinner.style.display = "none";
        });
    }
});