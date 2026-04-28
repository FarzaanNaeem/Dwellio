import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import models
from app.api.events import router as events_router
from app.api.feedback import router as feedback_router
from app.api.search import router as search_router
from app.config import settings
from app.db import Base, engine
from app.services.agent import run_agent


app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(search_router)
app.include_router(feedback_router)
app.include_router(events_router)


@app.on_event("startup")
def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


@app.on_event("startup")
async def start_agent() -> None:
    asyncio.create_task(run_agent())


@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.environment,
    }
