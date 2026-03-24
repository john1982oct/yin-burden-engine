from datetime import datetime

from merit_engine import STEM_ELEMENT, BRANCH_ELEMENT
from bazi_core import compute_year_pillar_basic


DAY_MASTER_PERSONALITY = {
    "甲": [
        "You tend to be straightforward, growth-driven and value progress.",
        "You naturally move toward growth, clarity and forward momentum.",
        "You are driven by progress and tend to approach life with directness and purpose.",
    ],
    "乙": [
        "You tend to be adaptable, thoughtful and sensitive to your surroundings.",
        "You have a natural ability to adjust, read your environment and respond with care.",
        "You tend to be flexible, perceptive and attuned to the feelings and energy around you.",
    ],
    "丙": [
        "You tend to be expressive, energetic and naturally visible to others.",
        "You have a warm, outward energy that draws others in and lights up a room.",
        "You tend to be lively, open and someone others naturally notice and remember.",
    ],
    "丁": [
        "You tend to be perceptive, warm and quietly influential.",
        "You have a steady inner warmth that others feel even when you say very little.",
        "You tend to be thoughtful, observant and someone whose quiet presence carries real weight.",
    ],
    "戊": [
        "You tend to be stable, dependable and naturally supportive to others.",
        "You are someone others lean on — steady, grounded and genuinely reliable.",
        "You tend to bring calm and steadiness, making those around you feel supported and safe.",
    ],
    "己": [
        "You tend to be careful, detail-oriented and thoughtful in your actions.",
        "You pay close attention to what others miss and move through life with care and precision.",
        "You tend to be conscientious, measured and deeply aware of the finer details in life.",
    ],
    "庚": [
        "You tend to be direct, decisive and value clarity and strength.",
        "You move with purpose, say what you mean and value people who do the same.",
        "You tend to be clear-headed, action-oriented and someone who values honesty over comfort.",
    ],
    "辛": [
        "You tend to be refined, observant and sensitive to quality and detail.",
        "You notice what others overlook and hold yourself and your environment to a high standard.",
        "You tend to be precise, discerning and drawn to beauty, quality and things done properly.",
    ],
    "壬": [
        "You tend to be intuitive, flexible and able to see the bigger picture.",
        "You have a natural ability to read between the lines and flow with what life brings.",
        "You tend to be open-minded, perceptive and good at sensing where things are heading.",
    ],
    "癸": [
        "You tend to be reflective, sensitive and deeply aware of emotional undercurrents.",
        "You feel things deeply and have a quiet, intuitive sense of what others are really going through.",
        "You tend to be inward, emotionally perceptive and attuned to the subtler layers of life.",
    ],
}


CURRENT_PHASE_TEXT = {
    "Wood": [
        "Right now, growth, change and forward movement feel especially important.",
        "This is a time when new direction, expansion and moving forward carry more weight.",
        "There is a pull toward growth right now — change and forward movement are calling for attention.",
    ],
    "Fire": [
        "Right now, expression, visibility and emotional energy become more active.",
        "This is a period when showing up, being seen and feeling things more vividly becomes the theme.",
        "Your inner fire is more active right now — expression, connection and emotional presence feel heightened.",
    ],
    "Earth": [
        "Right now, stability, responsibility and long-term foundations matter more.",
        "This is a time when building something steady, handling responsibilities and thinking long-term feels pressing.",
        "There is a pull toward groundedness right now — structure, reliability and lasting decisions take center stage.",
    ],
    "Metal": [
        "Right now, structure, decisions and clarity become more noticeable.",
        "This is a period when getting clear, making decisions and creating better order in your life feels necessary.",
        "There is a sharpening quality to this time — clarity, structure and cutting through the noise become important.",
    ],
    "Water": [
        "Right now, reflection, intuition and inner adjustment become more important.",
        "This is a quieter, more inward time — your instincts and inner knowing are asking to be heard.",
        "There is a call to slow down and listen inward right now — reflection and quiet recalibration are the theme.",
    ],
}


