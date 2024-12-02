import os
import cloudinary
import app.cloudinary.config_cloudinary 
# Import the cloudinary.uploader for uploading assets
from cloudinary.uploader import upload, destroy

def upload_img(nombre,file):
    try: 
        # Subir el archivo a Cloudinary
        response = cloudinary.uploader.upload(
            file,
            folder="img veterinaria",   
            public_id=nombre
        ) 
        
        # Devolver la URL del archivo
        return response.get("secure_url")
   
    except Exception as e:
        print("Error:", e)
        return None
