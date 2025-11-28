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

# Element psychological stories
ELEMENT_STORIES = {
    "Wood": {
        "strong": (
            "When Wood is strong, you carry the energy of growth, planning and courage. "
            "You like to move forward, initiate change and protect people you care about."
        ),
        "weak": (
            "When Wood is weaker, it can feel like confidence, direction or motivation "
            "go up and down. You may hesitate before taking the next brave step."
        ),
    },
    "Fire": {
        "strong": (
            "When Fire is strong, you radiate warmth, passion and charisma. "
            "You naturally light up rooms, inspire others and bring joy."
        ),
        "weak": (
            "When Fire is weaker, your enthusiasm may burn out quickly or you may hide "
            "your true feelings, worrying about being too much for others."
        ),
    },
    "Earth": {
        "strong": (
            "When Earth is strong, you hold space for others. You are dependable, "
            "grounded and often become the emotional anchor for family and friends."
        ),
        "weak": (
            "When Earth is weaker, boundaries can blur. You may feel responsible for "
            "everyone, yet find it hard to feel truly supported yourself."
        ),
    },
    "Metal": {
        "strong": (
            "When Metal is strong, you value principles, integrity and standards. "
            "You see clearly what is right for you and you dislike unfairness."
        ),
        "weak": (
            "When Metal is weaker, self-criticism or doubt may appear, or you may find "
            "it hard to say no even when something does not feel aligned."
        ),
    },
    "Water": {
        "strong": (
            "When Water is strong, you are intuitive, reflective and sensitive to energy. "
            "You can understand emotions deeply, even unspoken ones."
        ),
        "weak": (
            "When Water is weaker, emotions may be bottled up or flow in sudden waves. "
            "Rest, silence and honest sharing become very important for you."
        ),
    },
}

# Element-specific merit ideas
GOOD_DEEDS_BY_ELEMENT = {
    "Wood": [
        "Support learning and growth: sponsor classes, share knowledge, mentor someone younger.",
        "Plant trees or support environmental projects that protect forests and green spaces.",
        "Stand up gently for people who feel small, helping them find their voice.",
    ],
    "Fire": [
        "Bring warmth to lonely people: visit elders, check in on friends, brighten someone’s day.",
        "Use your charisma for good: encourage shy people, celebrate others' wins sincerely.",
        "Volunteer at events that spread joy, culture or community bonding.",
    ],
    "Earth": [
        "Offer stable help: cook for someone tired, accompany a stressed friend to appointments.",
        "Donate regularly (even small amounts) to causes that provide food, shelter or care.",
        "Practice healthy boundaries so your kindness is sustainable, not exhausting.",
    ],
    "Metal": [
        "Protect fairness: speak gently when you see unfair treatment or bullying.",
        "Use your organisation skills to help others sort finances, documents or life admin.",
        "Practice letting go by decluttering and donating items that can bless others.",
    ],
    "Water": [
        "Listen deeply to someone who needs to talk, without judging or rushing to fix.",
        "Support mental-health or counselling initiatives, even in small ways.",
        "Create quiet spaces of peace: a small prayer/meditation corner, or calm playlists to share.",
    ],
}


def _element_from_stem(stem: str):
    return STEM_ELEMENT.get(stem)


def _element_from_branch(branch: str):
    return BRANCH_ELEMENT.get(branch)


def calculate_yin_burden_from_bazi(chart):
    """
    Turn a BaZi chart into a gentle Yin-Burden profile.

    Logic:
      - Count 5 elements from 4 pillars (stems weight 2, branches weight 1).
      - Day-Master element gets extra weight (personal karma focus).
      - Imbalance (max - min) becomes symbolic karmic load.
      - More imbalance = deeper 'homework', but always framed as growth.
    """

    # -----------------------------
    # 1) Count elements with weights
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

    # Day Master focus
    dm_elem = _element_from_stem(chart.day_master)
    if dm_elem:
        elements[dm_elem] += 2

    # -----------------------------
    # 2) Imbalance calculation
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

    if level <= 3:
        label = "Light karmic breeze"
    elif level <= 5:
        label = "Mixed lessons, steady growth"
    elif level <= 7:
        label = "Deep ancestral homework"
    else:
        label = "Intense soul contract this life"

    # -----------------------------
    # 4) Dominant & weak element
    # -----------------------------
    dominant = max(elements, key=lambda k: elements[k])
    weak = min(elements, key=lambda k: elements[k])

    dom_story = ELEMENT_STORIES[dominant]["strong"]
    weak_story = ELEMENT_STORIES[weak]["weak"]

    dom_deeds = GOOD_DEEDS_BY_ELEMENT.get(dominant, [])
    weak_deeds = GOOD_DEEDS_BY_ELEMENT.get(weak, [])

    # Combine 3–5 deeds (2 from dominant, 1–2 from weak)
    good_deeds = []
    good_deeds.extend(dom_deeds[:2])
    if weak_deeds:
        good_deeds.append(weak_deeds[0])
    if len(weak_deeds) > 1 and len(good_deeds) < 5:
        good_deeds.append(weak_deeds[1])

    # -----------------------------
    # 5) Warm combined summary
    # -----------------------------
    parts = []

    parts.append(
        f"Your chart leans strongly toward {dominant} energy, "
        f"while {weak} energy is softer and more hidden."
    )

    parts.append(dom_story)
    parts.append(weak_story)

    if level <= 3:
        parts.append(
            "Overall, your karmic load appears light. With simple consistent merits and "
            "mindful habits, you can maintain a smooth and relaxed life flow."
        )
    elif level <= 5:
        parts.append(
            "Your chart suggests a mix of ease and challenge. As you balance your five elements "
            "through actions and mindset, old patterns will naturally soften."
        )
    elif level <= 7:
        parts.append(
            "This pattern is common in people carrying some ancestral stories. "
            "Your personal growth and merits do not only heal you, they also gently uplift "
            "your family and future generations."
        )
    else:
        parts.append(
            "This life carries a strong soul contract. With sincerity, compassion and service, "
            "you can transform heavier karmic weight into very powerful spiritual credit."
        )

    parts.append(
        "Practical next steps: choose one or two simple good deeds from the suggestions above "
        "and repeat them steadily. Small actions, done with heart, are extremely powerful."
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
        "dominant_story": dom_story,
        "weak_story": weak_story,
        "good_deeds": good_deeds,
    }
