# 1. Wähle das Basis-Image mit Python
FROM python:3.11

# 2. Setze das Arbeitsverzeichnis im Container
WORKDIR /backend

# 3. Kopiere die requirements.txt und installiere die Python-Abhängigkeiten
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Kopiere den gesamten App-Code ins Arbeitsverzeichnis
COPY . .

# 5. Exponiere den Port, auf dem die App läuft
EXPOSE 6969

# 6. Setze den Standardbefehl, um die App zu starten
CMD ["python", "main.py"]