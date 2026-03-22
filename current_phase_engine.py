from datetime import datetime

from merit_engine import STEM_ELEMENT, BRANCH_ELEMENT
from bazi_core import compute_year_pillar_basic


DAY_MASTER_PERSONALITY = {
    "甲": "You tend to be straightforward, growth-driven and value progress.",
    "乙": "You tend to be adaptable, thoughtful and sensitive to your surroundings.",
    "丙": "You tend to be expressive, energetic and naturally visible to others.",
    "丁": "You tend to be perceptive, warm and quietly influential.",
    "戊": "You tend to be stable, dependable and naturally supportive to others.",
    "己": "You tend to be careful, detail-oriented and thoughtful in your actions.",
    "庚": "You tend to be direct, decisive and value clarity and strength.",
    "辛": "You tend to be refined, observant and sensitive to quality and detail.",
    "壬": "You tend to be intuitive, flexible and able to see the bigger picture.",
    "癸": "You tend to be reflective, sensitive and deeply aware of emotional undercurrents.",
}


CURRENT_PHASE_TEXT = {
    "Wood": "You are in a phase where growth, change and forward movement feel especially important.",
    "Fire": "You are in a phase where expression, visibility and emotional energy become more active.",
    "Earth": "You are in a phase where stability, responsibility and long-term foundations matter more.",
    "Metal": "You are in a phase where structure, decisions and clarity become more noticeable.",
    "Water": "You are in a phase where reflection, intuition and inner adjustment become more important.",
}


UNDERLYING_RHYTHM_TEXT = {
    "Wood": "Deep down, you need movement and progress.",
    "Fire": "Deep down, you need warmth, encouragement and space to express yourself.",
    "Earth": "Deep down, you need stability and something you can rely on emotionally.",
    "Metal": "Deep down, you need clarity and space to think.",
    "Water": "Deep down, you need quiet time to process and recharge.",
}


YEAR_FEELING = {
    "same": "This year feels more intense — whatever you are experiencing tends to become stronger.",
    "produces": "This year feels smoother — things may flow more naturally without forcing.",
    "controls": "This year may feel pressuring — you may be pushed to step up or handle more.",
    "drains": "This year can feel busy — a lot of your energy may go into doing and giving.",
    "controlled_by": "This year may feel slightly restrictive — things may not move fully your way.",
}

YEAR_OPPORTUNITY = {
    "same": "You can make strong progress if you use your strengths well.",
    "produces": "You may find things aligning more easily when you take action.",
    "controls": "Pressure can become growth if you handle it well.",
    "drains": "Opportunities come through action and showing up.",
    "controlled_by": "You can refine yourself and become sharper this year.",
}

YEAR_MINDFUL = {
    "same": "Be mindful of overdoing or repeating patterns too strongly.",
    "produces": "Be mindful of becoming too comfortable.",
    "controls": "Be mindful of stress and reacting too quickly.",
    "drains": "Be mindful of burnout and overcommitment.",
    "controlled_by": "Be mindful of frustration and impatience.",
}


DECADE_PHASE = {
    "20s": {
        "summary": "This phase of life is about exploration, trial and discovering your direction.",
        "opportunity": "You have room to try, learn and pivot without being locked in yet.",
        "mindful": "Be mindful of drifting too long without building something stable.",
    },
    "30s": {
        "summary": "This phase is about building, stabilising and making more solid life decisions.",
        "opportunity": "This is a powerful time to establish career, relationships and long-term direction.",
        "mindful": "Be mindful of pressure, comparison or feeling like you must rush everything.",
    },
    "40s": {
        "summary": "This phase is about refinement, alignment and adjusting what truly fits you.",
        "opportunity": "You can focus on what really matters and remove what no longer aligns.",
        "mindful": "Be mindful of holding onto roles or identities that are no longer right for you.",
    },
    "50s+": {
        "summary": "This phase is about consolidation, wisdom and choosing what truly matters.",
        "opportunity": "You can move with clarity and focus on meaningful areas of life.",
        "mindful": "Be mindful of becoming too rigid or resistant to change.",
    },
}


def _get_age(birth_dt: datetime) -> int:
    now = datetime.now()
    age = now.year - birth_dt.year
    before_birthday = (now.month, now.day) < (birth_dt.month, birth_dt.day)
    if before_birthday:
        age -= 1
    return age


def _get_decade_bucket(age: int) -> str:
    if age < 30:
        return "20s"
    elif age < 40:
        return "30s"
    elif age < 50:
        return "40s"
    else:
        return "50s+"


def _relation_of_year_to_day_master(dm_element: str, year_element: str) -> str:
    if dm_element == year_element:
        return "same"

    produces_map = {
        "Wood": "Water",
        "Fire": "Wood",
        "Earth": "Fire",
        "Metal": "Earth",
        "Water": "Metal",
    }
    if produces_map[dm_element] == year_element:
        return "produces"

    controls_map = {
        "Wood": "Earth",
        "Fire": "Metal",
        "Earth": "Water",
        "Metal": "Wood",
        "Water": "Fire",
    }
    if controls_map[dm_element] == year_element:
        return "drains"

    controlled_by_map = {
        "Wood": "Metal",
        "Fire": "Water",
        "Earth": "Wood",
        "Metal": "Fire",
        "Water": "Earth",
    }
    if controlled_by_map[dm_element] == year_element:
        return "controls"

    return "controlled_by"


def _current_year_info():
    now = datetime.now()
    yp = compute_year_pillar_basic(now)
    return {
        "element": STEM_ELEMENT.get(yp.stem, "Unknown"),
        "year": now.year,
    }


def generate_current_phase_reading(chart, birth_dt: datetime):
    day_master = chart.day_master
    day_branch = chart.day.branch

    element = STEM_ELEMENT.get(day_master)
    underlying = BRANCH_ELEMENT.get(day_branch)

    personality = DAY_MASTER_PERSONALITY.get(day_master)
    phase = CURRENT_PHASE_TEXT.get(element)
    underlying_text = UNDERLYING_RHYTHM_TEXT.get(underlying)

    year_info = _current_year_info()
    relation = _relation_of_year_to_day_master(element, year_info["element"])

    year_summary = YEAR_FEELING.get(relation)
    year_opportunity = YEAR_OPPORTUNITY.get(relation)
    year_mindful = YEAR_MINDFUL.get(relation)

    age = _get_age(birth_dt)
    decade_key = _get_decade_bucket(age)
    decade = DECADE_PHASE.get(decade_key)

    return {
        "tool_role": "This tool helps you understand what’s happening in your life right now, what opportunities are opening up, and what to be mindful of.",
        "current_phase": {
            "title": "What’s Happening In Your Life Right Now",
            "summary": f"{personality} {phase} {underlying_text}",
        },
        "this_year": {
            "title": "What This Year Is Bringing",
            "year": year_info["year"],
            "summary": year_summary,
            "opportunity": year_opportunity,
            "mindful_of": year_mindful,
        },
        "current_decade": {
            "title": "Your Current Life Stage",
            "summary": decade["summary"],
            "opportunity": decade["opportunity"],
            "mindful_of": decade["mindful"],
        },
        "cta": {
            "title": "Go Deeper",
            "summary": "This is a surface-level reading. A full chart reading can reveal deeper timing and patterns behind your life.",
        },
    }
