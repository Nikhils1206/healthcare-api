from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.member import router as member_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(member_router)


@app.get("/")
def root():
    return {"message": "Healthcare API"}