from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.models.models import User
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.auth import verify_password, get_password_hash, create_access_token, oauth2_scheme, verify_token
from datetime import timedelta

router = APIRouter(tags=["Usuarios endpoints"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/userme")
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    # Verifica el token y obtiene el nombre de usuario
    username = verify_token(token)  
    user = db.query(User).filter(User.username == username).first() 
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    # Devuelve información relevante del usuario (como su rol y correo)
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    }

@router.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username}, expires_delta=timedelta(minutes=30))
    return {"access_token": access_token, "token_type": "bearer"}