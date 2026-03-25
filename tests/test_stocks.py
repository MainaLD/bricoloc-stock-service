# test_stocks.py — Tests unitaires du service BricoLoc Stock Service

from fastapi.testclient import TestClient
from app.main import app

# Client de test FastAPI — simule des requêtes HTTP sans vrai serveur
client = TestClient(app)


# --- Test GET /health ---
# Vérifie que le service répond bien et retourne status: ok
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# --- Test GET /stocks ---
# Vérifie que la liste des stocks retourne bien 3 entrepôts
def test_get_all_stocks():
    response = client.get("/stocks/")
    assert response.status_code == 200
    assert len(response.json()) == 3


# --- Test GET /stocks/{id} ---
# Vérifie qu'on récupère bien le bon entrepôt par son ID
def test_get_stock_by_id():
    response = client.get("/stocks/1")
    assert response.status_code == 200
    assert response.json()["entrepot"] == "Paris Nord"


# --- Test GET /stocks/{id} inexistant ---
# Vérifie qu'on reçoit bien une erreur 404 pour un entrepôt inconnu
def test_get_stock_not_found():
    response = client.get("/stocks/99")
    assert response.status_code == 404


# --- Test POST /stocks/{id} ---
# Vérifie qu'on peut bien mettre à jour le stock d'un entrepôt
def test_update_stock():
    payload = {"outils_disponibles": 50, "outils_loues": 10}
    response = client.post("/stocks/1", json=payload)
    assert response.status_code == 200
    assert response.json()["stock"]["outils_disponibles"] == 50