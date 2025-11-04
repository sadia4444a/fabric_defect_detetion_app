import cv2
import numpy as np
from PIL import Image
from pathlib import Path

def generate_heatmap(
    image_path: Path,
    predictions: list,
    name: str,
    output_dir: Path,
    blur_strength: int = 25
) -> str:


    # Load image
    image = np.array(Image.open(image_path).convert("RGB"))
    height, width = image.shape[:2]

    heatmap = np.zeros((height, width), dtype=np.float32)


    for pred in predictions:
        x1, y1, x2, y2 = map(int, [pred.bounding_box.x1, pred.bounding_box.y1,
                                    pred.bounding_box.x2, pred.bounding_box.y2])
        conf = float(pred.bounding_box.confidence)
        label = pred.bounding_box.label

        # Update heatmap intensity
        heatmap[y1:y2, x1:x2] += conf

        # Draw rectangle and label text
        # cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # text = f"{label}: {conf:.2f}"
        # cv2.putText(
        #     image, text, (x1, max(0, y1 - 5)),
        #     fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        #     fontScale=1, color=(0, 255, 0), thickness=1
        # )
        
        
        

        # Prepare label text
        text = f"{label}: {conf:.2f}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.6
        thickness = 2

        # Get text size
        (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)
        # Make sure text box doesn’t go outside image
        text_x, text_y = x1, max(0, y1 - text_h - baseline - 4)

        # Draw filled rectangle behind text
        cv2.rectangle(image, (text_x, text_y),
              (text_x + text_w + 4, text_y + text_h + baseline + 4),
              (0, 255, 0), cv2.FILLED, lineType=cv2.LINE_AA)

        # Put text on top of rectangle
        cv2.putText(
            image,
            text,
            (text_x + 2, text_y + text_h + baseline - 2),
            font,
            font_scale,
            (0, 0, 0),  # text color
            thickness
        )


    
    if blur_strength % 2 == 0:
        blur_strength += 1
    heatmap = cv2.GaussianBlur(heatmap, (blur_strength, blur_strength), 0)
    if heatmap.max() > 0:
        heatmap = np.clip(heatmap / heatmap.max(), 0, 1)

    heatmap_color = cv2.applyColorMap((heatmap * 255).astype(np.uint8), cv2.COLORMAP_JET)

    # Overlay heatmap on original image
    overlay = cv2.addWeighted(image, 0.6, heatmap_color, 0.4, 0)

    # Save heatmap
    heatmap_name = f"{Path(name).stem}_heatmap.jpg"
    save_path = output_dir / heatmap_name
    cv2.imwrite(str(save_path), overlay)
    #make http url
    return f"http://localhost:8000/static/annotated_heatmaps/{heatmap_name}"
