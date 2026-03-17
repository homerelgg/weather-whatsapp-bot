from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd

app = Flask(__name__)

CSV_URL = "https://docs.google.com/spreadsheets/d/11g-HUKPjyteAk2sYqCgkTVjIkhDFGy5uFNzCl7CznUs/export?format=csv"

@app.route("/")
def home():
    return "OK"

def cargar_datos():
    df = pd.read_csv(CSV_URL)

    # limpiar nombres de columnas
    df.columns = df.columns.str.strip()

    # convertir comas a punto (27,7 → 27.7)
    df = df.replace(",", ".", regex=True)

    # convertir todo a número donde se pueda
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="ignore")

    df = df.fillna(0)
    df = df.dropna(how="all")

    return df

@app.route("/bot", methods=["POST"])
def bot():
    resp = MessagingResponse()

    try:
        msg = request.values.get("Body", "").lower()

        df = cargar_datos()

        if df.empty:
            resp.message("Sin datos")
            return str(resp)

        last = df.iloc[-1]

        def safe(col):
            try:
                return float(last[col])
            except:
                return 0

        # USANDO TUS NOMBRES EXACTOS
        temp_aire = safe("Temp Aire (°C)")
        hum_aire = safe("Hum Aire (%)")
        temp_suelo = safe("Temp Suelo (°C)")
        hum_suelo = safe("Hum Suelo (%)")
        co2 = safe("CO2 (ppm)")
        ph = safe("pH")
        luz = safe("Iluminacion (lux)")
        voltaje = safe("Voltaje (V)")

        if "clima" in msg:
            resp.message(f"🌡 {temp_aire}°C | 💧 {hum_aire}%")

        elif "suelo" in msg:
            resp.message(f"🌿 {temp_suelo}°C | 💦 {hum_suelo}%")

        elif "co2" in msg:
            resp.message(f"CO2: {co2} ppm | pH: {ph}")

        elif "luz" in msg:
            resp.message(f"☀️ {luz} lux")

        elif "voltaje" in msg:
            resp.message(f"🔋 {voltaje} V")

        elif "estado" in msg:
            resp.message(f"""📊 ESTADO

🌡 Aire: {temp_aire}°C | {hum_aire}%
🌿 Suelo: {temp_suelo}°C | {hum_suelo}%
🌬 CO2: {co2}
🧪 pH: {ph}
☀️ Luz: {luz}
🔋 Voltaje: {voltaje}
""")

        else:
            resp.message("ok")

    except Exception as e:
        resp.message(f"ERROR: {str(e)}")

    return str(resp)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
