# merit_engine.py

from datetime import datetime
import hashlib

# ---------------------------------------------------------
# (A) STABLE PLACEHOLDER MERIT ENGINE (kept for /yin-burden)
# ---------------------------------------------------------

def _stable_int_seed(namespace: str, key: str) -> int:
    """
    Deterministic integer from (namespace, key) using md5.
    Same inputs => same output across restarts.
    """
    s = f"{namespace}:{key}"
    h = hashlib.md5(s.encode("utf-8")).hexdigest()
    return int(h[:8], 16)


def calculate_merit_debt_profile(dob: datetime) -> dict:
    """
    TEMP VERSION:
    - Uses only date string to generate a stable fake score.
    - This is for the old /yin-burden endpoint (keep for compatibility).
    """
    dob_key = dob.strftime("%Y%m%d")
    h = _stable_int_seed("yin-burden", dob_key)

    raw_score = 30 + (h % 61)

    if raw_score <= 40:
        level = 3
        label = "Emotional Baggage"
        summary = (
            "You carry light-to-medium emotional expectations and daily responsibilities. "
            "With small consistent positive actions, your burden can reduce quickly."
        )
    elif raw_score <= 60:
        level = 5
        label = "Responsibility Load"
        summary = (
            "You often take care of others and shoulder responsibility. "
            "Learning healthy boundaries will greatly lighten your life burden."
        )
    elif raw_score <= 80:
        level = 7
        label = "Wealth Leakage Phase"
        summary = (
            "Your life script includes lessons around money, loyalty and over-giving. "
            "You are meant to learn wise giving and strong self-protection."
        )
    else:
        level = 9
        label = "Heavy Ancestral Load"
        summary = (
            "You chose deep karmic lessons this lifetime. "
            "After each reset, your wisdom and spiritual credit grow very fast."
        )

    merit_points = max(100, min(raw_score * 20, 2000))

    return {
        "raw_score": raw_score,
        "level": level,
        "label": label,
        "merit_points": merit_points,
        "summary": summary,
    }


# ---------------------------------------------------------
# (B) REAL BAZI-BASED YIN BURDEN ENGINE
# ---------------------------------------------------------

# Stem → Element
STEM_ELEMENT = {
    "甲": "Wood", "乙": "Wood",
    "丙": "Fire", "丁": "Fire",
    "戊": "Earth", "己": "Earth",
    "庚": "Metal", "辛": "Metal",
    "壬": "Water", "癸": "Water",
}

# Branch → Element
BRANCH_ELEMENT = {
    "子": "Water", "亥": "Water",
    "寅": "Wood", "卯": "Wood",
    "巳": "Fire", "午": "Fire",
    "申": "Metal", "酉": "Metal",
    "辰": "Earth", "戌": "Earth", "丑": "Earth", "未": "Earth",
}


def _element_from_stem(stem: str):
    return STEM_ELEMENT.get(stem)


def _element_from_branch(branch: str):
    return BRANCH_ELEMENT.get(branch)


def calculate_yin_burden_from_bazi(chart):
    """
    Real Yin-Burden using:
    - 4 pillars (stem weight = 2, branch weight = 1)
    - Day-Master extra weight = 2
    - 5-element imbalance as karmic indicator
    """

    # -----------------------------
    # 1) Count elements
    # -----------------------------
    elements = {"Wood": 0, "Fire": 0, "Earth": 0, "Metal": 0, "Water": 0}

    pillars = [chart.year, chart.month, chart.day, chart.hour]

    for p in pillars:
        se = _element_from_stem(p.stem)
        be = _element_from_branch(p.branch)
        if se:
            elements[se] += 2
        if be:
            elements[be] += 1

    # Day master weights your personal karma
    dm_elem = _element_from_stem(chart.day_master)
    if dm_elem:
        elements[dm_elem] += 2

    # -----------------------------
    # 2) Compute imbalance
    # -----------------------------
    vals = list(elements.values())
    max_v = max(vals)
    min_v = min(vals)
    imbalance = max_v - min_v
    imbalance_clamped = max(0, min(10, imbalance))

    # -----------------------------
    # 3) Score + Level
    # -----------------------------
    raw_score = 40 + imbalance_clamped * 6
    score = max(10, min(95, raw_score))
    level = max(1, min(9, round(score / 10)))

    # -----------------------------
    # 4) Labels
    # -----------------------------
    if level <= 3:
        label = "Light karmic breeze"
    elif level <= 5:
        label = "Mixed lessons, steady growth"
    elif level <= 7:
        label = "Deep ancestral homework"
    else:
        label = "Intense soul contract this life"

    # -----------------------------
    # 5) Dominant + Weak elements
    # -----------------------------
    dominant = max(elements, key=lambda k: elements[k])
    weak = min(elements, key=lambda k: elements[k])

    # -----------------------------
    # 6) Gentle summary
    # -----------------------------
    parts = []

    parts.append(
        f"Your chart leans strongly toward {dominant} energy, "
        f"while {weak} energy is more subtle and quieter."
    )

    parts.append(
        "This doesn’t mean anything is wrong — it simply reflects the type of "
        "lessons, growth and emotional maturity you chose to experience in this lifetime."
    )

    if level <= 3:
        parts.append(
            "Your karmic load appears light. With small consistent merits and mindful habits, "
            "you maintain smooth life flow."
        )
    elif level <= 5:
        parts.append(
            "There is a blend of ease and challenge. As you balance your five elements "
            "through lifestyle and merits, old patterns soften naturally."
        )
    elif level <= 7:
        parts.append(
            "This pattern often appears in people carrying ancestral stories. "
            "Your merits and emotional work not only transform you, "
            "but uplift your entire family field."
        )
    else:
        parts.append(
            "This life carries a strong soul contract. With sincerity, compassion and service, "
            "you convert heavy karmic weight into powerful spiritual merit."
        )

    summary = " ".join(parts)

    return {
        "level": level,
        "score": score,
        "label": label,
        "elements": elements,
        "dominant_element": dominant,
        "weak_element": weak,
        "summary": summary,
    }
