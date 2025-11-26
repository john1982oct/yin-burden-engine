# merit_engine.py

from datetime import datetime
import hashlib


def _stable_int_seed(namespace: str, key: str) -> int:
    """
    Deterministic integer from (namespace, key) using md5.
    Same inputs => same output, across restarts.
    """
    s = f"{namespace}:{key}"
    h = hashlib.md5(s.encode("utf-8")).hexdigest()
    return int(h[:8], 16)


def calculate_merit_debt_profile(dob: datetime) -> dict:
    """
    TEMP VERSION:
    - Uses only date string to generate a stable fake score.
    - We will later swap this to use real BaZi pillars.
    """
    dob_key = dob.strftime("%Y%m%d")
    h = _stable_int_seed("yin-burden", dob_key)

    # Raw score 30..90 (placeholder scale)
    raw_score = 30 + (h % 61)

    # Simple level mapping for v0.1
    if raw_score <= 40:
        level = 3
        level_name = "Emotional Baggage"
        summary = (
            "You carry light-to-medium emotional expectations and daily responsibilities. "
            "With small consistent positive actions, your burden can reduce quickly."
        )
    elif raw_score <= 60:
        level = 5
        level_name = "Responsibility Load"
        summary = (
            "You often take care of others and shoulder responsibility. "
            "Learning healthy boundaries will greatly lighten your life burden."
        )
    elif raw_score <= 80:
        level = 7
        level_name = "Wealth Leakage Phase"
        summary = (
            "Your life script includes lessons around money, loyalty and over-giving. "
            "You are meant to learn wise giving and strong self-protection."
        )
    else:
        level = 9
        level_name = "Heavy Ancestral Load"
        summary = (
            "You chose deep karmic lessons this lifetime. "
            "After each reset, your wisdom and spiritual credit grow very fast."
        )

    merit_points = max(100, min(raw_score * 20, 2000))

    return {
        "raw_score": raw_score,
        "level": level,
        "level_name": level_name,
        "merit_points": merit_points,
        "summary": summary,
    }
