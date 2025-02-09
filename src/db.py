# db.py
import os
import psycopg2

# Hole den Verbindungsstring aus der Umgebungsvariable oder verwende einen Standardwert
DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://postgres:password@db:5432/db-1")

def get_db_connection(url = None):
    """Stellt eine Verbindung zur PostgreSQL-Datenbank her."""
    url = DATABASE_URL if url is None else url
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

class DB:
    def __init__(self, url=None):
        self.conn = get_db_connection(url)

    def insert_in_db(self,**kwargs):
        table_name = kwargs.get("table_name")
        if table_name is None:
            print("table_name not set, not writing anything...")
            return False
        cur = self.conn.cursor()
        cur.execute(f"INSERT INTO {table_name} ")
