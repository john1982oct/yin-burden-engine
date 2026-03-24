# Aido Yin Burden / Merit Debt Engine

## Overview

A Python Flask REST API that calculates and interprets metaphysical profiles based on Chinese astrology (BaZi). It provides endpoints for analyzing "merit debt," "yin burden," "elemental blueprints," and "life phase" readings using a user's date and time of birth.

## Tech Stack

- **Language:** Python 3.12
- **Web Framework:** Flask 3.0.0
- **WSGI Server:** Gunicorn 21.2.0 (production)
- **CORS:** Flask-Cors 4.0.1
- **Timezone:** pytz 2024.1

## Project Structure

- `app.py` — Flask application entry point, API routing
- `bazi_core.py` — Core BaZi chart computation and description
- `merit_engine.py` — Merit debt and yin burden calculations
- `elemental_blueprint_engine.py` — Elemental blueprint generation
- `current_phase_engine.py` — Current life phase readings
- `requirements.txt` — Python dependencies

## API Endpoints

- `GET /` — Service status and endpoint list
- `POST /yin-burden` — Original merit ledger calculation (non-BaZi)
- `POST /bazi-debug` — BaZi chart debug output
- `POST /elemental-blueprint` — Elemental blueprint from BaZi
- `POST /yin-burden-bazi` — Yin burden interpreted from BaZi
- `GET /bazi_decades` — Demo decade-based luck profiles
- `POST /current-phase` — Current life phase reading

## Running the App

- **Development:** `python app.py` (port 5000, debug mode)
- **Production:** `gunicorn --bind=0.0.0.0:5000 --reuse-port app:app`

## Deployment

Configured for autoscale deployment using Gunicorn on port 5000.