UNDERLYING_RHYTHM_TEXT = {
    "Wood": [
        "Deep down, you need movement and progress.",
        "Underneath it all, you need to feel like things are moving and that your efforts are going somewhere.",
        "At your core, you crave forward motion — stagnation tends to drain you more than others.",
    ],
    "Fire": [
        "Deep down, you need warmth, encouragement and room to express what you really feel.",
        "Underneath it all, you need connection, warmth and the freedom to express yourself openly.",
        "At your core, you need to feel seen and encouraged — being heard matters deeply to you.",
    ],
    "Earth": [
        "Deep down, you need stability and something you can rely on emotionally.",
        "Underneath it all, you need groundedness — a sense of safety and something consistent to hold onto.",
        "At your core, you need reliability and emotional steadiness — uncertainty tends to wear on you quietly.",
    ],
    "Metal": [
        "Deep down, you need clarity, quiet and space to sort things out properly.",
        "Underneath it all, you need order, stillness and the room to think things through without noise.",
        "At your core, you need mental clarity — too much chaos or ambiguity tends to leave you feeling unsettled.",
    ],
    "Water": [
        "Deep down, you need quiet time to process, retreat and recharge.",
        "Underneath it all, you need space to absorb, reflect and come back to yourself.",
        "At your core, you need rest and inner space — pushing through without pausing tends to cost you more than you realize.",
    ],
}


CURRENT_PHASE_DETAILS = {
    "Wood": "Because you naturally reach toward what's next, periods that activate Wood energy can feel particularly alive. Growth is not just happening around you — it's being asked of you. The pull you feel right now is real, and responding to it with intention tends to serve you well.",
    "Fire": "Because you carry a natural warmth and expressiveness, periods that activate Fire energy tend to amplify how visible and emotionally present you feel. What you're sensing is not just restlessness — it's a genuine invitation to show up more fully and let more of yourself be seen.",
    "Earth": "Because stability and reliability run deep in your nature, periods that activate Earth energy bring your focus to what is lasting and worth protecting. The weight you feel around responsibilities right now is your nature responding to real demands — and you are more capable of meeting them than you might think.",
    "Metal": "Because you tend to value clarity and doing things properly, periods that activate Metal energy sharpen your attention and raise your standards. What feels like pressure to get things right is partly your own nature asking for more order — and clearing the noise tends to help more than pushing harder.",
    "Water": "Because you process life deeply and intuitively, periods that activate Water energy draw you inward. What may feel like low energy or withdrawal is often your system doing important inner work. Giving yourself permission to slow down right now is not weakness — it's how you restore and clarify.",
}

YEAR_DETAILS = {
    "same": "When the year carries the same element as your day master, it tends to amplify whatever is already present in your life. Your natural strengths become more available, but so do your habitual blind spots. It's a year that rewards honest self-awareness more than usual.",
    "produces": "When the year's element nourishes your day master, there is a quieter support working in your favour. Things may feel less forced, and opportunities can arrive through ordinary moments rather than dramatic ones. The key is staying engaged and not waiting for things to be perfect before you move.",
    "controls": "When the year's element challenges your day master, life tends to ask more of you than usual. This is not necessarily a bad thing — pressure applied well tends to create clarity and motion. The challenge is to respond to what's being asked without wearing yourself out in the process.",
    "drains": "When your day master is expressing outward into the year's element, much of your energy goes into doing, contributing and showing up. This can feel fulfilling and busy at the same time. Pacing yourself and recognising when you've given enough are the most useful skills this year.",
    "controlled_by": "When the year's element limits your day master, certain things may not move as quickly or freely as you'd like. Rather than fighting the current, this tends to be a year where refining, reflecting and letting go of what isn't working pays off more than pushing forward.",
}

