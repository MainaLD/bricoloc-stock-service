# stocks.py — Endpoints de gestion des stocks BricoLoc
# Les données sont lues et écrites dans app/data.json

import json
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Chemin vers le fichier de données fictives
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data.json")


# --- Fonctions utilitaires lecture / écriture JSON ---

def lire_donnees():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def ecrire_donnees(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# --- Modèle de location d'un outil ---
class LocationOutil(BaseModel):
    outil_id: int
    quantite: int = 1


# --- GET /stocks ---
# Retourne la liste de tous les entrepôts avec leurs outils
@router.get("/")
def get_all_stocks():
    data = lire_donnees()
    return data["entrepots"]


# --- GET /stocks/{id} ---
# Retourne un entrepôt spécifique avec ses outils
@router.get("/{entrepot_id}")
def get_stock(entrepot_id: int):
    data = lire_donnees()
    for entrepot in data["entrepots"]:
        if entrepot["id"] == entrepot_id:
            return entrepot
    raise HTTPException(status_code=404, detail="Entrepôt introuvable")


# --- POST /stocks/{id}/louer ---
# Simule la location d'un outil dans un entrepôt
@router.post("/{entrepot_id}/louer")
def louer_outil(entrepot_id: int, location: LocationOutil):
    data = lire_donnees()
    for entrepot in data["entrepots"]:
        if entrepot["id"] == entrepot_id:
            for outil in entrepot["outils"]:
                if outil["id"] == location.outil_id:
                    if outil["disponibles"] < location.quantite:
                        raise HTTPException(
                            status_code=400,
                            detail=f"Stock insuffisant. Disponibles : {outil['disponibles']}"
                        )
                    outil["disponibles"] -= location.quantite
                    outil["loues"] += location.quantite
                    ecrire_donnees(data)
                    return {
                        "message": f"Location enregistrée pour {outil['nom']}",
                        "outil": outil,
                        "entrepot": entrepot["nom"]
                    }
            raise HTTPException(status_code=404, detail="Outil introuvable")
    raise HTTPException(status_code=404, detail="Entrepôt introuvable")


# --- POST /stocks/{id}/retourner ---
# Simule le retour d'un outil dans un entrepôt
@router.post("/{entrepot_id}/retourner")
def retourner_outil(entrepot_id: int, location: LocationOutil):
    data = lire_donnees()
    for entrepot in data["entrepots"]:
        if entrepot["id"] == entrepot_id:
            for outil in entrepot["outils"]:
                if outil["id"] == location.outil_id:
                    if outil["loues"] < location.quantite:
                        raise HTTPException(
                            status_code=400,
                            detail=f"Retour impossible. En location : {outil['loues']}"
                        )
                    outil["disponibles"] += location.quantite
                    outil["loues"] -= location.quantite
                    ecrire_donnees(data)
                    return {
                        "message": f"Retour enregistré pour {outil['nom']}",
                        "outil": outil,
                        "entrepot": entrepot["nom"]
                    }
            raise HTTPException(status_code=404, detail="Outil introuvable")
    raise HTTPException(status_code=404, detail="Entrepôt introuvable")