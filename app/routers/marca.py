from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.marca import MarcaCreate , MarcaResponse , MarcaUpdate
from app.crud.marca import *
from app.config.database import SessionLocal
from app.auth.auth import oauth2_scheme

router = APIRouter(tags=["Marca Endpoints"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[MarcaResponse])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_marcas(db, skip=skip, limit=limit)  

@router.post("/", response_model=MarcaResponse)
def create_new_category(marca: MarcaCreate, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    return create_marca(db, marca)

@router.get("/{marca_id}", response_model=MarcaResponse)
def read_product(marca_id: int, db: Session = Depends(get_db)):
    db_category = get_marca(db, marca_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_category

@router.put("/{marca_id}", response_model=MarcaResponse)
def update_existing_product(marca_id: int, marca: MarcaUpdate, db: Session = Depends(get_db),    token: str = Depends(oauth2_scheme)):
    return update_marca(db, marca_id, marca)

@router.delete("/{marca_id}")
def delete_existing_product(marca_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    
    return delete_marca(db, marca_id)