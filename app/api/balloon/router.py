from fastapi import APIRouter, Depends, File, UploadFile, Form, Body
from sqlalchemy.orm import Session

from app.api.balloon import crud
from app.api.balloon.schema import BalloonRequest, NotificationRegistrationTokenRequest
from app.database import get_db
from app.utils import Response

router = APIRouter()


@router.get("/", response_model=Response)
def get_balloons(db: Session = Depends(get_db)):
    balloons = crud.read_balloons(db)
    return Response(success=True, data=balloons, error=None)


@router.get("/{id}", response_model=Response)
def get_balloon(id: str, db: Session = Depends(get_db)):
    balloon = crud.read_balloon(id, db)
    return Response(success=True, data=balloon, error=None)


@router.post("/cctv-balloons", response_model=Response)
def post_reported_balloon(request: BalloonRequest = Depends(BalloonRequest.as_form),
                          detection_image: UploadFile = File(...), db: Session = Depends(get_db)):
    crud.create_cctv_balloon(request, detection_image, db)
    return Response(success=True, data=None, error=None)


@router.post("/reported-balloons", response_model=Response)
def post_reported_balloon(request: BalloonRequest = Depends(BalloonRequest.as_form),
                          detection_image: UploadFile = File(...), db: Session = Depends(get_db)):
    crud.create_reported_balloon(request, detection_image, db)
    return Response(success=True, data=None, error=None)


@router.post("/notifications", response_model=Response)
def post_notifications():
    crud.create_notification()
    return Response(success=True, data=None, error=None)


@router.post("/notifications/token", response_model=Response)
def post_notification_registration_token(request: NotificationRegistrationTokenRequest):
    crud.create_notification_registration_token(request)
    return Response(success=True, data=None, error=None)
