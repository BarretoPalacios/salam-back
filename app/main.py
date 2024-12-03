from fastapi import FastAPI,Query,Depends
from contextlib import asynccontextmanager
from app.models.models import Base
from app.config.database import engine
from app.auth.create_admin import create_admin
from typing import Optional
from app.routers import marca,categori,product,user
from fastapi.middleware.cors import CORSMiddleware


from app.auth.auth import oauth2_scheme 

# Función lifespan (inicio y fin del servidos)
async def lifespan(app: FastAPI):
    # Ejecutar la creación de las tablas al inicio
    print("Creando tablas en la base de datos...")
    create_admin()
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas correctamente.")    
    # Yield permite que FastAPI ejecute el código después de esto cuando termine
    yield
    # Aquí puedes poner el código de limpieza al finalizar la vida útil de la app
    print("Aplicación cerrada, limpiando recursos...")

app = FastAPI(lifespan=lifespan)  

# rutas incluidas
app.include_router(user.router,prefix="/user")
app.include_router(product.router, prefix="/products")
app.include_router(marca.router, prefix="/marcas")
app.include_router(categori.router, prefix="/categories")

app.add_middleware( 
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers   
)




