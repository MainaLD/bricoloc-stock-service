# BricoLoc Stock Service — POC Microservice v2.0

Preuve de concept (POC) développée dans le cadre du rapport d'architecture
CESI BricoLoc 2.0. Ce service simule le microservice Stock & Logistique
de la plateforme de location d'outils BricoLoc.

Il illustre deux décisions architecturales clés :
- Le remplacement du serveur FTP par un dépôt Git avec pipeline CI/CD automatisé
- La conteneurisation des microservices via Docker

---

## Stack technique

| Technologie cible       | Technologie POC          | Rôle                        |
|-------------------------|--------------------------|-----------------------------|
| Java 21 / Spring Boot 3 | Python 3.12              | Langage de développement    |
| Spring Boot REST        | FastAPI                  | Framework API REST          |
| JUnit / Spring Test     | pytest                   | Tests unitaires             |
| Azure Container Apps    | Docker + docker-compose  | Conteneurisation            |
| Azure DevOps CI/CD      | GitHub Actions           | Pipeline CI/CD              |
| Azure Container Registry| GitHub Container Registry| Registry Docker             |
| PostgreSQL              | data.json                | Persistance des données     |

---

## Endpoints disponibles

| Méthode | Endpoint                  | Description                          |
|---------|---------------------------|--------------------------------------|
| GET     | `/health`                 | Health check du service              |
| GET     | `/stocks`                 | Liste tous les entrepôts             |
| GET     | `/stocks/{id}`            | Stock d'un entrepôt spécifique       |
| POST    | `/stocks/{id}/louer`      | Enregistre la location d'un outil    |
| POST    | `/stocks/{id}/retourner`  | Enregistre le retour d'un outil      |

Documentation interactive : `http://localhost:8000/docs`

---

## Lancer le projet en local

### Prérequis
- Docker installé et démarré
- Git installé

### Avec Docker (recommandé)
```bash
git clone https://github.com/MainaLD/bricoloc-stock-service.git
cd bricoloc-stock-service
docker compose up --build
```

Accéder à l'application : `http://localhost:8000`

Stopper le service :
```bash
docker compose down
```

### Sans Docker (développement)
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

---

## Lancer les tests
```bash
source venv/bin/activate
pytest tests/ -v
```

---

## Pipeline CI/CD

Le pipeline GitHub Actions se déclenche automatiquement sur chaque push
sur la branche `main` :

| Stage       | Description                                    |
|-------------|------------------------------------------------|
| **build**   | Construit l'image Docker                       |
| **test**    | Lance les 7 tests pytest                       |
| **publish** | Publie l'image sur GitHub Container Registry   |

Image publiée : `ghcr.io/mainald/bricoloc-stock-service:latest`

---

## Structure du projet
```
bricoloc-stock-service/
├── app/
│   ├── data.json            # Données fictives (stocks entrepôts)
│   ├── main.py              # Point d'entrée FastAPI
│   ├── static/
│   │   └── style.css        # CSS de l'IHM
│   ├── templates/
│   │   └── index.html       # Interface web
│   └── routes/
│       └── stocks.py        # Endpoints de gestion des stocks
├── tests/
│   └── test_stocks.py       # 7 tests unitaires pytest
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .github/
    └── workflows/
        └── ci.yml           # Pipeline GitHub Actions
```