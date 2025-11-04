import shutil
from datetime import datetime
from uuid import uuid4
from pathlib import Path

async def save_uploaded_image(file, save_dir: str):
    """Save uploaded image to disk with unique UUID + date suffix."""
    today = datetime.now().strftime("%Y%m%d")
    unique_name = f"{uuid4().hex}_{today}.jpg"
    save_path = Path(save_dir) / unique_name

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return save_path, unique_name
