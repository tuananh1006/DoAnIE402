from pydantic import BaseModel

class Polygon3DCreate(BaseModel):
    name: str
    color: str
    geom: str

class Polygon3DRead(Polygon3DCreate):
    poly_id: int
    class Config:
        orm_mode = True
