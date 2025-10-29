from fastapi import APIRouter
from api.v1.endpoints import teachings, parables, events

api_router = APIRouter()

api_router.include_router(teachings.router)
api_router.include_router(parables.router)
api_router.include_router(events.router)
