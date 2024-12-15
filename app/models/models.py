from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.config.database import Base
from sqlalchemy.orm import relationship

class User(Base): 
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user") 

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    atributes = Column(String)
    categori_id = Column(Integer, ForeignKey("category.id"))  # Clave foránea a Category
    marca_id = Column(Integer, ForeignKey("marca.id"))        # Clave foránea a Marca
    stock = Column(Integer)
    image_url = Column(String)
    # Relaciones
    category = relationship("Category", back_populates="products")
    marca = relationship("Marca", back_populates="products")

class Marca(Base):
    __tablename__ = "marca"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    # Relación inversa
    products = relationship("Product", back_populates="marca")

class  Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    # Relación inversa
    products = relationship("Product", back_populates="category")