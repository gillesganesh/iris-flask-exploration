# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copier les fichiers
COPY . /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install notebook

# Exposer les ports Flask (5000) et Jupyter (8888)
EXPOSE 5000
EXPOSE 8888

# Commande de démarrage : Flask + Jupyter
CMD ["sh", "-c", "jupyter notebook --ip=0.0.0.0 --no-browser --NotebookApp.token='' --NotebookApp.password='' --allow-root & python app.py"]

