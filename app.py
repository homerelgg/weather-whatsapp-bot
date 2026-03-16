from flask import Flask, request
import pandas as pd

app = Flask(__name__)

CSV_URL = "https://docs.google.com/spreadsheets/d/11g-HUKPjyteAk2sYqCgkTVjIkhDFGy5uFNzCl7CznUs/export?format=csv"

@app.route("/")
def home():
    return "Bot meteorologico funcionando"

@app.route("/bot", methods=["POST"])
def bot():

    try:

        df = pd.read_csv(CSV_URL)

        # tomar la ultima fila con datos
        last = df.iloc[-1]

        temp_aire = last["Temp Aire (°C)"]
        hum_aire = last["Hum Aire (%)"]
        temp_suelo = last["Temp Suelo (°C)"]
        hum_suelo = last["Hum Suelo (%)"]
        ph = last["pH"]
        co2 = last["CO2 (ppm)"]
        luz = last["Iluminacion (lux)"]
        temp_interna = last["Temp Interna (°C)"]
        hum_interna = last["Hum Interna (%)"]
        voltaje = last["Voltaje (V)"]

        respuesta = f"""
🌱 Estación ambiental

🌡 Temp aire: {temp_aire} °C
💧 Hum aire: {hum_aire} %

🌿 Temp suelo: {temp_suelo} °C
💦 Hum suelo: {hum_suelo} %

🧪 pH: {ph}
🌬 CO2: {co2} ppm
☀️ Luz: {luz} lux

🏠 Temp interna: {temp_interna} °C
💧 Hum interna: {hum_interna} %

🔋 Voltaje: {voltaje} V
"""

        return respuesta

    except Exception as e:

        return f"Error leyendo sensores: {e}"


if __name__ == "__main__":
    app.run()
