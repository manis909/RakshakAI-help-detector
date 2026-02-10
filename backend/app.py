from flask import Flask, request, jsonify
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app)

latest_alert = None   # 🔴 GLOBAL VARIABLE

# TEMP STORAGE
alerts = []


app = Flask(__name__)

@app.route("/alert", methods=["POST"])
def receive_alert():
    global latest_alert
    data = request.json

    latest_alert = {
        "message": "Emergency detected",
        "locality": data.get("locality"),
        "timestamp": time.time()
    }

    print("Alert stored:", latest_alert)

    return jsonify({"status": "ok"}), 200


@app.route("/send-alert", methods=["POST"])
def send_alert():
    data = request.json
    locality = data.get("locality", "Unknown")

    # ✅ your existing code stays here
    # telegram send
    # sms send
    # screenshot save
    print("Alert sent to app backend")

    # ✅ THIS IS WHAT YOU ASKED ABOUT
    return jsonify({
        "status": "success",
        "message": "Emergency detected",
        "locality": locality,
        "timestamp": time.time()
    }), 200



@app.route("/get-alerts/<locality>", methods=["GET"])
@app.route("/alert", methods=["GET"])
def get_alert():
    if latest_alert:
        return jsonify(latest_alert), 200
    return jsonify({"message": "No alert"}), 200

@app.route("/alerts", methods=["GET"])
def get_all_alerts():
    return jsonify(alerts), 200

@app.route("/")
def home():
    return "Help Sender Backend Running 🚀"

@app.route("/alert", methods=["POST"])
def alert():
    return send_alert()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