DECADE_DETAILS = {
    "same": "Decades that carry the same element as your day master tend to develop your sense of self over time. The intensity of this period is asking you to become more grounded in who you genuinely are — not who you've been performing or hiding behind. What emerges is usually a stronger, more honest version of yourself.",
    "resource": "Decades with a resource quality tend to quietly restore and rebuild what has been spent. Over time, this phase develops your inner resilience, deepens your self-understanding, and helps you reconnect with what you truly need. Growth during this period tends to be internal before it becomes visible.",
    "output": "Decades with an output quality tend to develop your creative and expressive capacity over time. What begins as a pull to do more or be seen more can grow into genuine contribution and skill. This phase tends to reward those who keep showing up and refining how they share themselves with the world.",
    "control": "Decades with a control quality tend to develop discipline, discernment and real-world capability over time. The pressure to handle more and take responsibility tends to build into lasting competence. What may feel heavy at first often becomes a quiet source of confidence.",
    "pressure": "Decades with a pressure quality tend to develop resilience and genuine clarity about what matters. Being pushed harder than usual over time has a way of stripping away what is unnecessary and revealing what is real. What survives this phase tends to be the most solid and true.",
    "unknown": "When the decade's energy is harder to classify, the development it brings tends to be more subtle and gradual. Over time, you may find yourself growing in ways that are difficult to name but unmistakably real — more open, more flexible, more at ease with uncertainty than you once were.",
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


def _pick_variant(options: list, seed_text: str) -> str:
    index = sum(ord(c) for c in seed_text) % len(options)
    return options[index]


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

    seed = dm + db + element
    personality = _pick_variant(DAY_MASTER_PERSONALITY[dm], seed) if dm in DAY_MASTER_PERSONALITY else None
    phase = _pick_variant(CURRENT_PHASE_TEXT[element], seed) if element in CURRENT_PHASE_TEXT else None
    underlying_text = _pick_variant(UNDERLYING_RHYTHM_TEXT[underlying], seed) if underlying in UNDERLYING_RHYTHM_TEXT else None

    year = _current_year_info()
    rel = _relation_of_year_to_day_master(element, year["element"])

    decade = _get_current_decade_text(chart, birth_dt, element)

    da = _get_light_da_yun_pillar(chart, birth_dt)
    decade_relation = (
        _get_element_relation(element, STEM_ELEMENT.get(da["stem"], "Unknown"))
        if da.get("stem") else "unknown"
    )

    signals = {
        "day_master": dm,
        "day_master_element": element,
        "day_branch": db,
        "day_branch_element": underlying,
        "year_element": year["element"],
        "year_relation": rel,
        "decade_relation": decade_relation,
    }

    return {
        "day_master": dm,
        "day_master_element": element,
        "day_branch": db,
        "day_branch_element": underlying,

        "current_phase": {
            "title": "What’s Happening In Your Life Right Now",
            "summary": _build_current_phase_summary(personality, phase, underlying_text),
            "details": CURRENT_PHASE_DETAILS.get(element, "The energies at work right now are asking you to pay closer attention to how you move through daily life."),
        },
        "this_year": {
            "title": "What This Year Is Bringing",
            "year": year["year"],
            "summary": YEAR_FEELING.get(rel, "This year is bringing a meaningful shift in pace and priorities."),
            "details": YEAR_DETAILS.get(rel, "This year carries an influence worth paying attention to — how you respond to it matters more than the circumstances themselves."),
            "opportunity": YEAR_OPPORTUNITY.get(rel, "There is still useful momentum here if you respond with awareness."),
            "mindful_of": YEAR_MINDFUL.get(rel, "Be mindful of imbalance and how you use your energy."),
        },
        "current_decade": {
            "title": "Your Current Life Stage",
            "summary": decade["summary"],
            "details": DECADE_DETAILS.get(decade_relation, "This longer phase is developing something real in you, even if it is not fully visible yet."),
            "opportunity": decade["opportunity"],
            "mindful_of": decade["mindful"],
        },
        "cta": {
            "title": "Go Deeper",
            "summary": "This is only the surface of your timing. A full reading can show why these patterns are happening, what is opening next, and how to move through it with more clarity.",
        },
        "signals": signals,
    }
