from sqlalchemy.orm import Session
from app.models.models import User, Base, Category, Marca
from app.auth.auth import get_password_hash
from app.config.database import engine, SessionLocal
from app.environt.setting import settings
# Crear la base de datos si no existe
Base.metadata.create_all(bind=engine)
# Crear sesión
db: Session = SessionLocal()
def create_admin():
    # Verificar si ya existe un usuario administrador
    existing_admin = db.query(User).filter(User.username == settings.ADMIN_USERNAME).first() 
    if existing_admin:
        print("Admin user already exists.")
        return 
    # Crear un usuario administrador manualmente si no existe
    hashed_password = get_password_hash(settings.CREATE_ADMIN_PASSWORD)  
    admin_user = User(
        username=settings.CREATE_ADMIN_USERNAME,
        email=settings.CREATE_ADMIN_EMAIL,
        hashed_password=hashed_password,
        role=settings.CREATE_ADMIN_ROL 
    )

    perro_category = Category(name="Perro")
    db.add(perro_category)
    db.commit()

    gato_category = Category(name="Gato")
    db.add(gato_category)
    db.commit()

    marca_add = Marca(name="Ricocan")
    db.add(marca_add)
    db.commit()

    # Guardar en la base de datos
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    print(f"Admin user created ")
    return 



