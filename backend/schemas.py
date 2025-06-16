from pydantic import BaseModel
from typing import List

class Polygon3DCreate(BaseModel):
    name: str
    color: str
    rings: List[List[float]]

class Polygon3DRead(Polygon3DCreate):
    poly_id: int
    class Config:
        orm_mode = True
