from uuid import UUID
from datetime import datetime

from fastapi import Form
from pydantic import BaseModel


class BalloonRequest(BaseModel):
    latitude: float
    longitude: float
    detection_time: datetime

    @classmethod
    def as_form(cls, latitude: float = Form(...), longitude: float = Form(...), detection_time: datetime = Form(...)):
        return cls(latitude=latitude, longitude=longitude, detection_time=detection_time)


class BalloonResponse(BaseModel):
    id: UUID
    latitude: float
    longitude: float
    detection_image: str
    detection_time: datetime
    processing_image: str | None = None
    processing_time: datetime | None = None
    processing_state: str
    description: str | None = None


class BalloonsResponse(BaseModel):
    balloons: list[BalloonResponse]
    count: int
