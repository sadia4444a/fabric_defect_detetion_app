# 🧵 Fabric Defect Detection App

A **FastAPI application** for detecting defects in fabric images using a YOLO11l model.  
Upload an image via the API and get predicted defects, confidence scores, and annotated heatmaps.  
Bounding box annotations are also saved in **YOLO format** for future model training or annotation tasks.
 
---
## 📁 Dataset Overview
**Dataset:** Textile Defects v3 (from [Roboflow](https://roboflow.com))  
**Images:** 4,326  
**Classes:** `['Hole', 'Knot', 'Line', 'Stain']`  
**Format:** YOLOv8 (train/valid/test splits)

**Preprocessing & Augmentation**
- Resize: 640×640 (fit within)
- 50% chance horizontal flip  
- Random rotation (0°, 90°, 270°)  
- Random shear (−10° to +10°)

These steps increase dataset diversity and reduce overfitting.

---

## ⚙️ Training Setup
**Command used:**
```bash
yolo detect train data=/root/home/projects/yolo/textile_defects_v3/data.yaml \
model=yolo11l.pt epochs=120 imgsz=768 batch=32 device=0,1,3 amp=True 
```

## Framework: Ultralytics YOLO
Why YOLO?
1. Fast and accurate object detection
2. Easy transfer learning from pre-trained weights
3. Real-time performance for industrial inspection

Training completed in ~1.23h over 120 epochs with 3xRTX3090.
Losses decreased steadily, showing good model convergence.

### BoxF1_curve

<img width="2250" height="1500" alt="BoxF1_curve" src="https://github.com/user-attachments/assets/fe1bb4ec-4835-429d-af84-b212eb26b287" />

### confusion_matrix
<img width="3000" height="2250" alt="confusion_matrix" src="https://github.com/user-attachments/assets/9881fb15-9e83-4b5f-b52d-8089f8e41c11" />

### labels
![labels](https://github.com/user-attachments/assets/f2868899-eba9-4321-bcaa-dec7ba3fb909)


###  results 
<img width="2400" height="1200" alt="results" src="https://github.com/user-attachments/assets/8b329f60-ab0f-4ea2-b260-8b4ba44d96c1" />


## Future Improvements
1. Add more diverse fabric textures and lighting conditions
2. Use stronger augmentations (color, brightness, noise)
3. Try higher-resolution inputs (e.g., 1024×1024)
4. Evaluate with real production data
5. Optimize model (quantization, pruning) for edge devices

# Backend 
## 📋 Features
- Upload fabric images and get defect predictions  
- Generates confidence scores for each detected defect  
- Saves YOLO-formatted bounding box annotations for future use  
- Generates heatmaps of detected defects  
- Interactive API documentation via **FastAPI / Swagger UI**

---

## 🛠️ Tech Stack
- **Python >= 3.13**  
- **FastAPI**  
- **Uvicorn**  
- **Ultralytics YOLO**  
- **Pillow** (PIL) for image processing  
- **Environs** for environment variable management  
- **Python Multipart** for file uploads  
- **Poetry** for dependency management  

---

## ⚙️ Installation

### 1️⃣ Clone the repository
```bash
git clone git@github.com:sadia4444a/fabric_defect_detetion_app.git
cd fabric_defect_detetion_app
```

### 2️⃣ Install dependencies
```bash
 poetry install
 source .venv/bin/acivate
```
### 3️⃣ Configure environment

```bash
DEBUG=True
YOLO_11L_DETECTOR=/path/to/your/yolo/weights.pt
```
drive link for model download  and for other info about traning visit runs folder: https://drive.google.com/drive/folders/1dCMKDA7NIRWiyXBaL4-dqcxcK7m7pxgf?usp=sharing

### ▶️ Running the App
```bash
uvicorn application:app --reload
```

### 🌐 Testing the API
  Open the interactive API docs (Swagger UI)
  Predict endpoint: POST /predict

Steps to test:
1. Click Try it out in Swagger UI
2. Upload a fabric image (.jpg or .png)
3. Click Execute
4. Response includes:
 ```bash
{
    "prediction": ["defect_label1", "defect_label2"],
    "confidence": [0.95, 0.87],
    "heatmap_url": "/static/annotated_heatmaps/heatmap_image.png"
}
```
5. YOLO-formatted bounding box annotations are saved in /static/predictions/ for future training or annotation tasks.

# Backend Demo:

https://github.com/user-attachments/assets/cd1a6a5c-6c66-4fa7-a8ff-a87bd01a8e2c


