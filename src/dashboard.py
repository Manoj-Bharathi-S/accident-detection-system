import os
import pandas as pd
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

app = Flask(__name__, static_folder="../static", static_url_path="/")
CORS(app)

LOG_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs", "accidents.csv")

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/api/logs")
def get_logs():
    if not os.path.exists(LOG_FILE_PATH):
        return jsonify([])
    try:
        # Read full CSV
        df = pd.read_csv(LOG_FILE_PATH)
        # Handle NaN values
        df = df.fillna("")
        # Return as list of dictionaries
        logs = df.to_dict(orient="records")
        return jsonify(logs)
    except Exception as e:
        print(f"Error reading logs: {e}")
        return jsonify([])

if __name__ == "__main__":
    app.run(debug=True, port=5000)
