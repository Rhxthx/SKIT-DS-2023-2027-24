import os

import cloudinary
import cloudinary.uploader


def is_configured():
    return bool(os.getenv("CLOUDINARY_URL"))


def upload_image(file):
    cloudinary.config(secure=True)
    result = cloudinary.uploader.upload(file, folder="wildlife")
    return result["secure_url"]
