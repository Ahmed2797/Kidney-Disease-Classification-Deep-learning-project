from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse,FileResponse
from fastapi.staticfiles import StaticFiles
from project.pipeline.prediction import ImagePredictor
import uvicorn
import shutil
import uuid
import os

app = FastAPI()

# Load model
predictor = ImagePredictor("artifacts/training/model.h5")

# Serve static files
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Serve index.html manually
@app.get("/")
async def root():
    return FileResponse("frontend/index.html")


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        if not file.filename.lower().endswith((".png", ".jpg", ".jpeg")):
            return JSONResponse({"error": "Invalid file type"}, status_code=400)

        temp_filename = f"temp_{uuid.uuid4()}.png"

        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        label, confidence = predictor.predict(temp_filename)

        os.remove(temp_filename)

        return {
            "filename": file.filename,
            "prediction": label,
            "confidence": float(confidence)
        }

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


## uvicorn app:app --reload
