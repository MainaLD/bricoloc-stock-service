# main.py — Point d'entrée de l'application FastAPI BricoLoc Stock Service

from fastapi import FastAPI
from app.routes import stocks

# --- Création de l'application FastAPI ---
app = FastAPI(
    title="BricoLoc Stock Service",
    description="Service de gestion des stocks et entrepôts BricoLoc",
    version="1.0.0"
)

# --- Enregistrement des routes ---
# Tous les endpoints de stocks.py seront accessibles sous /stocks
app.include_router(stocks.router, prefix="/stocks")


# --- GET /health ---
# Health check — permet de vérifier que le service est bien démarré
@app.get("/health")
def health_check():
    return {"status": "ok", "service": "bricoloc-stock-service"}