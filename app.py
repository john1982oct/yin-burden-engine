# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from merit_engine import calculate_merit_debt_profile
from bazi_core import compute_placeholder_bazi, describe_bazi_chart

app = Flask(__name__)

# Allow calls from your WordPress domain (adjust if needed)
CORS(app, resources={
    r"/*": {
        "origins": [
            "https://aidoshop.com",
            "https://www.aidoshop.com",
        ]
    }
})


def _parse_date_flex(dob_str: str):
    """
    Accepts dd/mm/yyyy or yyyy-mm-dd.
    Returns datetime or None.
    """
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(dob_str, fmt)
        except ValueError:
            continue
    return None


@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "service": "Aido Yin Burden Engine v0.1",
        "hint": "POST to /yin-burden with JSON { 'date_of_birth': 'dd/mm/yyyy' }"
    })


@app.route("/yin-burden", methods=["POST"])
def yin_burden():
    """
    Expected JSON body:
    {
      "date_of_birth": "dd/mm/yyyy" or "yyyy-mm-dd",
      "time_of_birth": "HH:MM" (optional, 24h),
      "timezone": "Asia/Singapore" (optional, future use)
    }
    For now we only use the date part. Time + timezone are for future BaZi upgrade.
    """
    data = request.get_json(silent=True) or {}

    dob_str = data.get("date_of_birth")
    if not dob_str:
        return jsonify({"error": "date_of_birth is required"}), 400

    dob = _parse_date_flex(dob_str)
    if dob is None:
        return jsonify({
            "error": "Invalid date_of_birth format. Use dd/mm/yyyy or yyyy-mm-dd."
        }), 400

    profile = calculate_merit_debt_profile(dob)

    return jsonify({
        "input": {
            "date_of_birth": dob_str,
        },
        "merit_debt": profile
    })

@app.route("/bazi-debug", methods=["POST"])
def bazi_debug():
    """
    Debug endpoint to inspect the current (placeholder) BaZi chart.

    Expected JSON body:
    {
      "date_of_birth": "dd/mm/yyyy" or "yyyy-mm-dd",
      "time_of_birth": "HH:MM" (optional)
    }

    For now:
    - If no time-of-birth is given, we default to 12:00 (noon)
    - This uses compute_placeholder_bazi(), not real BaZi yet.
    """
    data = request.get_json(silent=True) or {}

    dob_str = data.get("date_of_birth")
    if not dob_str:
        return jsonify({"error": "date_of_birth is required"}), 400

    dob = _parse_date_flex(dob_str)
    if dob is None:
        return jsonify({
            "error": "Invalid date_of_birth format. Use dd/mm/yyyy or yyyy-mm-dd."
        }), 400

    # Handle optional time of birth
    tob_str = data.get("time_of_birth")
    if tob_str:
        try:
            hh, mm = tob_str.split(":")
            dob = dob.replace(hour=int(hh), minute=int(mm))
        except Exception:
            pass
    else:
        dob = dob.replace(hour=12, minute=0)  # default

    chart = compute_placeholder_bazi(dob)

if __name__ == "__main__":
    # For local testing; Render will run via gunicorn
    app.run(host="0.0.0.0", port=5000, debug=True)
