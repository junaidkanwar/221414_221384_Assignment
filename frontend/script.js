// File input handling
const imageInput = document.getElementById("image");
const uploadArea = document.getElementById("uploadArea");
const fileName = document.getElementById("fileName");
const previewContainer = document.getElementById("previewContainer");
const preview = document.getElementById("preview");
const result = document.getElementById("result");
const loading = document.getElementById("loading");
const predictBtn = document.getElementById("predictBtn");

// Handle file selection
imageInput.addEventListener("change", function(e) {
    const file = e.target.files[0];
    if (file) {
        fileName.textContent = "Selected: " + file.name;
        showPreview(file);
    }
});

// Drag and drop functionality
uploadArea.addEventListener("dragover", function(e) {
    e.preventDefault();
    uploadArea.classList.add("dragover");
});

uploadArea.addEventListener("dragleave", function() {
    uploadArea.classList.remove("dragover");
});

uploadArea.addEventListener("drop", function(e) {
    e.preventDefault();
    uploadArea.classList.remove("dragover");
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith("image/")) {
        imageInput.files = e.dataTransfer.files;
        fileName.textContent = "Selected: " + file.name;
        showPreview(file);
    }
});

// Show image preview
function showPreview(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        preview.src = e.target.result;
        previewContainer.classList.add("show");
        result.classList.remove("show");
    };
    reader.readAsDataURL(file);
}

// Predict function
function predict() {
    const file = imageInput.files[0];
    if (!file) {
        alert("Please select an image first!");
        return;
    }

    // Show loading state
    loading.classList.add("show");
    result.classList.remove("show");
    predictBtn.disabled = true;
    predictBtn.textContent = "⏳ Processing...";

    const formData = new FormData();
    formData.append("image", file);

    fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        body: formData
    })
    .then(res => res.json())
    .then(data => {
        loading.classList.remove("show");
        predictBtn.disabled = false;
        predictBtn.textContent = "🔍 Predict Action";
        
        if (data.action) {
            result.textContent = "✨ Recognized Action: " + data.action.toUpperCase();
            result.classList.add("show");
            result.classList.remove("error");
        } else if (data.error) {
            result.textContent = "❌ Error: " + data.error;
            result.classList.add("show", "error");
        }
    })
    .catch(err => {
        console.error("Error:", err);
        loading.classList.remove("show");
        predictBtn.disabled = false;
        predictBtn.textContent = "🔍 Predict Action";
        result.textContent = "❌ Error connecting to backend. Make sure the server is running!";
        result.classList.add("show", "error");
    });
}
