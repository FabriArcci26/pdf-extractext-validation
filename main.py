"""Validation service FastAPI application: bootstrap y montaje de componentes."""

from fastapi import FastAPI
from shared.web.cors import add_cors, parse_origins

from routes import router
from settings import get_settings

settings = get_settings()

app = FastAPI(title="PDF Validation Service", version="1.0.0")

# CORS explícito por entorno (sin comodín).
add_cors(app, origins=parse_origins(settings.cors_origins))


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "validation-service"}


app.include_router(router)
