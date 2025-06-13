from flask import Flask, request, jsonify
import datetime, json, os

app = Flask(__name__)
LOG_FILE = "grace_global_log.json"

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        json.dump([], f)

@app.route("/log", methods=["POST"])
def log_entry():
    try:
        data = request.get_json()
        entry = {
            "timestamp": str(datetime.datetime.now()),
            "event": data.get("event", "no event provided"),
            "node": data.get("node", "unknown")
        }

        with open(LOG_FILE, "r") as f:
            logs = json.load(f)
        logs.append(entry)
        with open(LOG_FILE, "w") as f:
            json.dump(logs[-500:], f, indent=2)

        return jsonify({"status": "logged", "entry": entry}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "🌐 Grace Logger is alive."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
