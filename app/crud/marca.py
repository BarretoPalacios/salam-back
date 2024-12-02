from sqlalchemy.orm import Session
from app.models.models import Marca
from app.schemas.marca import MarcaCreate, MarcaUpdate
from fastapi import HTTPException, status

def get_marcas(db: Session, skip: int = 0, limit: int = 10):
    if skip < 0 or limit <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid pagination parameters. 'skip' must be >= 0 and 'limit' > 0." 
        )
    return db.query(Marca).offset(skip).limit(limit).all()

def create_marca(db: Session, marca: MarcaCreate):
    try:
        db_marca = Marca(**marca.model_dump())
        db.add(db_marca)
        db.commit()
        db.refresh(db_marca)
        return db_marca
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating Marca: {str(e)}"
        )

def get_marca(db: Session, marca_id: int):
    if not isinstance(marca_id, int) or marca_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid 'marca_id'. It must be a positive integer."
        )
    marca = db.query(Marca).filter(Marca.id == marca_id).first()
    if not marca:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Marca with id {marca_id} not found."
        )
    return marca

def update_marca(db: Session, marca_id: int, marca: MarcaUpdate):
    if not isinstance(marca_id, int) or marca_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid 'marca_id'. It must be a positive integer."
        )
    db_marca = db.query(Marca).filter(Marca.id == marca_id).first()
    if not db_marca:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Marca with id {marca_id} not found."
        )
    try:
        for key, value in marca.model_dump(exclude_unset=True).items():
            setattr(db_marca, key, value)
        db.commit()
        db.refresh(db_marca)
        return db_marca
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error updating Marca: {str(e)}"
        )

def delete_marca(db: Session, marca_id: int):
    if not isinstance(marca_id, int) or marca_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid 'marca_id'. It must be a positive integer."
        )
    db_marca = db.query(Marca).filter(Marca.id == marca_id).first()
    if not db_marca:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Marca with id {marca_id} not found."
        )
    try:
        db.delete(db_marca)
        db.commit()
        return {"detail": f"Marca with id {marca_id} deleted successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting Marca: {str(e)}"
        )


