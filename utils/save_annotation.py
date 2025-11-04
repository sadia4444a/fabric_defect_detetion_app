from pathlib import Path
from typing import List, Tuple
from PIL import Image
import os


def save_yolo_annotations(
    filename: str,
    predictions: list,
    image_path: str , 
    label_dir: Path   
) -> str:

    txt_path = label_dir / (Path(filename).stem + ".txt")

    with Image.open(image_path) as img:
        img_width, img_height = img.size

    with open(txt_path, "w") as f:
        for pred in predictions:
            box = pred.bounding_box
            # Convert to YOLO format
            x_center = ((box.x1 + box.x2) / 2) / img_width
            y_center = ((box.y1 + box.y2) / 2) / img_height
            width = (box.x2 - box.x1) / img_width
            height = (box.y2 - box.y1) / img_height

            f.write(f"{box.class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

    return str(txt_path)
