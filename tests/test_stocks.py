# test_stocks.py — Tests unitaires du service BricoLoc Stock Service

from fastapi.testclient import TestClient
from app.main import app
import json
import os

client = TestClient(app)


# --- Test GET /health ---
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# --- Test GET /stocks ---
# Vérifie que la liste retourne bien 3 entrepôts
def test_get_all_stocks():
    response = client.get("/stocks/")
    assert response.status_code == 200
    assert len(response.json()) == 3


# --- Test GET /stocks/{id} ---
# Vérifie qu'on récupère le bon entrepôt avec ses outils
def test_get_stock_by_id():
    response = client.get("/stocks/1")
    assert response.status_code == 200
    assert response.json()["nom"] == "Paris Nord"
    assert len(response.json()["outils"]) > 0


# --- Test GET /stocks/{id} inexistant ---
def test_get_stock_not_found():
    response = client.get("/stocks/99")
    assert response.status_code == 404


# --- Test POST /stocks/{id}/louer ---
# Vérifie qu'une location diminue le stock disponible
def test_louer_outil():
    # Récupère le stock initial
    avant = client.get("/stocks/1").json()
    dispo_avant = avant["outils"][0]["disponibles"]
    loues_avant = avant["outils"][0]["loues"]

    # Loue l'outil
    response = client.post("/stocks/1/louer", json={"outil_id": 1, "quantite": 1})
    assert response.status_code == 200

    # Vérifie que le stock a bien changé
    apres = client.get("/stocks/1").json()
    assert apres["outils"][0]["disponibles"] == dispo_avant - 1
    assert apres["outils"][0]["loues"] == loues_avant + 1


# --- Test POST /stocks/{id}/retourner ---
# Vérifie qu'un retour augmente le stock disponible
def test_retourner_outil():
    # S'assure qu'il y a au moins un outil en location
    client.post("/stocks/1/louer", json={"outil_id": 1, "quantite": 1})

    avant = client.get("/stocks/1").json()
    dispo_avant = avant["outils"][0]["disponibles"]
    loues_avant = avant["outils"][0]["loues"]

    # Retourne l'outil
    response = client.post("/stocks/1/retourner", json={"outil_id": 1, "quantite": 1})
    assert response.status_code == 200

    # Vérifie que le stock a bien changé
    apres = client.get("/stocks/1").json()
    assert apres["outils"][0]["disponibles"] == dispo_avant + 1
    assert apres["outils"][0]["loues"] == loues_avant - 1


# --- Test stock insuffisant ---
# Vérifie qu'on ne peut pas louer plus que le stock disponible
def test_louer_stock_insuffisant():
    response = client.post("/stocks/1/louer", json={"outil_id": 1, "quantite": 9999})
    assert response.status_code == 400