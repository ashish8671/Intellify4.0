from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import sys
import tempfile
import os

# Allow backend to access the working Neuro-Twin AI code
sys.path.insert(0, "/home/hp/neuro-twin-ai")

from inference import detect_image


app = FastAPI(
    title="Neuro-Twin Mesh API",
    description="AI Structural Health Monitoring Backend",
    version="1.0.0"
)


# ==============================
# CORS
# ==============================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ==============================
# ROOT
# ==============================

@app.get("/")
def root():
    return {
        "message": "Neuro-Twin Mesh Backend is running",
        "status": "online"
    }


# ==============================
# HEALTH CHECK
# ==============================

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# ==============================
# AI PREDICTION
# ==============================

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    # Validate file
    if not file.filename:
        return {
            "error": "No file uploaded"
        }

    # Read uploaded image
    contents = await file.read()

    # Create temporary image file
    suffix = os.path.splitext(file.filename)[1] or ".jpg"

    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    ) as temp_file:

        temp_file.write(contents)
        temp_path = temp_file.name

    try:

        # Run YOLO inference
        detections = detect_image(temp_path)

        return {
            "filename": file.filename,
            "message": "AI analysis completed successfully",
            "detection_count": len(detections),
            "detections": detections
        }

    except Exception as e:

        return {
            "filename": file.filename,
            "message": "AI analysis failed",
            "error": str(e),
            "detections": []
        }

    finally:

        # Delete temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)
