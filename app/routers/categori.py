from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.categori import CategoryCreate,CategoryUpdate,CategoryResponse
from app.crud.categori import *
from app.config.database import SessionLocal
from app.auth.auth import oauth2_scheme

router = APIRouter(tags=["Categorias Endpoints"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=list[CategoryResponse])
def read_categories(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_categories(db, skip=skip, limit=limit)  

@router.post("/", response_model=CategoryResponse)
def create_new_category(categoria: CategoryCreate, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    return create_category(db, categoria)

@router.get("/{category_id}", response_model=CategoryResponse)
def read_product(category_id: int, db: Session = Depends(get_db)):
    db_category = get_category(db, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_category

@router.put("/{category_id}", response_model=CategoryResponse)
def update_existing_product(category_id: int, category: CategoryUpdate, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    return update_category(db, category_id, category)

@router.delete("/{category_id}")
def delete_existing_product(category_id: int, db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    delete_category(db, category_id)
    return {"detail": "category deleted"}