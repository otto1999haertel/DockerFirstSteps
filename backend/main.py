import psycopg2
import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Hole den Verbindungsstring aus der Umgebungsvariable oder verwende einen Standardwert
DATABASE_URL = os.environ.get("DATABASE_URL", "postgres://postgres:password@db:5432/db-1")

def get_db_connection(url = None):
    """Stellt eine Verbindung zur PostgreSQL-Datenbank her."""
    url = DATABASE_URL if url is None else url
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/write_data', methods=['POST'])
def write_data():
    print("Received request with")
    data = request.get_json()
    print("data:", data)

    if 'username' in data and 'name' in data:
        conn = get_db_connection()
        try:
        
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, email) VALUES (%s, %s)", (data['username'], data['name']))
            conn.commit()
            cursor.close()
            conn.close()
        except Exception as e:
            #cursor = conn.cursor()
            cursor.close()
            conn.close()
            print("closing connections...")
            return jsonify({"error": f"Datenbankfehler: {e}"}), 500
        return jsonify({"message": "User gespeichert"}), 201
    else:
        return jsonify({"error": "Fehlende Daten"}), 400
    
@app.route('/get_data', methods=['GET'])
def get_data():
    print("Received request with")
    #data = request.get_json()
    #print("data:", data)

    #if 'username' in data and 'name' in data:
    conn = get_db_connection()
    try:
    
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        data = cursor.fetchall()
        print(data)
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        #cursor = conn.cursor()
        cursor.close()
        conn.close()
        data = dict()
        print("closing connections...")

    res = app.response_class(
        response=json.dumps(data),
        status=200,
        mimetype='application/json'
    )
    return data #res #json.dumps(data) #jsonify({"data": data}), 200
    #return jsonify({"message": "User gespeichert"}), 201
    #else:
    #    return jsonify({"error": "Fehlende Daten"}), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6969)