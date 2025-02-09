# db.py
import os
import psycopg2

# Hole den Verbindungsstring aus der Umgebungsvariable oder verwende einen Standardwert
DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://postgres:password@db:5432/db-1")

def get_db_connection():
    """Stellt eine Verbindung zur PostgreSQL-Datenbank her."""
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def insert_user(email, username):
    """Fügt einen neuen Benutzer in die Tabelle 'users' ein."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (email, username) VALUES (%s, %s)",
        (email, username)
    )
    conn.commit()
    cur.close()
    conn.close()
