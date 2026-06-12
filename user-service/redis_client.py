from fastapi import FastAPI

from database import engine
from models import Base

from redis_client import redis_client

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def root():
    return {
        "status": "running"
    }

@app.get("/cached")
def cached():

    value = redis_client.get("test")

    if value:
        return {
            "source": "redis",
            "data": value
        }

    redis_client.set(
        "test",
        "Hello Redis"
    )

    return {
        "source": "app",
        "data": "Hello Redis"
    }