from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.fcm import initialize_fcm
from app.utils import UvicornException, http_exception_handler

app = FastAPI()

initialize_fcm()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api_router, prefix="/api/v1")
app.add_exception_handler(UvicornException, http_exception_handler)
