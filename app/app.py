from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
import os
import random
from typing import List, Optional
from pathlib import Path
from app.yandex import yandex_art_request, yandex_lite_request

allowed_origins = [
    "https://demo.adnetworkhoney.com",
]

app = FastAPI()

# Более строгие настройки CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Явное указание методов
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],  # Важно для скачивания файлов
)

# Модель для изображения
class Image(BaseModel):
    id: str
    path: str
    description: str

# Загрузка данных из JSON
def load_images():
    folder_path = "images"
    print(os.getcwd())
    return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

@app.get("/get", response_model=List[Image])
async def get_images(description: Optional[str] = None):
    # Загружаем и проверяем изображения
    text = yandex_lite_request(description)
    print(text)
    images = [
        yandex_art_request(description, random.randint(1, 100))["filename"]
        for _ in range(3)
    ]
    return [
        dict(
            id=id,
            path=id+".jpeg",
            description=text,
        )
        for id in images
    ]

@app.get("/image/{id}")
async def get_image(id: str):
    # Загружаем изображения
    images = load_images()
    ids = [os.path.splitext(f)[0] for f in images]
    print(ids)
    for cur_id in ids:
        if id == cur_id:
            image_path = Path("images/" + cur_id + ".jpeg")
            if image_path.is_file():
                return FileResponse(image_path)
            else:
                raise HTTPException(status_code=404, detail=f"Image file not found")
    
    # Ищем изображение по ID
    raise HTTPException(status_code=404, detail="Image with specified ID not found")