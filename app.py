from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd

app = Flask(__name__)

CSV_URL = "https://docs.google.com/spreadsheets/d/11g-HUKPjyteAk2sYqCgkTVjIkhDFGy5uFNzCl7CznUs/export?format=csv"

@app.route("/")
def home():
    return "Bot meteorologico funcionando"

@app.route("/bot", methods=["POST"])
def bot():
    try:
        msg = request.values.get("Body", "").lower()

        df = pd.read_csv(CSV_URL)
        df = df.dropna(how="all")  # eliminar filas vacías

        last = df.iloc[-1]

        # usar índices (más seguro que nombres con símbolos)
        temp_aire = last[1]
        hum_aire = last[2]
        temp_hoja = last[3]
        hum_hoja = last[4]
        temp_suelo = last[5]
        hum_suelo = last[6]
        ph = last[7]
        co2 = last[8]
        luz = last[9]
        temp_interna = last[10]
        hum_interna = last[11]
        voltaje = last[12]

        resp = MessagingResponse()

        if "clima" in msg:
            resp.message(f"🌡 Temp aire: {temp_aire}°C\n💧 Humedad: {hum_aire}%")

        elif "suelo" in msg:
            resp.message(f"🌿 Temp suelo: {temp_suelo}°C\n💦 Hum suelo: {hum_suelo}%")

        elif "co2" in msg:
            resp.message(f"🌬 CO2: {co2} ppm\n🧪 pH: {ph}")

        elif "luz" in msg:
            resp.message(f"☀️ Luz: {luz} lux")

        elif "interno" in msg:
            resp.message(f"🏠 Temp interna: {temp_interna}°C\n💧 Hum interna: {hum_interna}%")

        elif "voltaje" in msg:
            resp.message(f"🔋 Voltaje: {voltaje} V")

        elif "estado" in msg:
            resp.message(f"""
📊 ESTADO COMPLETO

🌡 Aire: {temp_aire}°C | {hum_aire}%
🌿 Suelo: {temp_suelo}°C | {hum_suelo}%
🌬 CO2: {co2} ppm
🧪 pH: {ph}
☀️ Luz: {luz} lux
🏠 Interno: {temp_interna}°C | {hum_interna}%
🔋 Voltaje: {voltaje} V
""")

        else:
            resp.message("""📊 Comandos disponibles:

clima
suelo
co2
luz
interno
voltaje
estado
""")

        return str(resp)

    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
