from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

import sys
import tempfile
import os

# ============================================================
# AI INFERENCE
# ============================================================

sys.path.insert(0, "/home/hp/neuro-twin-ai")

from inference import detect_image


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="Neuro-Twin AI API",
    description="AI Structural Defect Detection API",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# ============================================================
# ROOT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "Neuro-Twin AI Backend is running",
        "status": "online"
    }


# ============================================================
# HEALTH
# ============================================================

@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


# ============================================================
# AI PREDICTION
# ============================================================

@app.post("/predict")
async def predict(
    file: UploadFile = File(...)
):

    # --------------------------------------------------------
    # Validate file
    # --------------------------------------------------------

    if not file.filename:

        return {
            "message": "No file uploaded",
            "detections": []
        }


    # --------------------------------------------------------
    # Read uploaded image
    # --------------------------------------------------------

    contents = await file.read()


    # --------------------------------------------------------
    # Create temporary image
    # --------------------------------------------------------

    suffix = (
        os.path.splitext(file.filename)[1]
        or ".jpg"
    )


    temp_path = None


    try:

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            temp_file.write(contents)

            temp_path = temp_file.name


        # ----------------------------------------------------
        # RUN AI
        # ----------------------------------------------------

        print(
            f"\nAI analyzing: "
            f"{file.filename}"
        )


        detections = detect_image(
            temp_path
        )


        print(
            f"AI returned "
            f"{len(detections)} detections"
        )


        # ----------------------------------------------------
        # RETURN RESULT
        # ----------------------------------------------------

        return {

            "message":
                "AI analysis completed successfully",

            "filename":
                file.filename,

            "detection_count":
                len(detections),

            "detections":
                detections
        }


    except Exception as e:

        print(
            "\nAI ERROR:"
        )

        print(e)


        return {

            "message":
                "AI analysis failed",

            "error":
                str(e),

            "filename":
                file.filename,

            "detection_count":
                0,

            "detections":
                []
        }


    finally:

        # ----------------------------------------------------
        # Delete temporary image
        # ----------------------------------------------------

        if (
            temp_path
            and os.path.exists(temp_path)
        ):

            os.remove(temp_path)
