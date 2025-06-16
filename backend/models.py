from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from geoalchemy2 import Geometry

Base = declarative_base()

# --- Building
class Building(Base):
    __tablename__ = "Building"

    buildingID = Column(Integer, primary_key=True)
    name = Column(String)
    lod = Column(Integer)

    floors = relationship(
        "Floor",
        back_populates="building",
        cascade="all, delete-orphan",
    )
    mesh_points = relationship(
        "Mesh_Point",
        back_populates="building",
        cascade="all, delete-orphan",
    )


# --- Floor
class Floor(Base):
    __tablename__ = "Floor"

    floorID = Column(Integer, primary_key=True)
    number = Column(Integer)
    buildingID = Column(Integer, ForeignKey("Building.buildingID"))

    building = relationship("Building", back_populates="floors")
    bodycomps = relationship(
        "BodyComp", back_populates="floor", cascade="all, delete-orphan"
    )
    cylinders = relationship(
        "Cylinder", back_populates="floor", cascade="all, delete-orphan"
    )


# --- BodyComp
class BodyComp(Base):
    __tablename__ = "BodyComp"

    bodyID = Column(Integer, primary_key=True)
    name = Column(String)
    floorID = Column(Integer, ForeignKey("Floor.floorID"))

    floor = relationship("Floor", back_populates="bodycomps")
    faces = relationship(
        "Face", secondary="Face_Body", back_populates="bodycomps"
    )


# --- Color
class Color(Base):
    __tablename__ = "Color"

    colorID = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(String)

    faces = relationship("Face", back_populates="color")


# --- Face
class Face(Base):
    __tablename__ = "Face"

    faceID = Column(Integer, primary_key=True)
    name = Column(String)
    colorID = Column(Integer, ForeignKey("Color.colorID"))

    color = relationship("Color", back_populates="faces")
    nodes = relationship(
        "Node", secondary="Face_Node", back_populates="faces"
    )
    bodycomps = relationship(
        "BodyComp", secondary="Face_Body", back_populates="faces"
    )


# --- Node / Point
class Node(Base):
    __tablename__ = "Node"

    nodeID = Column(Integer, primary_key=True)
    type = Column(String)
    pointID = Column(Integer, ForeignKey("Point.pointID"))

    point = relationship("Point")
    faces = relationship(
        "Face", secondary="Face_Node", back_populates="nodes"
    )
    cylinders = relationship("Cylinder", back_populates="node")


class Point(Base):
    __tablename__ = "Point"

    pointID = Column(Integer, primary_key=True)
    x = Column(Float)
    y = Column(Float)
    z = Column(Float)


# --- Association tables
class Face_Node(Base):
    __tablename__ = "Face_Node"

    faceID = Column(Integer, ForeignKey("Face.faceID"), primary_key=True)
    nodeID = Column(Integer, ForeignKey("Node.nodeID"), primary_key=True)


class Face_Body(Base):
    __tablename__ = "Face_Body"

    bodyID = Column(Integer, ForeignKey("BodyComp.bodyID"), primary_key=True)
    faceID = Column(Integer, ForeignKey("Face.faceID"), primary_key=True)


# --- Cylinder
class Cylinder(Base):
    __tablename__ = "Cylinder"

    cylinderID = Column(Integer, primary_key=True)
    type = Column(String)
    height = Column(Float)
    radius = Column(Float)
    floorID = Column(Integer, ForeignKey("Floor.floorID"))
    nodeID = Column(Integer, ForeignKey("Node.nodeID"))
    colorID = Column(Integer, ForeignKey("Color.colorID"))

    floor = relationship("Floor", back_populates="cylinders")
    node = relationship("Node", back_populates="cylinders")
    color = relationship("Color")


# --- MeshObject & MeshPoint
class Mesh_Object(Base):
    __tablename__ = "Mesh_Object"

    objectID = Column(Integer, primary_key=True)
    filePath = Column(String)

    points = relationship(
        "Mesh_Point", back_populates="mesh_object", cascade="all, delete-orphan"
    )


class Mesh_Point(Base):
    __tablename__ = "Mesh_Point"

    meshPointID = Column(Integer, primary_key=True)
    objectID = Column(Integer, ForeignKey("Mesh_Object.objectID"))
    pointID = Column(Integer, ForeignKey("Point.pointID"))
    buildingID = Column(Integer, ForeignKey("Building.buildingID"))

    mesh_object = relationship("Mesh_Object", back_populates="points")
    point = relationship("Point")
    building = relationship("Building", back_populates="mesh_points")


# --- Polygon 3D
class Polygon3D(Base):
    __tablename__ = "polygon"

    poly_id = Column(Integer, primary_key=True)
    name = Column(String)
    color = Column(String)
    geom = Column(Geometry("POLYGONZ", srid=4326))


# Database utility
SessionLocal = sessionmaker()


def init_engine(db_url: str):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    SessionLocal.configure(bind=engine)
    return engine
