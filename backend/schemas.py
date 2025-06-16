from pydantic import BaseModel, ConfigDict

class Polygon3DCreate(BaseModel):
    name: str
    color: str
    geom: str

class Polygon3DRead(Polygon3DCreate):
    poly_id: int
    model_config = ConfigDict(from_attributes=True)
