from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd
import time

app = Flask(__name__)

sheet_url = "https://docs.google.com/spreadsheets/d/1RsN1sB-vglbjaKC_mFx59hYHhdx81bc4qc9ovuWEZec/export?format=csv"

cache_df = None
cache_time = 0

def obtener_datos():

    global cache_df, cache_time

    if time.time() - cache_time > 30:

        df = pd.read_csv(sheet_url, header=1)
        df.columns = df.columns.str.strip()

        cache_df = df
        cache_time = time.time()

    return cache_df

def clima_actual(df):

    ultima = df.iloc[-1]

    return f"""
🌤 Estación Meteorológica

🌡 Temperatura: {ultima['sensor1_temp']} °C
💧 Humedad: {ultima['sensor2_humedad']} %
🌬 Presión: {ultima['sensor3_presion']} hPa
☀ Luz: {ultima['sensor4_luz']}

🕒 {ultima['timestamp']}
"""

def promedio(df):

    return f"""
📊 Promedios

🌡 Temperatura: {df['sensor1_temp'].mean():.2f} °C
💧 Humedad: {df['sensor2_humedad'].mean():.2f} %
🌬 Presión: {df['sensor3_presion'].mean():.2f} hPa
"""

@app.route("/bot", methods=["POST"])
def bot():

    mensaje = request.values.get("Body","").lower().strip()

    resp = MessagingResponse()

    try:

        df = obtener_datos()

        if "hola" in mensaje:

            resp.message("Hola 👋")

        elif "clima" in mensaje:

            resp.message(clima_actual(df))

        elif "promedio" in mensaje:

            resp.message(promedio(df))

        else:

            resp.message("Comandos: hola | clima | promedio")

    except Exception as e:

        print(e)
        resp.message("⚠ Error leyendo sensores")

    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
