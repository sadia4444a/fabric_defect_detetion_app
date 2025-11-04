import time
from base64 import b64decode
from io import BytesIO
import os
from pathlib import Path

from PIL import Image
from PIL.Image import open as open_image
from environs import Env
from fastapi import FastAPI ,File, UploadFile
from fastapi.staticfiles import StaticFiles



from domain import Yolo11lDetector
from domain.model import PredictionPayload

from utils import get_logger , save_uploaded_image , save_yolo_annotations , generate_heatmap

env = Env()
env.read_env()
is_debugging = env.bool("DEBUG", False)
logger = get_logger(__name__)

## Create necessary directories


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")


RAW_DIR = os.path.join(STATIC_DIR, "images")
PRED_DIR = os.path.join(STATIC_DIR, "predictions")
HEATMAP_DIR = os.path.join(STATIC_DIR, "annotated_heatmaps")
for folder in [RAW_DIR, PRED_DIR, HEATMAP_DIR]:
    os.makedirs(folder, exist_ok=True)
    logger.info(f"Created folder: {folder}")


app = FastAPI(debug=is_debugging, title="Yolo 11l service")
defect_detector = Yolo11lDetector(weight_path=env.path("YOLO_11L_DETECTOR"))
logger.info("Application initialized")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print("BASE_DIR:", BASE_DIR)
STATIC_DIR = os.path.join(BASE_DIR, "static") 

# Verify folder exists
if not os.path.isdir(STATIC_DIR):
    raise Exception(f"Static folder not found: {STATIC_DIR}")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


 
 
@app.post("/predict")
async def get_prediction(file: UploadFile = File(...)):
    start_time = time.perf_counter()
    
    if not file:
        return {"error": "No file provided"}

    unique_path, unique_name = await save_uploaded_image(file, RAW_DIR)
    image = Image.open(unique_path)

    try:
        
        
        predictions = defect_detector.predict(
            image=image
        )
    except Exception as e:
        logger.exception(e)
        return {
            "prediction": "Failed to predict. Sending empty",
            "confidence": 0.0,
            "heatmap_url": "",
        }
        
    if not predictions:
            return {
            "prediction": [],
            "confidence": 0.0,
            "heatmap_url": "",
        }

    end_time = time.perf_counter()
    logger.info(f"Took {end_time - start_time:.2} seconds")
    
    labels = [pred.bounding_box.label for pred in predictions]
    confidences = [pred.bounding_box.confidence for pred in predictions]

    label_path = save_yolo_annotations(filename=unique_name, predictions=predictions, image_path=unique_path, label_dir=Path(PRED_DIR))

    heatmap_url = generate_heatmap(image_path=unique_path, predictions=predictions, name=unique_name, output_dir=Path(HEATMAP_DIR))

    return {
        "prediction": labels,
        "confidence": confidences,
        "heatmap_url": heatmap_url
    }
    
   