# 🧵 Fabric Defect Detection App

A **FastAPI application** for detecting defects in fabric images using a YOLOv11 model.  
Upload an image via the API and get predicted defects, confidence scores, and annotated heatmaps.  
Bounding box annotations are also saved in **YOLO format** for future model training or annotation tasks.

---

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


