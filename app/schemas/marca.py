from pydantic import BaseModel

class MarcaBase(BaseModel):
    name: str

class MarcaCreate(MarcaBase):
    pass

class MarcaUpdate(BaseModel):
    name: str

class MarcaResponse(MarcaBase):
    id: int