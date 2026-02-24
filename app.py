# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import random

from merit_engine import calculate_merit_debt_profile, calculate_yin_burden_from_bazi
from bazi_core import compute_placeholder_bazi, describe_bazi_chart
from elemental_blueprint_engine import generate_elemental_blueprint

app = Flask(__name__)

# -------------------------------------------------------------
# CORS FIX (allow local file:// and frontend JS)
# -------------------------------------------------------------
CORS(app, resources={r"/*": {"origins": "*"}})


# -------------------------------------------------------------
# Flexible date + time parser
# -------------------------------------------------------------
def _parse_datetime_flex(dob_str: str, tob_str: str | None = None):
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
            "/yin-burden-bazi",
            "/bazi_decades"
        ]
    })


# -------------------------------------------------------------
# Original Merit Ledger (non-BaZi)
# -------------------------------------------------------------
@app.route("/yin-burden", methods=["POST"])
def yin_burden():
    data = request.get_json(silent=True) or {}
    dob_str = data.get("date_of_birth")

    if not dob_str:
        return jsonify({"error": "date_of_birth is required"}), 400

    dob = _parse_datetime_flex(dob_str)
    if dob is None:
        return jsonify({"error": "Invalid date format"}), 400

    profile = calculate_merit_debt_profile(dob)

    return jsonify({
        "input": {"date_of_birth": dob_str},
        "merit_debt": profile
    })


# -------------------------------------------------------------
# BaZi Debug
# -------------------------------------------------------------
@app.route("/bazi-debug", methods=["POST"])
def bazi_debug():
    data = request.get_json(silent=True) or {}

    dob_str = data.get("date_of_birth")
    if not dob_str:
        return jsonify({"error": "date_of_birth is required"}), 400

    tob_str = data.get("time_of_birth")
    dt = _parse_datetime_flex(dob_str, tob_str)

    if dt is None:
        return jsonify({"error": "Invalid date/time"}), 400

    chart = compute_placeholder_bazi(dt)
    chart_dict = describe_bazi_chart(chart)

    return jsonify({
        "input": {
            "date_of_birth": dob_str,
            "time_of_birth": tob_str or "12:00 (default)"
        },
        "bazi_chart": chart_dict,
        "note": "REAL Year/Month/Day/Hour BaZi logic used"
    })
    
# -------------------------------------------------------------
# NEW: Elemental Blueprint (Primary Constitution + Underlying Layer)
# -------------------------------------------------------------
@app.route("/elemental-blueprint", methods=["POST"])
def elemental_blueprint():
    data = request.get_json(silent=True) or {}

    dob_str = data.get("date_of_birth")
    if not dob_str:
        return jsonify({"error": "date_of_birth is required"}), 400

    tob_str = data.get("time_of_birth")
    dt = _parse_datetime_flex(dob_str, tob_str)

    if dt is None:
        return jsonify({"error": "Invalid date/time"}), 400

    chart = compute_placeholder_bazi(dt)
    blueprint = generate_elemental_blueprint(chart)

    return jsonify({
        "input": {
            "date_of_birth": dob_str,
            "time_of_birth": tob_str or None
        },
        "blueprint": blueprint
    })

# -------------------------------------------------------------
# Yin Burden interpreted FROM BaZi
# -------------------------------------------------------------
@app.route("/yin-burden-bazi", methods=["POST"])
def yin_burden_bazi():
    data = request.get_json(silent=True) or {}
    dob_str = data.get("date_of_birth")
    tob_str = data.get("time_of_birth")

    if not dob_str:
        return jsonify({"error": "date_of_birth is required"}), 400

    dt = _parse_datetime_flex(dob_str, tob_str)
    if dt is None:
        return jsonify({"error": "Invalid date/time"}), 400

    chart = compute_placeholder_bazi(dt)
    chart_dict = describe_bazi_chart(chart)
    yin_profile = calculate_yin_burden_from_bazi(chart)

    return jsonify({
        "input": {
            "date_of_birth": dob_str,
            "time_of_birth": tob_str
        },
        "bazi_chart": chart_dict,
        "yin_burden": yin_profile
    })


# -------------------------------------------------------------
# NEW: BaZi DECADE Journey endpoint for the AIDO game
# -------------------------------------------------------------
@app.route("/bazi_decades", methods=["GET"])
def bazi_decades():
    """
    Query params:
      birth_date=yyyy-mm-dd or dd/mm/yyyy
      birth_time=HH:MM (optional)
      gender=male/female (unused for now)

    Returns:
      A fixed JSON structure required by the front-end game.
    """
    birth_date = request.args.get("birth_date")
    birth_time = request.args.get("birth_time")
    gender = request.args.get("gender", "male")

    if not birth_date:
        return jsonify({"error": "birth_date is required"}), 400

    dt = _parse_datetime_flex(birth_date, birth_time)
    if dt is None:
        return jsonify({"error": "Invalid birth_date/birth_time"}), 400

    # deterministic seed based on birth datetime
    seed = dt.year + dt.month + dt.day + dt.hour
    rng = random.Random(seed)

    base_year = dt.year
    decades = []

    for i in range(4):  # 4 decades for v1
        start_year = base_year + i * 10
        end_year = start_year + 9

        love = rng.randint(60, 90)
        wealth = rng.randint(60, 90)
        career = rng.randint(60, 90)
        health = rng.randint(60, 90)
        overall = round((love + wealth + career + health) / 4)

        decades.append({
            "start": start_year,
            "end": end_year,
            "overall_luck": overall,
            "love": love,
            "wealth": wealth,
            "career": career,
            "health": health
        })

    return jsonify({
        "input": {
            "birth_date": birth_date,
            "birth_time": birth_time,
            "gender": gender
        },
        "chart_type": "demo_decade_profile",
        "favorable_gods": ["食神", "偏财"],
        "decades": decades
    })


# -------------------------------------------------------------
# Local testing
# -------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
