from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import UserDefinedType

Base = declarative_base()

class Polygon3D(Base):
    __tablename__ = "polygon"
    poly_id = Column(Integer, primary_key=True)
    name = Column(String)
    color = Column(String)
    rings = Column(JSONB)

# Database utility
SessionLocal = sessionmaker()

def init_engine(db_url: str):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    SessionLocal.configure(bind=engine)
    return engine
