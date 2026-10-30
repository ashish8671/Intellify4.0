from datetime import datetime, date

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    DateTime,
    ForeignKey,
    JSON,
)

from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)

    email = Column(
        String(150),
        unique=True,
        index=True,
        nullable=False
    )

    password_hash = Column(String(255), nullable=False)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    buildings = relationship(
        "Building",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    inspections = relationship(
        "Inspection",
        back_populates="inspector",
        cascade="all, delete-orphan"
    )


class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    building_name = Column(
        String(200),
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    owner = relationship(
        "User",
        back_populates="buildings"
    )

    inspections = relationship(
        "Inspection",
        back_populates="building",
        cascade="all, delete-orphan"
    )


class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    building_id = Column(
        Integer,
        ForeignKey("buildings.id"),
        nullable=False
    )

    inspection_date = Column(
        Date,
        default=date.today,
        nullable=False
    )

    location = Column(
        String(255),
        nullable=False
    )

    image_path = Column(
        String(500),
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    inspector = relationship(
        "User",
        back_populates="inspections"
    )

    building = relationship(
        "Building",
        back_populates="inspections"
    )

    detections = relationship(
        "Detection",
        back_populates="inspection",
        cascade="all, delete-orphan"
    )


class Detection(Base):
    __tablename__ = "detections"

    id = Column(Integer, primary_key=True, index=True)

    inspection_id = Column(
        Integer,
        ForeignKey("inspections.id"),
        nullable=False
    )

    label = Column(
        String(100),
        nullable=False
    )

    confidence = Column(
        Float,
        nullable=False
    )

    severity = Column(
        String(50),
        nullable=False
    )

    priority = Column(
        String(50),
        nullable=True
    )

    status = Column(
        String(50),
        default="Detected"
    )

    repair_method = Column(
        String(255),
        nullable=True
    )

    material = Column(
        String(255),
        nullable=True
    )

    estimated_time = Column(
        String(100),
        nullable=True
    )

    estimated_cost = Column(
        Float,
        nullable=True
    )

    bbox = Column(
        JSON,
        nullable=True
    )

    segmentation = Column(
        JSON,
        nullable=True
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    inspection = relationship(
        "Inspection",
        back_populates="detections"
    )
