from fastapi import APIRouter

from app.api.balloon.router import router as balloon_router

api_router = APIRouter()
api_router.include_router(balloon_router, prefix="/balloons")