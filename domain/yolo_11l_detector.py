from pathlib import Path
from typing import List

import numpy as np
from PIL import Image
from ultralytics import YOLO
import torch

from utils import get_logger
from .model import BoundingBox, Prediction
from .model.defect_labels import DefectLabel

logger = get_logger(__name__)

CLASS_ID_TO_LABEL = {
    0: DefectLabel.hole,
    1: DefectLabel.knot,
    2: DefectLabel.line,
    3: DefectLabel.stain,
}


class Yolo11lDetector:
    def __init__(self, weight_path: Path):
        if not weight_path.exists():
            raise RuntimeError(f"Invalid model path. Given {weight_path.absolute()}")

        self._model = YOLO(model=weight_path)
        self._device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self._model.to(self._device)

        logger.info(f"Model loaded to {self._device}")
        logger.info("YOLO 11l  detection predictor initialized")

    def predict(self, image: Image) -> List[Prediction]:
        logger.debug(f"Image of shape ({image.size}) to predict detections")

        try:
            prediction = self._model.predict(source=np.array(image))
        except Exception as e:
            logger.exception(e)
            return []

        boxes = prediction[0].boxes
        if boxes is None or len(boxes) == 0:
            return []

        results: List[Prediction] = []

        predicted_boxes = boxes.xyxy.cpu().numpy()
        predicted_classes = boxes.cls.cpu().numpy()
        predicted_scores = boxes.conf.cpu().numpy()

        for box, class_id, score in zip(predicted_boxes, predicted_classes, predicted_scores):
            x1, y1, x2, y2 = map(int, box)

            result = Prediction(
                bounding_box=BoundingBox(
                    x1=x1,
                    y1=y1,
                    x2=x2,
                    y2=y2,
                    class_id=int(class_id),
                    confidence=float(score),
                    label=CLASS_ID_TO_LABEL[class_id].value
                ),
                image=image,
            )
            results.append(result)

        logger.info(f"Total detections returned: {len(results)}")
        return results
