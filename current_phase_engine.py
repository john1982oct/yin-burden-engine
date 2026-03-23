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
    "Wood": "Right now, growth, change and forward movement feel especially important.",
    "Fire": "Right now, expression, visibility and emotional energy become more active.",
    "Earth": "Right now, stability, responsibility and long-term foundations matter more.",
    "Metal": "Right now, structure, decisions and clarity become more noticeable.",
    "Water": "Right now, reflection, intuition and inner adjustment become more important.",
}


UNDERLYING_RHYTHM_TEXT = {
    "Wood": "Deep down, you need movement and progress.",
    "Fire": "Deep down, you need warmth, encouragement and room to express what you really feel.",
    "Earth": "Deep down, you need stability and something you can rely on emotionally.",
    "Metal": "Deep down, you need clarity, quiet and space to sort things out properly.",
    "Water": "Deep down, you need quiet time to process, retreat and recharge.",
}


YEAR_FEELING = {
    "same": "This year feels more intense — whatever is already happening in your life may feel stronger and harder to ignore.",
    "produces": "This year feels smoother — things may flow more naturally when you stop forcing every step.",
    "controls": "This year may feel pressuring — you may be pushed to step up, respond faster, or handle more than usual.",
    "drains": "This year can feel busy — a lot of your energy may go into doing, giving, and showing up.",
    "controlled_by": "This year may feel slightly restrictive — things may not move fully your way, but there is still something important to learn here.",
}

YEAR_OPPORTUNITY = {
    "same": "You can make strong progress if you use your natural strengths with maturity.",
    "produces": "You may find doors opening more easily when you take clear, steady action.",
    "controls": "Pressure can become growth if you respond with steadiness instead of panic.",
    "drains": "Opportunities come through action, consistency, and staying engaged with life.",
    "controlled_by": "You can refine yourself, sharpen your priorities, and become clearer about what matters.",
}

YEAR_MINDFUL = {
    "same": "Be mindful of overdoing things or repeating old patterns too strongly.",
    "produces": "Be mindful of becoming too comfortable and waiting too long to act.",
    "controls": "Be mindful of stress, impatience, and reacting too quickly.",
    "drains": "Be mindful of burnout, overcommitment, or giving more than you can sustain.",
    "controlled_by": "Be mindful of frustration, resistance, and taking delays too personally.",
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
    age = _get_age(birth_dt)
    return 0 if age < 10 else age // 10


def _shift_stem(stem: str, steps: int) -> str:
    if stem not in STEMS:
        return stem
    return STEMS[(STEMS.index(stem) + steps) % 10]


def _shift_branch(branch: str, steps: int) -> str:
    if branch not in BRANCHES:
        return branch
    return BRANCHES[(BRANCHES.index(branch) + steps) % 12]


def _get_light_da_yun_pillar(chart, birth_dt: datetime):
    month_stem, month_branch = _get_month_stem_branch(chart)
    idx = _get_da_yun_period_index(birth_dt)

    if not month_stem or not month_branch:
        return {"stem": None, "branch": None}

    return {
        "stem": _shift_stem(month_stem, idx),
        "branch": _shift_branch(month_branch, idx),
    }


def _get_element_relation(dm, other):
    if dm == other:
        return "same"
    if ELEMENT_GENERATES.get(other) == dm:
        return "resource"
    if ELEMENT_GENERATES.get(dm) == other:
        return "output"
    if ELEMENT_CONTROLS.get(dm) == other:
        return "control"
    if ELEMENT_CONTROLS.get(other) == dm:
        return "pressure"
    return "unknown"


def _get_current_decade_text(chart, birth_dt, dm_element):
    da = _get_light_da_yun_pillar(chart, birth_dt)
    if not da.get("stem"):
        return DECADE_RELATION_TEXT["unknown"]

    rel = _get_element_relation(dm_element, STEM_ELEMENT.get(da["stem"], "Unknown"))
    return DECADE_RELATION_TEXT.get(rel, DECADE_RELATION_TEXT["unknown"])


def _build_current_phase_summary(p, ph, u):
    p = (p or "You have your own way of moving through life.").rstrip(".")
    ph = (ph or "Right now, a meaningful life phase is unfolding.").rstrip(".")
    u = (u or "Deep down, your inner rhythm is asking for more awareness.").rstrip(".")
    return f"{p}. {ph}. {u}."


def generate_current_phase_reading(chart, birth_dt: datetime):
    dm = chart.day_master
    db = chart.day.branch

    element = STEM_ELEMENT.get(dm, "Unknown")
    underlying = BRANCH_ELEMENT.get(db, "Unknown")

    personality = DAY_MASTER_PERSONALITY.get(dm)
    phase = CURRENT_PHASE_TEXT.get(element)
    underlying_text = UNDERLYING_RHYTHM_TEXT.get(underlying)

    year = _current_year_info()
    rel = _relation_of_year_to_day_master(element, year["element"])

    decade = _get_current_decade_text(chart, birth_dt, element)

    return {
        "day_master": dm,
        "day_master_element": element,
        "day_branch": db,
        "day_branch_element": underlying,

        "current_phase": {
            "title": "What’s Happening In Your Life Right Now",
            "summary": _build_current_phase_summary(personality, phase, underlying_text),
        },
        "this_year": {
            "title": "What This Year Is Bringing",
            "year": year["year"],
            "summary": YEAR_FEELING.get(rel, "This year is bringing a meaningful shift in pace and priorities."),
            "opportunity": YEAR_OPPORTUNITY.get(rel, "There is still useful momentum here if you respond with awareness."),
            "mindful_of": YEAR_MINDFUL.get(rel, "Be mindful of imbalance and how you use your energy."),
        },
        "current_decade": {
            "title": "Your Current Life Stage",
            "summary": decade["summary"],
            "opportunity": decade["opportunity"],
            "mindful_of": decade["mindful"],
        },
        "cta": {
            "title": "Go Deeper",
            "summary": "This is only the surface of your timing. A full reading can show why these patterns are happening, what is opening next, and how to move through it with more clarity.",
        },
    }
