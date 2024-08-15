import uuid
from uuid import UUID

from sqlalchemy import Column, Integer, Double, String, Text, Enum, DateTime, BINARY, ForeignKey
from sqlalchemy.orm import relationship

from app.enum import ProcessingState
from app.database import Base

class CCTV(Base):
    __tablename__ = "cctv"

    id = Column(Integer, primary_key=True)
    latitude = Column(Double, nullable=False)
    longitude = Column(Double, nullable=False)

    cctv_balloon = relationship("CCTVBalloon", backref="cctv_balloons")


class CCTVBalloon(Base):
    __tablename__ = "cctv_balloon"

    id = Column(String(36), primary_key=True)
    cctv_id = Column(Integer, ForeignKey("cctv.id"))
    detection_image = Column(String(255), nullable=False)
    processing_image = Column(String(255), nullable=True)
    detection_time = Column(DateTime, nullable=False)
    processing_time = Column(DateTime, nullable=True)
    processing_state = Column(Enum(ProcessingState), nullable=False, default=ProcessingState.PENDING)
    description = Column(Text, nullable=True)


class ReportedBalloon(Base):
    __tablename__ = "reported_balloon"

    id = Column(String(36), primary_key=True)
    latitude = Column(Double, nullable=False)
    longitude = Column(Double, nullable=False)
    detection_image = Column(String(255), nullable=False)
    processing_image = Column(String(255), nullable=True)
    detection_time = Column(DateTime, nullable=False)
    processing_time = Column(DateTime, nullable=True)
    processing_state = Column(Enum(ProcessingState), nullable=False, default=ProcessingState.PENDING)
    description = Column(Text, nullable=True)
