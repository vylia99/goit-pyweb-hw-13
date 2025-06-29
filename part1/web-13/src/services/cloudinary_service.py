import os
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader

from fastapi import UploadFile


load_dotenv()


cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)


async def upload_image(file: UploadFile, public_id: str) -> str:
    result = cloudinary.uploader.upload(file.file, public_id=public_id, overwrite=True)
    return result['secure_url']
