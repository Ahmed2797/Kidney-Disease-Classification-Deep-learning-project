const form = document.getElementById("upload-form");
const imageInput = document.getElementById("image");

const previewContainer = document.getElementById("preview-container");
const previewImage = document.getElementById("preview-image");
const overlay = document.getElementById("overlay");

const loader = document.getElementById("loader");
const barContainer = document.getElementById("bar-container");
const bar = document.getElementById("bar");

const result = document.getElementById("result");
const filenameEl = document.getElementById("filename");
const predictionEl = document.getElementById("prediction");
const confidenceEl = document.getElementById("confidence");

const errorDiv = document.getElementById("error");

/* -----------------------------
   1️⃣ Show image immediately after selecting
------------------------------- */
imageInput.addEventListener("change", () => {
  const file = imageInput.files[0];
  if (!file) return;

  errorDiv.textContent = "";
  overlay.style.display = "none";
  barContainer.style.display = "none";
  result.style.display = "none";

  const reader = new FileReader();
  reader.onload = (e) => {
    previewImage.src = e.target.result;   // Set image src
    previewContainer.style.display = "block"; // Show container
  };
  reader.readAsDataURL(file);
});

/* -----------------------------
   2️⃣ Submit form for prediction
------------------------------- */
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const file = imageInput.files[0];
  if (!file) {
    errorDiv.textContent = "Please select an image first.";
    return;
  }

  loader.style.display = "block";
  errorDiv.textContent = "";

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch("/predict", { method: "POST", body: formData });
    if (!res.ok) throw new Error(await res.text());

    const data = await res.json();

    // Overlay prediction text
    overlay.textContent = `${data.prediction} (${(data.confidence*100).toFixed(1)}%)`;
    overlay.style.display = "block";

    // Confidence bar
    bar.style.width = (data.confidence * 100) + "%";
    barContainer.style.display = "block";

    // Textual result
    filenameEl.textContent = data.filename;
    predictionEl.textContent = data.prediction;
    confidenceEl.textContent = (data.confidence * 100).toFixed(2) + "%";
    result.style.display = "block";

  } catch (err) {
    errorDiv.textContent = "Error: " + err.message;
  } finally {
    loader.style.display = "none";
  }
});
