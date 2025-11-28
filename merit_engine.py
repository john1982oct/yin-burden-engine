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
# ---------------------------
# BaZi-based Yin Burden profile
# ---------------------------

# Five Elements mapping for stems & branches

STEM_ELEMENT = {
    "甲": "Wood", "乙": "Wood",
    "丙": "Fire", "丁": "Fire",
    "戊": "Earth", "己": "Earth",
    "庚": "Metal", "辛": "Metal",
    "壬": "Water", "癸": "Water",
}

BRANCH_ELEMENT = {
    "子": "Water", "亥": "Water",
    "寅": "Wood", "卯": "Wood",
    "巳": "Fire", "午": "Fire",
    "申": "Metal", "酉": "Metal",
    "辰": "Earth", "戌": "Earth", "丑": "Earth", "未": "Earth",
}


def _element_counts_from_bazi_chart(chart) -> dict:
    """
    Count how many times each element appears in 4 pillars (8 characters).
    `chart` can be a BaziChart or a simple dict with keys year/month/day/hour.
    """
    elements = {"Wood": 0, "Fire": 0, "Earth": 0, "Metal": 0, "Water": 0}

    def add_pillar(pillar):
        # pillar can be Pillar object or string like "壬戌"
        if pillar is None:
            return
        if hasattr(pillar, "stem"):
            stem = pillar.stem
            branch = pillar.branch
        else:
            # assume string "XY"
            s = str(pillar)
            if len(s) >= 2:
                stem, branch = s[0], s[1]
            else:
                return

        se = STEM_ELEMENT.get(stem)
        be = BRANCH_ELEMENT.get(branch)
        if se:
            elements[se] += 1
        if be:
            elements[be] += 1

    add_pillar(chart.year)
    add_pillar(chart.month)
    add_pillar(chart.day)
    add_pillar(chart.hour)

    return elements


def calculate_yin_burden_from_bazi(chart):
    """
    Turn a BaZi chart into an 'Yin Burden' profile.

    Idea:
      - Look at 5-element balance across 4 pillars (8 chars).
      - More imbalanced = heavier karmic load.
      - This is symbolic, for Aido use only.
    """
    counts = _element_counts_from_bazi_chart(chart)

    values = [v for v in counts.values() if v > 0]
    if not values:
        # Fallback: no data
        return {
            "level": 5,
            "label": "Unknown Load",
            "score": 50,
            "summary": "Chart data incomplete. Please re-check birth details.",
            "elements": counts,
        }

    max_c = max(values)
    min_c = min(values)
    imbalance = max_c - min_c

    # Basic scaling 0–4 -> 20–90
    # imbalance 0/1 = lighter, 2 = medium, 3+ = heavy
    if imbalance <= 1:
        level = 3
        label = "Light Ancestral Load"
        score = 35 + imbalance * 5  # ~35–40
        summary = (
            "Your five elements are relatively balanced. "
            "Karmic and ancestral burdens are present but not overwhelming. "
            "Good deeds and mindful living can steadily dissolve them."
        )
    elif imbalance == 2:
        level = 6
        label = "Moderate Ancestral Load"
        score = 60
        summary = (
            "Your chart shows a few strong patterns and some missing elements. "
            "This suggests moderate karmic debts and responsibilities in this life. "
            "Consistent merit-making and inner work will help you rebalance."
        )
    else:  # imbalance >= 3
        level = 8
        label = "Heavy Ancestral Load"
        score = 80
        summary = (
            "Your elements are quite imbalanced, pointing to heavier inherited karma "
            "and life challenges. This life is a strong 'repayment and transformation' cycle. "
            "Deep compassion, service, and sincere repentance practices will be powerful."
        )

    return {
        "level": level,
        "label": label,
        "score": score,
        "summary": summary,
        "elements": counts,
    }
