FROM python:3.11-slim

# Dossier de travail dans le conteneur
WORKDIR /code

# Dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le dossier app dans /code/app
COPY ./app /code/app

# Lancer uvicorn en pointant vers app.main:app (donc /code/app/main.py)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
