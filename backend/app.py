from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import json
import os

from .models import Polygon3D, SessionLocal, init_engine
from .schemas import Polygon3DRead, Polygon3DCreate
from geoalchemy2.elements import WKTElement

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
    data = polygon.dict()
    if "geom" in data:
        data["geom"] = WKTElement(data["geom"], srid=4326)
    db_polygon = Polygon3D(**data)
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
    def rings_to_wkt(rings: list[list[list[float]]]) -> str:
        def ring_str(r):
            return ", ".join(f"{p[0]} {p[1]} {p[2]}" for p in r)
        inner = ", ".join(f"({ring_str(r)})" for r in rings)
        return f"POLYGON Z ({inner})"

    for item in data.get("polygons", []):
        color = ",".join(map(str, item.get("symbol", {}).get("color", [])))
        rings = item.get("rings", [])
        wkt = rings_to_wkt(rings)
        poly = Polygon3D(
            name=item.get("name"),
            color=color,
            geom=WKTElement(wkt, srid=4326),
        )
        db.add(poly)
    db.commit()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)