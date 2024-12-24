import os
import io
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, APIRouter, File, UploadFile, HTTPException
from ultralytics import YOLO
from fastapi.responses import JSONResponse
from PIL import Image
import torch
from pathlib import Path
from app.api.v1.controller.yolo import yolo_prediction
import traceback

LOCAL_ARTIFACTS = Path("./DATA/artifacts")
LOCAL_CAPTURED = Path("./DATA/captured/yolo")

UPLOAD_DIR = LOCAL_CAPTURED / "uploads"
ANNOTATED_DIR = LOCAL_CAPTURED / "annotated"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(ANNOTATED_DIR, exist_ok=True)

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_path = LOCAL_ARTIFACTS / "yolo" / "yolo11x.pt"


def load_model(model_path: str) -> YOLO:
    """Load YOLO model from file path"""
    try:
        model = YOLO(model_path)
        if torch.cuda.is_available():
            model.to(DEVICE)
        return model
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading model: {str(e)}")


models = {}
@asynccontextmanager
async def lifespan(app: FastAPI):
    models["yolo"] = load_model(model_path)
    yield
    models.clear()

router = APIRouter(lifespan=lifespan)

@router.post("/detect/")
async def detect_objects(file: UploadFile = File(...)):
    """
    Endpoint for object detection on uploaded image
    
    :param file: Uploaded image file
    :return: JSON response with detection results and file paths
    """
    try:
        # Generate unique filename
        original_filename = file.filename
        unique_filename = f"{uuid.uuid4()}_{original_filename}"
        
        # Full paths for saving
        original_filepath = os.path.join(UPLOAD_DIR, unique_filename)
        
        # Read and save original image
        contents = await file.read()
        with open(original_filepath, "wb") as f:
            f.write(contents)
        
        # Open image for detection
        image = Image.open(io.BytesIO(contents))

        # Perform object detection
        detections = yolo_prediction(
            load_model(model_path),
            image
        )
        
        return JSONResponse(content={
            'detections': detections,
            'total_objects': len(detections)
        })
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{traceback.format_exc()}")
