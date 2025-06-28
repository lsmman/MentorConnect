import base64
from PIL import Image
import io
import os
from app.core.config import settings

ALLOWED_EXT = {"jpg", "jpeg", "png"}

# XSS sanitize util (간단 버전)
def sanitize_text(text: str) -> str:
    return text.replace("<", "&lt;").replace(">", "&gt;")

def save_profile_image(user_id: int, role: str, image_b64: str) -> str:
    try:
        img_bytes = base64.b64decode(image_b64)
        img = Image.open(io.BytesIO(img_bytes))
        if img.format.lower() not in ALLOWED_EXT:
            raise ValueError("Invalid image format")
        if img.width != img.height or not (500 <= img.width <= 1000):
            raise ValueError("Image must be square 500~1000px")
        if len(img_bytes) > 1024 * 1024:
            raise ValueError("Image size must be <= 1MB")
        dir_path = os.path.join(settings.PROFILE_IMG_DIR, role)
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, f"{user_id}.{img.format.lower()}")
        img.save(file_path)
        return file_path
    except Exception as e:
        raise ValueError(f"Image upload failed: {e}")
