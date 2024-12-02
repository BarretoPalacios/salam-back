from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    atributes:str
    categori:int
    marca:int
    stock: int


class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    pass

class ProductResponse(ProductBase):
    id: int
    image_url: str
    
