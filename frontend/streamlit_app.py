import streamlit as st
import pandas as pd
import requests
import json
import logging
# Titel der App
st.title("Benutzerverwaltung")

# Session State für die Speicherung der Benutzerdaten initialisieren
if "user_data" not in st.session_state:
    st.session_state.user_data = pd.DataFrame(columns=["Name", "Benutzername"])
response = requests.get("http://172.19.0.3:6969/get_data")
logging.debug("####################")
logging.debug(response)

# Direkt auf die JSON-Daten zugreifen
user_data = response.json()  # Hier wird der JSON-Inhalt direkt extrahiert

#st.write(user_data)
logging.debug(user_data)
logging.debug("####################")


# make user data pandas df

# st.session_state.user_data = ...

# Eingabefelder für Name und Benutzername
name = st.text_input("Name")
username = st.text_input("Benutzername")

# Button zum Absenden der Daten
if st.button("Absenden"):
    if name and username:
        new_data = pd.DataFrame([[name, username]], columns=["Name", "Benutzername"])
        st.session_state.user_data = pd.concat([st.session_state.user_data, new_data], ignore_index=True)
        data = json.dumps(dict(username = username, name = name))
        headers = {
             "Content-Type": "application/json"
        }
        requests.post("http://172.19.0.3:6969/write_data", data=data,headers=headers)
        # Nach dem Absenden die neueste Benutzerdaten vom Server abrufen
        response = requests.get("http://172.19.0.3:6969/get_data")
        if response.status_code == 200:
            user_data = response.json()  # JSON-Daten vom Server extrahieren
            # Umwandlung in DataFrame und in Session State speichern
            st.session_state.user_data = pd.DataFrame(user_data, columns=["ID", "Name", "Username"])
        else:
            st.warning("Fehler beim Abrufen der Benutzerdaten vom Server.")
    else:
        st.warning("Bitte sowohl Name als auch Benutzername eingeben.")

# Tabelle mit allen Benutzerdaten anzeigen

# Umwandlung in DataFrame mit benannten Spalten
df = pd.DataFrame(user_data, columns=["ID", "Name", "Username"])

# Daten im Session State speichern
st.session_state.user_data = df

# Styling für die Spaltenbreiten
styled_df = df.style.set_properties(
    **{
        "ID": "width: 5px; min-width: 5px;",  # ID-Spalte klein halten
        "Name": "width: 30%;",  # Name-Spalte auf 30% der Breite
        "Username": "width: 65%;"  # Username-Spalte auf 65% der Breite
    }
)

# Streamlit-Tabelle anzeigen
st.title("Benutzerliste")
st.dataframe(styled_df, use_container_width=True, hide_index=True)