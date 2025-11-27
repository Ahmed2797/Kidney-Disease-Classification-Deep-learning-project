const form = document.getElementById('upload-form');
const resultSection = document.getElementById('result');
const errorDiv = document.getElementById('error');

form.addEventListener('submit', async (e) => {
  e.preventDefault();

  errorDiv.textContent = "";
  resultSection.style.display = "none";

  const fileInput = document.getElementById('image');

  if (!fileInput.files.length) {
    errorDiv.textContent = "Please select an image file.";
    return;
  }

  const file = fileInput.files[0];
  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch("/predict", {
      method: "POST",
      body: formData,
    });

    if (!res.ok) {
      const err = await res.text();
      throw new Error(err || `HTTP ${res.status}`);
    }

    const data = await res.json();

    document.getElementById("filename").textContent = data.filename;
    document.getElementById("prediction").textContent = data.prediction;
    document.getElementById("confidence").textContent = data.confidence.toFixed(3);

    resultSection.style.display = "block";

  } catch (err) {
    errorDiv.textContent = "Error: " + err.message;
  }
});
