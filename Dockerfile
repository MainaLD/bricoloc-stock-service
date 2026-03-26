# Dockerfile — Conteneurisation du service BricoLoc Stock Service

# Image de base Python légère
FROM python:3.12-slim

# Répertoire de travail dans le conteneur
WORKDIR /app

# Copie et installation des dépendances en premier
# (optimise le cache Docker — si requirements.txt ne change pas, cette couche est réutilisée)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du code source
COPY app/ ./app/

# Port exposé par le conteneur
EXPOSE 8000

# Commande de démarrage du service
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]