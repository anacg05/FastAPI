from fastapi import FastAPI
from core.db import Base, engine
from api.router import api_router

app = FastAPI(title="Jesus API", version="0.1.0")

# Cria as tabelas (apenas na primeira vez)
Base.metadata.create_all(bind=engine)

# Inclui as rotas
app.include_router(api_router)
