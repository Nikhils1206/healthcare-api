from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.member import router as member_router
from app.routers.claim import router as claim_router
from app.exceptions.handlers import app_exception_handler
from app.exceptions.custom import AppException


app = FastAPI(
    title="Healthcare Claims & Member Management API"
)


app.add_exception_handler(
    AppException,
    app_exception_handler,
)


app.include_router(auth_router)
app.include_router(member_router)
app.include_router(claim_router)


@app.get("/")
def root():
    return {"message": "Healthcare API"}