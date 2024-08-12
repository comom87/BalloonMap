from uuid import UUID
from datetime import datetime

from fastapi import Form
from pydantic import BaseModel


class BalloonRequest(BaseModel):
    address: str
    detection_time: datetime

    @classmethod
    def as_form(cls, address: str = Form(...), detection_time: datetime = Form(...)):
        return cls(address=address, detection_time=detection_time)


class BalloonResponse(BaseModel):
    id: UUID
    latitude: float
    longitude: float
    address: str
    detection_image: str
    detection_time: datetime
    processing_image: str | None = None
    processing_time: datetime | None = None
    processing_state: str
    description: str | None = None
