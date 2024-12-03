from sqlalchemy.orm import Session
from app.models.models import Product
from app.schemas.products import ProductUpdate
from fastapi import HTTPException, status

def get_product_with_relations(db: Session, product_id: int):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        return {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "atributes":product.atributes,
            "categori": product.category.name if product.category else None,
            "marca": product.marca.name if product.marca else None,
            "stock": product.stock,
            "image_url": product.image_url,
        }
    return None

def get_products_with_relations(db: Session, skip: int = 0, limit: int = 10):
    products = db.query(Product).offset(skip).limit(limit).all()
    return [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "atributes":product.atributes,
            "categori": product.category.name if product.category else None,
            "marca": product.marca.name if product.marca else None,
            "stock": product.stock,
            "image_url": product.image_url,
        }
        for product in products
    ]

def update_product_with_relations(db: Session, product_id: int, product: ProductUpdate):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        return None
    
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products_by_name(db: Session, name: str, skip: int = 0, limit: int = 10):
    products = db.query(Product).offset(skip).limit(limit).all()
    return [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "atributes": product.atributes,
            "categori": product.category.name if product.category else None,
            "marca": product.marca.name if product.marca else None,
            "stock": product.stock,
            "image_url": product.image_url,
        }
        for product in products
    ]

# Nueva función: Filtrar productos por categoría
def get_products_by_category(db: Session, category_id: int, skip: int = 0, limit: int = 10):
    products = db.query(Product).filter(Product.categori_id == category_id).offset(skip).limit(limit).all()
    return [
        {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "atributes": product.atributes,
            "categori": product.category.name if product.category else None,
            "marca": product.marca.name if product.marca else None,
            "stock": product.stock,
            "image_url": product.image_url,
        }
        for product in products
    ]