# routes/stocks.py — Endpoints de gestion des stocks BricoLoc

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# Routeur FastAPI — regroupe tous les endpoints /stocks
router = APIRouter()

# --- Données fictives en mémoire ---
# Simule les stocks de 3 entrepôts BricoLoc
stocks = {
    1: {"id": 1, "entrepot": "Paris Nord",    "outils_disponibles": 42, "outils_loues": 8},
    2: {"id": 2, "entrepot": "Lyon Centre",   "outils_disponibles": 27, "outils_loues": 15},
    3: {"id": 3, "entrepot": "Bordeaux Sud",  "outils_disponibles": 35, "outils_loues": 5},
}

# --- Modèle de mise à jour de stock ---
# Définit la structure des données attendues dans le POST
class StockUpdate(BaseModel):
    outils_disponibles: int
    outils_loues: int


# --- GET /stocks ---
# Retourne la liste complète des stocks de tous les entrepôts
@router.get("/")
def get_all_stocks():
    return list(stocks.values())


# --- GET /stocks/{id} ---
# Retourne le stock d'un entrepôt spécifique par son ID
@router.get("/{stock_id}")
def get_stock(stock_id: int):
    if stock_id not in stocks:
        raise HTTPException(status_code=404, detail="Entrepôt introuvable")
    return stocks[stock_id]


# --- POST /stocks/{id} ---
# Met à jour le stock d'un entrepôt (modification en mémoire)
@router.post("/{stock_id}")
def update_stock(stock_id: int, update: StockUpdate):
    if stock_id not in stocks:
        raise HTTPException(status_code=404, detail="Entrepôt introuvable")
    stocks[stock_id]["outils_disponibles"] = update.outils_disponibles
    stocks[stock_id]["outils_loues"] = update.outils_loues
    return {"message": "Stock mis à jour", "stock": stocks[stock_id]}