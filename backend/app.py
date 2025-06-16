from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import json
import os

from .models import Polygon3D, SessionLocal, init_engine
from .schemas import Polygon3DRead, Polygon3DCreate

DB_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:password@localhost/db")
init_engine(DB_URL)

app = FastAPI()

# Dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/polygons", response_model=Polygon3DRead)
def create_polygon(polygon: Polygon3DCreate, db: Session = Depends(get_db)):
    db_polygon = Polygon3D(**polygon.dict())
    db.add(db_polygon)
    db.commit()
    db.refresh(db_polygon)
    return db_polygon

@app.get("/polygons", response_model=list[Polygon3DRead])
def read_polygons(db: Session = Depends(get_db)):
    return db.query(Polygon3D).all()

# Utility to load polygons from a JSON file

def load_from_json(path: str, db: Session):
    with open(path) as f:
        data = json.load(f)
    for item in data.get("polygons", []):
        poly = Polygon3D(name=item.get("name"), color=','.join(map(str, item.get("symbol", {}).get("color", []))), rings=item.get("rings"))
        db.add(poly)
    db.commit()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
