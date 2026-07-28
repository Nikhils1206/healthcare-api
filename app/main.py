from fastapi import FastAPI
from app.config import settings

app = FastAPI()


@app.get("/")
def root():
    return {
        "database": settings.database_url
    }