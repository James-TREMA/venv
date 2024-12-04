# Utilise une image Python compatible
FROM python:3.13

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier les fichiers nécessaires dans le conteneur
COPY . .

# Installer les dépendances
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Commande par défaut pour lancer le script
CMD ["python", "connectMYSQL.py"]