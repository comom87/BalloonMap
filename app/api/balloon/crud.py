import ssl
import uuid

import boto3
import certifi
from fastapi import UploadFile, Form
from geopy import Nominatim, geocoders
from sqlalchemy.orm import Session

from app.api.balloon.schema import BalloonRequest, BalloonResponse, BalloonsResponse
from app.models import CCTVBalloon, CCTV, ReportedBalloon
from app.utils import UvicornException


def read_balloons(db: Session):
    cctv_balloons = db.query(
        CCTVBalloon.id,
        CCTV.latitude,
        CCTV.longitude,
        CCTVBalloon.detection_image,
        CCTVBalloon.detection_time,
        CCTVBalloon.processing_image,
        CCTVBalloon.processing_time,
        CCTVBalloon.processing_state,
        CCTVBalloon.description
    ).join(CCTV, CCTVBalloon.cctv_id == CCTV.id
           ).all()
    if not cctv_balloons:
        raise UvicornException(status_code=400, message="풍선이 존재하지 않습니다.")

    reported_balloons = db.query(ReportedBalloon).all()
    if not reported_balloons:
        raise UvicornException(status_code=400, message="풍선이 존재하지 않습니다.")

    balloons = cctv_balloons + reported_balloons

    data = BalloonsResponse(
        balloons=[BalloonResponse(
            id=balloon.id,
            latitude=balloon.latitude,
            longitude=balloon.longitude,
            detection_image=balloon.detection_image,
            detection_time=balloon.detection_time,
            processing_image=balloon.processing_image,
            processing_time=balloon.processing_time,
            processing_state=balloon.processing_state.value,
            description=balloon.description
        ) for balloon in balloons],
        count=len(balloons)
    )

    return data


def read_balloon(id: str, db: Session):
    balloon = db.query(
        CCTVBalloon.id,
        CCTV.latitude,
        CCTV.longitude,
        CCTVBalloon.detection_image,
        CCTVBalloon.detection_time,
        CCTVBalloon.processing_image,
        CCTVBalloon.processing_time,
        CCTVBalloon.processing_state,
        CCTVBalloon.description
    ).join(CCTV, CCTVBalloon.cctv_id == CCTV.id
           ).filter(CCTVBalloon.id == id
                    ).first()

    if not balloon:
        balloon = db.query(ReportedBalloon).filter(ReportedBalloon.id == id).first()

    if not balloon:
        raise UvicornException(status_code=400, message="풍선이 존재하지 않습니다.")

    data = BalloonResponse(
        id=balloon.id,
        latitude=balloon.latitude,
        longitude=balloon.longitude,
        detection_image=balloon.detection_image,
        detection_time=balloon.detection_time,
        processing_image=balloon.processing_image,
        processing_time=balloon.processing_time,
        processing_state=balloon.processing_state.value,
        description=balloon.description
    )

    return data


def create_reported_balloon(request: BalloonRequest, detection_image: UploadFile, db: Session):
    # context = ssl.create_default_context(cafile=certifi.where())
    # geocoders.options.default_ssl_context = context
    #
    # geolocator = Nominatim(user_agent="BalloonMap")
    # location = geolocator.geocode(request.address)

    new_reported_balloon = ReportedBalloon(
        id=uuid.uuid4(),
        latitude=request.longitude,
        longitude=request.longitude,
        detection_image="detection_image",
        detection_time=request.detection_time
    )

    db.add(new_reported_balloon)
    db.commit()
