# BricoLoc Stock Service - POC Microservice

Service de gestion des stocks et entrepôts de BricoLoc 2.0.  
Ce POC illustre deux décisions architecturales clés du rapport d'architecture CESI :
- Le remplacement du serveur FTP sans Git par un dépôt Git avec pipeline CI/CD
- La conteneurisation des microservices via Docker

---

## Stack technique

- **Langage** : Python 3.12
- **Framework** : FastAPI
- **Conteneurisation** : Docker + docker-compose
- **CI/CD** : GitHub Actions
- **Registry** : GitHub Container Registry (ghcr.io)

---

## Structure du projet
```
bricoloc-stock-service/
├── app/
│   ├── main.py              # Point d'entrée FastAPI
│   └── routes/
│       └── stocks.py        # Endpoints de gestion des stocks
├── tests/
│   └── test_stocks.py       # Tests unitaires pytest
├── Dockerfile               # Conteneurisation du service
├── docker-compose.yml       # Lancement local
├── requirements.txt         # Dépendances Python
├── .github/
│   └── workflows/
│       └── ci.yml           # Pipeline CI/CD GitHub Actions
└── README.md
```

---

## Endpoints disponibles

| Méthode | Endpoint        | Description                         |
|---------|-----------------|-------------------------------------|
|   GET   | `/health`       | Health check du service             |
|   GET   | `/stocks`       | Liste tous les stocks               |
|   GET   | `/stocks/{id}`  | Stock d'un entrepôt spécifique      |
|  POST   | `/stocks/{id}`  | Met à jour le stock d'un entrepôt   |

Documentation interactive disponible sur : `http://localhost:8000/docs`

---

## Lancer le projet en local

### Prérequis
- Docker installé
- Git installé

### Avec Docker (recommandé)
```bash
# Cloner le repo
git clone https://github.com/MainaLD/bricoloc-stock-service.git
cd bricoloc-stock-service

# Lancer le service
docker compose up --build

# Accéder à l'API
http://localhost:8000/health
http://localhost:8000/docs
```

### Stopper le service
```bash
docker compose down
```

---

## Lancer les tests
```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Lancer les tests
pytest tests/ -v
```

---

## Pipeline CI/CD

Le pipeline GitHub Actions se déclenche automatiquement sur chaque push sur `main` :

|   Stage     | Description                 |
|-------------|-----------------------------|
| **build**   | Construit l'image Docker    |
| **test**    | Lance les tests pytest      |
| **publish** | Publie l'image sur ghcr.io  |

Image publiée : `ghcr.io/mainald/bricoloc-stock-service:latest`