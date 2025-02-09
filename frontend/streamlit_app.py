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

st.write(user_data)
logging.debug(user_data)
logging.debug("####################")

# Falls der JSON-Inhalt ein weiteres "data"-Feld enthält
user_data = user_data[0] # Falls du nur das "data"-Feld brauchst
logging.debug(user_data)
st.session_state.user_data = pd.DataFrame(data=user_data)



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
    else:
        st.warning("Bitte sowohl Name als auch Benutzername eingeben.")

# Tabelle mit allen Benutzerdaten anzeigen
st.write("### Benutzerliste")
st.dataframe(st.session_state.user_data)