from fastapi import APIRouter, Depends, HTTPException, File, Form, UploadFile, status
from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.models.models import Product
from app.schemas.products import ProductResponse,ProductUpdate,ProductCreate
from app.cloudinary.function_cloudinary import upload_img
from app.crud.product import *

router = APIRouter(tags=["Productos endpoints"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
async def create_product_with_image(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    atributes: str = Form(...),
    stock: int = Form(...),
    categori_id: int = Form(...),
    marca_id: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    response =  upload_img(name,file.file)

    # Crear el producto en la base de datos
    new_product = Product(
        name=name,
        description=description,
        price=price,
        atributes=atributes,
        stock=stock,
        categori_id=categori_id,
        marca_id=marca_id,
        image_url=response,
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product

# Obtener todos los productos con categorías y marcas
@router.get("/")
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_products_with_relations(db, skip=skip, limit=limit)

# Obtener un producto específico con su categoría y marca
@router.get("/{product_id}")
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product_with_relations(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Obtener productos por categoria
@router.post("/{category_id}")
def search_product_by_category( db: Session = Depends(get_db) ,category_id: int = 0, skip: int = 0, limit: int = 10):
    product = get_products_by_category(db, category_id,skip=skip,limit=limit)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.get("/buscar")
def buscar_prod(name:str, skip:int=0,limit:int=0 ,db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.name.ilike(f"%{name}%")).offset(skip).limit(limit).all()
    if not products:
        raise HTTPException(status_code=404, detail="Product not found")
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


# elimina un producto en la base ded atos
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found."
        )
    try:
        db.delete(db_product)
        db.commit()
        return {"detail": f"Product with id {product_id} deleted successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error deleting Product: {str(e)}"
        )
   
    
@router.put("/{product_id}")
async def update_product_with_image(
    product_id: int,
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    atributes: str = Form(...),
    stock: int = Form(...),
    categori_id: int = Form(...),
    marca_id: int = Form(...),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    # Buscar el producto por ID
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found."
        )
    
    # Subir la imagen si se proporciona
    if file:
        image_url = upload_img(name, file.file)
        if not image_url:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to upload the image."
            )
        db_product.image_url = image_url

    # Actualizar los campos del producto
    db_product.name = name
    db_product.description = description
    db_product.price = price
    db_product.atributes = atributes
    db_product.stock = stock
    db_product.categori_id = categori_id
    db_product.marca_id = marca_id

    # Guardar cambios en la base de datos
    db.commit()
    db.refresh(db_product)

    # Respuesta
    return {
        "message": "Product updated successfully",
        "product": {
            "id": db_product.id,
            "name": db_product.name,
            "description": db_product.description,
            "price": db_product.price,
            "atributes": db_product.atributes,
            "stock": db_product.stock,
            "category_id": db_product.categori_id,
            "marca_id": db_product.marca_id,
            "image_url": db_product.image_url,
        },
    }