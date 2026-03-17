from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd

app = Flask(__name__)

CSV_URL = "https://docs.google.com/spreadsheets/d/11g-HUKPjyteAk2sYqCgkTVjIkhDFGy5uFNzCl7CznUs/export?format=csv"

@app.route("/")
def home():
    return "OK"

@app.route("/bot", methods=["POST"])
def bot():
    resp = MessagingResponse()

    try:
        msg = request.values.get("Body", "").lower()

        df = pd.read_csv(CSV_URL)

        # limpieza segura
        df = df.dropna(how="all")
        df = df.fillna(0)

        if df.empty:
            resp.message("Sin datos")
            return str(resp)

        last = df.iloc[-1]

        # asegurar números
        def safe(x):
            try:
                return float(x)
            except:
                return 0

        temp_aire = safe(last[1])
        hum_aire = safe(last[2])
        temp_suelo = safe(last[5])
        hum_suelo = safe(last[6])
        co2 = safe(last[8])
        ph = safe(last[7])

        if "clima" in msg:
            resp.message(f"🌡 {temp_aire}°C | 💧 {hum_aire}%")

        elif "suelo" in msg:
            resp.message(f"🌿 {temp_suelo}°C | 💦 {hum_suelo}%")

        elif "co2" in msg:
            resp.message(f"CO2: {co2} ppm | pH: {ph}")

        else:
            resp.message("ok")

    except Exception as e:
        resp.message(f"ERROR: {str(e)}")

    return str(resp)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
