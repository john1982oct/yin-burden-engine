# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

from merit_engine import calculate_merit_debt_profile, calculate_yin_burden_from_bazi
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


# -------------------------------------------------------------
# Flexible date + time parser
# -------------------------------------------------------------
def _parse_datetime_flex(dob_str: str, tob_str: str | None = None):
    """
    Parse date + optional time:
      - date supports "dd/mm/yyyy" or "yyyy-mm-dd"
      - time supports "HH:MM" 24h
    Returns a datetime or None if invalid.
    """
    if not dob_str:
        return None

    dt = None
    for fmt in ("%d/%m/%Y", "%Y-%m-%d"):
        try:
            dt = datetime.strptime(dob_str, fmt)
            break
        except ValueError:
            continue

    if dt is None:
        return None

    if tob_str:
        try:
            t = datetime.strptime(tob_str, "%H:%M")
            dt = dt.replace(hour=t.hour, minute=t.minute)
        except ValueError:
            # ignore bad time, keep date-only
            pass

    return dt


# -------------------------------------------------------------
# Base route
# -------------------------------------------------------------
@app.route("/")
def home():
    return jsonify({
        "status": "ok",
        "service": "Aido Yin Burden Engine v1.0",
        "endpoints": [
            "/yin-burden",
            "/bazi-debug",
            "/yin-burden-bazi"
        ]
    })


# -------------------------------------------------------------
# Original Merit Ledger (non-BaZi)
# -------------------------------------------------------------
@app.route("/yin-burden", methods=["POST"])
def yin_burden():
    """
    Expected JSON:
      { "date_of_birth": "dd/mm/yyyy" or "yyyy-mm-dd" }
    """
    data = request.get_json(silent=True) or {}

    dob_str = data.get("date_of_birth")
    if not dob_str:
        return jsonify({"error": "date_of_birth is required"}), 400

    dob = _parse_datetime_flex(dob_str)
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


# -------------------------------------------------------------
# BaZi Debug
# -------------------------------------------------------------
@app.route("/bazi-debug", methods=["POST"])
def bazi_debug():
    """
    Debug endpoint: returns the FULL BaZi chart (Year/Month/Day/Hour).
    Uses REAL computations (not placeholders anymore).
    """
    data = request.get_json(silent=True) or {}

    dob_str = data.get("date_of_birth")
    if not dob_str:
        return jsonify({"error": "date_of_birth is required"}), 400

    tob_str = data.get("time_of_birth")

    dt = _parse_datetime_flex(dob_str, tob_str)
    if dt is None:
        return jsonify({
            "error": "Invalid date/time format. Use dd/mm/yyyy and HH:MM."
        }), 400

    chart = compute_placeholder_bazi(dt)
    chart_dict = describe_bazi_chart(chart)

    return jsonify({
        "input": {
            "date_of_birth": dob_str,
            "time_of_birth": tob_str or "12:00 (default)"
        },
        "bazi_chart": chart_dict,
        "note": "Now using REAL Year/Month/Day/Hour BaZi logic."
    })


# -------------------------------------------------------------
# NEW: Yin Burden interpreted FROM BaZi
# -------------------------------------------------------------
@app.route("/yin-burden-bazi", methods=["POST"])
def yin_burden_bazi():
    """
    New endpoint:
    Input:
      {
        "date_of_birth": "dd/mm/yyyy" or "yyyy-mm-dd",
        "time_of_birth": "HH:MM"   (optional)
      }

    Output:
      {
        "bazi_chart": {...},
        "yin_burden": {...}
      }
    """
    data = request.get_json(silent=True) or {}

    dob_str = data.get("date_of_birth")
    tob_str = data.get("time_of_birth")

    if not dob_str:
        return jsonify({"error": "date_of_birth is required"}), 400

    dt = _parse_datetime_flex(dob_str, tob_str)
    if dt is None:
        return jsonify({
            "error": "Invalid date/time format. Use dd/mm/yyyy and HH:MM."
        }), 400

    # Build REAL BaZi chart
    chart = compute_placeholder_bazi(dt)
    chart_dict = describe_bazi_chart(chart)

    # Compute Yin Burden profile FROM BaZi
    yin_profile = calculate_yin_burden_from_bazi(chart)

    return jsonify({
        "input": {
            "date_of_birth": dob_str,
            "time_of_birth": tob_str,
        },
        "bazi_chart": chart_dict,
        "yin_burden": yin_profile
    })


# -------------------------------------------------------------
# Local testing
# -------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
