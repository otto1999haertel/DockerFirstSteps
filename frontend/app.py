# app.py
from flask import Flask, request
from src.db import insert_user  # Importiere die DB-Funktion aus der separaten Datei

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Lese die eingegebenen Werte aus dem Formular
        email = request.form.get('email')
        username = request.form.get('username')

        # Füge die Daten in die Datenbank ein
        insert_user(email, username)

        return f"<h1>Daten gespeichert</h1><p>E-Mail: {email}</p><p>Nutzername: {username}</p>"

    # HTML-Formular wird bei einer GET-Anfrage angezeigt
    return '''
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <title>Registrierungsformular</title>
    </head>
    <body>
        <h1>Registrierungsformular</h1>
        <form method="post">
            <label for="email">E-Mail:</label><br>
            <input type="text" id="email" name="email"><br><br>
            
            <label for="username">Nutzername:</label><br>
            <input type="text" id="username" name="username"><br><br>
            
            <input type="submit" value="Absenden">
        </form>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6969)
