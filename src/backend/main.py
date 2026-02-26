from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models.tasks import Base
from database import engine

from routers import tasks


app = FastAPI(
    title="Mark Door Coding Interview API",
    description="Markdoor コーディングテスト TODOアプリケーション API",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)


app.include_router(tasks.router)


@app.get("/")
def read_root():
    return {"message": "Hello World!"}
