import cloudinary
# Import the cloudinary.api for managing assets
import cloudinary.api
# Import the cloudinary.uploader for uploading assets
from cloudinary.uploader import upload, destroy

from app.environt.setting import settings

cloudinary.config(
    cloud_name=settings.CLOUD_NAME,
    api_key=settings.CLOUD_KEY,
    api_secret=settings.CLOUD_SECRET,
    secure=True,
    # cloud_name="djiro1win",
    # api_key="718225226485392",
    # api_secret="I-1U7y2S8y7rz93ZbUUMeAbJR9M",
    # secure=True,
)


