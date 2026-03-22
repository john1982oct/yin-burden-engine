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


DECADE_RELATION_TEXT = {
    "same": {
        "summary": "You may notice parts of your life intensifying — the same patterns, emotions or situations keep showing up more strongly. It can feel like you’re being pushed to face yourself more honestly.",
        "opportunity": "This is a powerful period to step into your true identity and stop shrinking yourself just to fit.",
        "mindful": "Be mindful of reacting too strongly or repeating the same patterns without making a real change.",
    },
    "resource": {
        "summary": "Things may not look dramatic on the outside, but something is quietly rebuilding within you. You may feel the need to slow down, reflect, or reset certain parts of your life.",
        "opportunity": "This is a good period to strengthen your foundation — emotionally, mentally, or in your direction.",
        "mindful": "Be mindful of staying in preparation mode for too long without eventually moving forward.",
    },
    "output": {
        "summary": "You may feel a growing urge to express yourself more — through your work, choices, or the way you show up in life. Holding things in may start to feel harder than before.",
        "opportunity": "This is a strong period for visibility, creation, and showing more of your real self.",
        "mindful": "Be mindful of overextending yourself or giving too much without enough recovery.",
    },
    "control": {
        "summary": "You may notice yourself becoming more focused on control, stability, or getting things in order. There can be stronger pressure to handle responsibilities, finances, or long-term decisions properly.",
        "opportunity": "This is a powerful period to build something solid — whether in career, structure, or life direction.",
        "mindful": "Be mindful of becoming too hard on yourself or trying to control everything around you.",
    },
    "pressure": {
        "summary": "Life may feel like it’s pushing you harder than before. Expectations, responsibilities, or unexpected challenges can make things feel heavier or more intense.",
        "opportunity": "This period can build real strength, resilience, and clarity about what truly matters.",
        "mindful": "Be mindful of stress, burnout, or feeling like you must carry everything alone.",
    },
    "unknown": {
        "summary": "You may feel like things are shifting, even if you cannot fully explain it yet. Certain areas of life may be changing direction quietly.",
        "opportunity": "This is a time to stay open and allow new direction to unfold naturally.",
        "mindful": "Be mindful of resisting change just because it feels unfamiliar.",
    },
}


STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

ELEMENT_GENERATES = {
    "Wood": "Fire",
    "Fire": "Earth",
    "Earth": "Metal",
    "Metal": "Water",
    "Water": "Wood",
}

ELEMENT_CONTROLS = {
    "Wood": "Earth",
    "Fire": "Metal",
    "Earth": "Water",
    "Metal": "Wood",
    "Water": "Fire",
}


def _get_age(birth_dt: datetime) -> int:
    now = datetime.now()
    age = now.year - birth_dt.year
    before_birthday = (now.month, now.day) < (birth_dt.month, birth_dt.day)
    if before_birthday:
        age -= 1
    return age


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
    if produces_map.get(dm_element) == year_element:
        return "produces"

    controls_map = {
        "Wood": "Earth",
        "Fire": "Metal",
        "Earth": "Water",
        "Metal": "Wood",
        "Water": "Fire",
    }
    if controls_map.get(dm_element) == year_element:
        return "drains"

    controlled_by_map = {
        "Wood": "Metal",
        "Fire": "Water",
        "Earth": "Wood",
        "Metal": "Fire",
        "Water": "Earth",
    }
    if controlled_by_map.get(dm_element) == year_element:
        return "controls"

    return "controlled_by"


def _current_year_info():
    now = datetime.now()
    yp = compute_year_pillar_basic(now)
    return {
        "element": STEM_ELEMENT.get(yp.stem, "Unknown"),
        "year": now.year,
    }


def _get_month_stem_branch(chart):
    """
    Safely supports a few possible chart shapes.
    """
    if hasattr(chart, "month") and hasattr(chart.month, "stem") and hasattr(chart.month, "branch"):
        return chart.month.stem, chart.month.branch

    if hasattr(chart, "month_pillar"):
        month_pillar = chart.month_pillar

        if isinstance(month_pillar, dict):
            return month_pillar.get("stem"), month_pillar.get("branch")

        if hasattr(month_pillar, "stem") and hasattr(month_pillar, "branch"):
            return month_pillar.stem, month_pillar.branch

    return None, None


def _get_da_yun_period_index(birth_dt: datetime) -> int:
    """
    Light Da Yun layer only:
    - still approximate
    - first 10-year cycle starts around age 10
    - enough for a lead magnet without full traditional complexity
    """
    age = _get_age(birth_dt)

    if age < 10:
        return 0

    return age // 10


