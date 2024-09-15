import ssl
import uuid

import boto3
import certifi
from fastapi import UploadFile, Form
from geopy import Nominatim, geocoders
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app import s3config
from app.api.balloon.schema import BalloonRequest, BalloonResponse, BalloonsResponse, \
    NotificationRegistrationTokenRequest
from app.fcm import initialize_fcm, send_notification
from app.models import CCTVBalloon, CCTV, ReportedBalloon
from app.utils import UvicornException

registration_token = None


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

    reported_balloons = db.query(ReportedBalloon).all()

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


def create_cctv_balloon(request: BalloonRequest, detection_image: UploadFile, db: Session):
    cctv = db.query(CCTV).filter(and_(CCTV.latitude == request.latitude, CCTV.longitude == request.longitude)).first()

    if not cctv:
        cctv = CCTV(
            latitude=request.latitude,
            longitude=request.longitude
        )

        db.add(cctv)
        db.commit()

    detection_image_url = s3config.upload_file(detection_image)

    new_cctv_balloon = CCTVBalloon(
        id=uuid.uuid4(),
        cctv=cctv,
        detection_image=detection_image_url,
        detection_time=request.detection_time
    )

    db.add(new_cctv_balloon)
    db.commit()


def create_reported_balloon(request: BalloonRequest, detection_image: UploadFile, db: Session):
    # context = ssl.create_default_context(cafile=certifi.where())
    # geocoders.options.default_ssl_context = context
    #
    # geolocator = Nominatim(user_agent="BalloonMap")
    # location = geolocator.geocode(request.address)

    detection_image_url = s3config.upload_file(detection_image)

    new_reported_balloon = ReportedBalloon(
        id=uuid.uuid4(),
        latitude=request.latitude,
        longitude=request.longitude,
        detection_image=detection_image_url,
        detection_time=request.detection_time
    )

    db.add(new_reported_balloon)
    db.commit()


def create_notification_registration_token(request: NotificationRegistrationTokenRequest):
    global registration_token
    registration_token = request.registration_token


def read_notification():
    global registration_token
    send_notification(registration_token)
