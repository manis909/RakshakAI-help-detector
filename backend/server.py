from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

ALERTS = []  # temporary in-memory store

@app.route("/", methods=["GET"])
def home():
    return "Help Sender Backend Running"

@app.route("/alert", methods=["POST"])
def receive_alert():
    data = request.json

    alert = {
        "type": data.get("type", "UNKNOWN"),
        "locality": data.get("locality"),
        "time": datetime.now().strftime("%H:%M:%S"),
        "message": data.get("message")
    }

    ALERTS.append(alert)
    return jsonify({"status": "ok"})

@app.route("/alerts", methods=["GET"])
def get_alerts():
    locality = request.args.get("locality")

    filtered = [
        a for a in ALERTS
        if a["locality"] == locality
    ]

    return jsonify(filtered)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
