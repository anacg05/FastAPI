from fastapi import FastAPI
from core.db import Base, engine
from core.config import settings
from api.router import api_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION)
app.include_router(api_router)

@app.get("/")
def root():
    return {"msg": "Jesus API is live!"}
