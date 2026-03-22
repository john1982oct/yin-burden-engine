# current_phase_engine.py

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
    "Wood": "Deep down, you need movement and progress. When things feel stuck, it can affect you more than you show.",
    "Fire": "Deep down, you need warmth, encouragement and space to express yourself.",
    "Earth": "Deep down, you need stability and something you can rely on emotionally.",
    "Metal": "Deep down, you need clarity, order and space to breathe mentally.",
    "Water": "Deep down, you need quiet time to process and recharge emotionally.",
}


# 🔥 HUMANISED YEAR TEXT (NO JARGON)

YEAR_FEELING = {
    "same": "This year feels like things are intensifying. Patterns in your life may become more obvious, and whatever you are going through can feel stronger than usual.",

    "produces": "This year feels a bit smoother. You may notice that things don’t require as much force, and support or opportunities appear more naturally.",

    "controls": "This year may feel more pressuring at times. You might face expectations, responsibilities or situations that push you to step up.",

    "drains": "This year can feel busy and demanding. You may find yourself giving more, doing more, and needing to manage your energy carefully.",

    "controlled_by": "This year may feel slightly restrictive or uncomfortable at times. Situations may not fully go your way, requiring patience and adjustment.",
}


YEAR_OPPORTUNITY = {
    "same": "If you use your natural strengths well, you can make strong progress this year.",
    "produces": "You may find it easier to move forward, especially when you stay open to help and timing.",
    "controls": "Growth can happen quickly if you respond well to pressure instead of resisting it.",
    "drains": "This is a year where visibility and action can open doors, if you pace yourself properly.",
    "controlled_by": "This is a good year to refine your approach and become sharper in how you handle situations.",
}


YEAR_MINDFUL = {
    "same": "Be mindful of overdoing things or repeating the same patterns too strongly.",
    "produces": "Be mindful of becoming too comfortable and delaying important action.",
    "controls": "Be mindful of stress, tension or reacting too quickly under pressure.",
    "drains": "Be mindful of burnout and overcommitting yourself.",
    "controlled_by": "Be mindful of frustration or feeling stuck — this phase requires patience.",
}


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
    year_pillar = compute_year_pillar_basic(now)

    return {
        "pillar": f"{year_pillar.stem}{year_pillar.branch}",
        "element": STEM_ELEMENT.get(year_pillar.stem, "Unknown"),
        "year": now.year,
    }


def generate_current_phase_reading(chart):

    day_master = chart.day_master
    day_branch = chart.day.branch

    element = STEM_ELEMENT.get(day_master, "Unknown")
    underlying = BRANCH_ELEMENT.get(day_branch, "Unknown")

    personality = DAY_MASTER_PERSONALITY.get(day_master)
    phase = CURRENT_PHASE_TEXT.get(element)
    underlying_text = UNDERLYING_RHYTHM_TEXT.get(underlying)

    year_info = _current_year_info()
    relation = _relation_of_year_to_day_master(element, year_info["element"])

    year_summary = YEAR_FEELING.get(relation)
    year_opportunity = YEAR_OPPORTUNITY.get(relation)
    year_mindful = YEAR_MINDFUL.get(relation)

    return {
        "tool_role": "This tool helps you understand what’s happening in your life right now, what opportunities are opening up, and what to be mindful of.",

        "current_phase": {
            "title": "What’s Happening In Your Life Right Now",
            "summary": f"{personality} {phase} {underlying_text}"
        },

        "this_year": {
            "title": "What This Year Is Bringing",
            "year": year_info["year"],
            "summary": year_summary,
            "opportunity": year_opportunity,
            "mindful_of": year_mindful,
        },

        "cta": {
            "title": "Go Deeper",
            "summary": "This is a surface-level reading. A full chart reading can reveal the deeper timing and patterns behind what you are experiencing."
        }
    }
