from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd

app = Flask(__name__)

CSV_URL = "https://docs.google.com/spreadsheets/d/11g-HUKPjyteAk2sYqCgkTVjIkhDFGy5uFNzCl7CznUs/export?format=csv"

# =========================
# FUNCION LIMPIA Y SEGURA
# =========================
def cargar_datos():
    df = pd.read_csv(CSV_URL)

    # limpiar nombres
    df.columns = df.columns.str.strip()

    # convertir comas a punto (27,7 → 27.7)
    df = df.replace(",", ".", regex=True)

    # convertir a número seguro
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # limpiar
    df = df.dropna(how="all")
    df = df.fillna(0)

    return df


# =========================
# HOME (para cron / ping)
# =========================
@app.route("/")
def home():
    return "OK FUNCIONANDO"


# =========================
# BOT WHATSAPP
# =========================
@app.route("/bot", methods=["POST"])
def bot():
    resp = MessagingResponse()

    try:
        msg = request.values.get("Body", "").lower()

        df = cargar_datos()

        if df.empty:
            resp.message("⚠️ Sin datos disponibles")
            return str(resp)

        last = df.iloc[-1]

        def safe(col):
            try:
                return float(last[col])
            except:
                return 0

        # === COLUMNAS REALES DE TU SHEET ===
        temp_aire = safe("Temp Aire (°C)")
        hum_aire = safe("Hum Aire (%)")
        temp_hoja = safe("Temp Hoja (°C)")
        hum_hoja = safe("Hum Hoja (%)")
        temp_suelo = safe("Temp Suelo (°C)")
        hum_suelo = safe("Hum Suelo (%)")
        ph = safe("pH")
        conductividad = safe("Conductividad (uS/cm)")
        co2 = safe("CO2 (ppm)")
        luz = safe("Iluminacion (lux)")
        temp_interna = safe("Temp Interna (°C)")
        hum_interna = safe("Hum Interna (%)")
        voltaje = safe("Voltaje (V)")

        # =========================
        # COMANDOS
        # =========================

        if "clima" in msg:
            resp.message(f"🌡 {temp_aire}°C | 💧 {hum_aire}%")

        elif "suelo" in msg:
            resp.message(f"🌿 {temp_suelo}°C | 💦 {hum_suelo}%")

        elif "co2" in msg:
            resp.message(f"🌬 CO2: {co2} ppm\n🧪 pH: {ph}")

        elif "luz" in msg:
            resp.message(f"☀️ {luz} lux")

        elif "interno" in msg:
            resp.message(f"🏠 {temp_interna}°C | 💧 {hum_interna}%")

        elif "voltaje" in msg:
            resp.message(f"🔋 {voltaje} V")

        elif "estado" in msg:
            resp.message(f"""📊 ESTADO COMPLETO

🌡 Aire: {temp_aire}°C | {hum_aire}%
🌿 Suelo: {temp_suelo}°C | {hum_suelo}%
🍃 Hoja: {temp_hoja}°C | {hum_hoja}%
🌬 CO2: {co2} ppm
🧪 pH: {ph}
⚡ Conductividad: {conductividad}
☀️ Luz: {luz}
🏠 Interno: {temp_interna}°C | {hum_interna}%
🔋 Voltaje: {voltaje} V
""")

        else:
            resp.message("""📊 Comandos:

clima
suelo
co2
luz
interno
voltaje
estado
""")

    except Exception as e:
        resp.message(f"❌ ERROR: {str(e)}")

    return str(resp)