def _shift_stem(stem: str, steps: int) -> str:
    if stem not in STEMS:
        return stem
    idx = STEMS.index(stem)
    return STEMS[(idx + steps) % 10]


def _shift_branch(branch: str, steps: int) -> str:
    if branch not in BRANCHES:
        return branch
    idx = BRANCHES.index(branch)
    return BRANCHES[(idx + steps) % 12]


def _get_light_da_yun_pillar(chart, birth_dt: datetime):
    """
    Light Da Yun approximation:
    - uses month pillar as base
    - moves forward one pillar per 10-year period
    - does NOT yet handle forward/reverse direction
    - does NOT yet calculate exact traditional Da Yun start age
    """
    month_stem, month_branch = _get_month_stem_branch(chart)
    period_index = _get_da_yun_period_index(birth_dt)

    if not month_stem or not month_branch:
        return {
            "index": period_index,
            "stem": None,
            "branch": None,
            "pillar": None,
        }

    da_yun_stem = _shift_stem(month_stem, period_index)
    da_yun_branch = _shift_branch(month_branch, period_index)

    return {
        "index": period_index,
        "stem": da_yun_stem,
        "branch": da_yun_branch,
        "pillar": f"{da_yun_stem}{da_yun_branch}",
    }


def _get_element_relation(day_master_element: str, other_element: str) -> str:
    """
    Human-usable relation naming for decade interpretation.
    """
    if day_master_element == other_element:
        return "same"

    if ELEMENT_GENERATES.get(other_element) == day_master_element:
        return "resource"

    if ELEMENT_GENERATES.get(day_master_element) == other_element:
        return "output"

    if ELEMENT_CONTROLS.get(day_master_element) == other_element:
        return "control"

    if ELEMENT_CONTROLS.get(other_element) == day_master_element:
        return "pressure"

    return "unknown"


def _get_current_decade_data(chart, birth_dt: datetime, day_master_element: str):
    da_yun = _get_light_da_yun_pillar(chart, birth_dt)

    if not da_yun["stem"]:
        return {
            "text": DECADE_RELATION_TEXT["unknown"],
            "debug": {
                "period_index": da_yun["index"],
                "da_yun_stem": da_yun["stem"],
                "da_yun_branch": da_yun["branch"],
                "da_yun_pillar": da_yun["pillar"],
                "da_yun_element": None,
                "relation": "unknown",
            },
        }

    da_yun_element = STEM_ELEMENT.get(da_yun["stem"], "Unknown")
    relation = _get_element_relation(day_master_element, da_yun_element)

    return {
        "text": DECADE_RELATION_TEXT.get(relation, DECADE_RELATION_TEXT["unknown"]),
        "debug": {
            "period_index": da_yun["index"],
            "da_yun_stem": da_yun["stem"],
            "da_yun_branch": da_yun["branch"],
            "da_yun_pillar": da_yun["pillar"],
            "da_yun_element": da_yun_element,
            "relation": relation,
        },
    }


def generate_current_phase_reading(chart, birth_dt: datetime):
    day_master = chart.day_master
    day_branch = chart.day.branch

    element = STEM_ELEMENT.get(day_master, "Unknown")
    underlying = BRANCH_ELEMENT.get(day_branch, "Unknown")

    personality = DAY_MASTER_PERSONALITY.get(
        day_master,
        "You have your own natural way of responding to life.",
    )
    phase = CURRENT_PHASE_TEXT.get(
        element,
        "You are in a phase where change and adjustment are becoming more noticeable.",
    )
    underlying_text = UNDERLYING_RHYTHM_TEXT.get(
        underlying,
        "Deep down, you may need more space, clarity and emotional steadiness.",
    )

    year_info = _current_year_info()
    relation = _relation_of_year_to_day_master(element, year_info["element"])

    year_summary = YEAR_FEELING.get(
        relation,
        "This year brings a mix of movement, adjustment and learning.",
    )
    year_opportunity = YEAR_OPPORTUNITY.get(
        relation,
        "There are still useful openings if you move with awareness.",
    )
    year_mindful = YEAR_MINDFUL.get(
        relation,
        "Be mindful of imbalance and how you use your energy.",
    )

    decade_data = _get_current_decade_data(chart, birth_dt, element)
    decade = decade_data["text"]

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
            "debug": decade_data["debug"],
        },
        "cta": {
            "title": "Go Deeper",
            "summary": "This is a surface-level reading. A full chart reading can reveal deeper timing and patterns behind your life.",
        },
    }
