# main.py — Point d'entrée de l'application FastAPI BricoLoc Stock Service

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routes import stocks
import os

# --- Création de l'application FastAPI ---
app = FastAPI(
    title="BricoLoc Stock Service",
    description="Service de gestion des stocks et entrepôts BricoLoc",
    version="2.0.0"
)

# --- Dossiers statiques et templates ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# --- Enregistrement des routes API ---
app.include_router(stocks.router, prefix="/stocks")


# --- GET / ---
# Page principale de l'IHM
@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# --- GET /health ---
# Health check du service
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "bricoloc-stock-service"}