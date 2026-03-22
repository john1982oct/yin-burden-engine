# current_phase_engine.py
# Purpose:
# New lead-magnet interpretation engine for:
# "This tool helps you understand what’s happening in your life right now,
# what opportunities are opening up, and what to be mindful of."

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
    "Wood": (
        "You are in a phase where growth, change and forward movement feel especially important. "
        "Even if life feels uneven at times, you are being pushed to develop clarity, direction and stronger personal momentum."
    ),
    "Fire": (
        "You are in a phase where visibility, expression and emotional energy are more active. "
        "This can bring inspiration and connection, but it also asks you to manage your energy wisely."
    ),
    "Earth": (
        "You are in a phase where stability, responsibility and long-term foundations matter more. "
        "Life may be asking you to slow down, organise what matters, and build something more lasting."
    ),
    "Metal": (
        "You are in a phase where structure, standards and important decisions become more noticeable. "
        "This is a period for refining your path, cutting away distractions and becoming clearer about what truly fits you."
    ),
    "Water": (
        "You are in a phase where reflection, intuition and inner adjustment are especially important. "
        "Even if things feel uncertain on the surface, this period is helping you sense what needs healing, restoring or rethinking."
    ),
}


UNDERLYING_RHYTHM_TEXT = {
    "Wood": (
        "Underneath all this, your deeper rhythm needs movement, renewal and emotional flexibility. "
        "When life feels too blocked or repetitive, you may feel the pressure more strongly."
    ),
    "Fire": (
        "Underneath all this, your deeper rhythm responds strongly to warmth, encouragement and healthy emotional expression. "
        "When your inner spark is suppressed for too long, your energy can feel unsettled."
    ),
    "Earth": (
        "Underneath all this, your deeper rhythm seeks steadiness, emotional safety and something solid to rely on. "
        "When life becomes too uncertain or scattered, you may feel more drained than you show."
    ),
    "Metal": (
        "Underneath all this, your deeper rhythm values order, breathing space and a sense of internal clarity. "
        "When too much feels messy or unresolved, it can quietly weigh on you."
    ),
    "Water": (
        "Underneath all this, your deeper rhythm needs rest, reflection and time to process what is not visible on the surface. "
        "Even when you look composed, deeper emotional tides may still be moving inside."
    ),
}


OPPORTUNITIES_TEXT = {
    "Wood": {
        "career_wealth": (
            "Opportunities may open through initiative, learning, new plans or stepping into a more active role."
        ),
        "relationships": (
            "You may attract people who support your growth, especially when you communicate more honestly and directly."
        ),
        "personal_growth": (
            "This is a strong time to rebuild confidence, create momentum and trust yourself more."
        ),
    },
    "Fire": {
        "career_wealth": (
            "Opportunities may come through visibility, networking, presentation, sales, teaching or creative expression."
        ),
        "relationships": (
            "Warmth and attraction can increase when you allow yourself to be seen more naturally."
        ),
        "personal_growth": (
            "This is a strong time to reconnect with joy, confidence and the parts of yourself that want expression."
        ),
    },
    "Earth": {
        "career_wealth": (
            "Opportunities may build through consistency, practical planning, reliable work and stronger financial discipline."
        ),
        "relationships": (
            "You may strengthen trust with people who value steadiness, emotional safety and long-term sincerity."
        ),
        "personal_growth": (
            "This is a strong time to build healthier routines, stronger boundaries and a more grounded lifestyle."
        ),
    },
    "Metal": {
        "career_wealth": (
            "Opportunities may come through better structure, sharper decision-making, leadership, compliance or specialist skills."
        ),
        "relationships": (
            "Clearer standards can help you attract relationships that feel more respectful and aligned."
        ),
        "personal_growth": (
            "This is a strong time to define what matters, simplify distractions and become more decisive."
        ),
    },
    "Water": {
        "career_wealth": (
            "Opportunities may open through insight, planning, strategy, communication, advisory work or behind-the-scenes influence."
        ),
        "relationships": (
            "You may deepen important bonds through listening, sensitivity and emotional understanding."
        ),
        "personal_growth": (
            "This is a strong time for inner clarity, emotional healing and reconnecting with your deeper instincts."
        ),
    },
}


MINDFUL_TEXT = {
    "Wood": {
        "career_wealth": (
            "Be mindful of rushing, forcing progress too quickly, or getting frustrated when results take time."
        ),
        "relationships": (
            "Strong opinions or impatience may create unnecessary tension if not handled gently."
        ),
        "personal_growth": (
            "Growth is important now, but avoid tying your worth too closely to constant progress."
        ),
    },
    "Fire": {
        "career_wealth": (
            "Be mindful of overexposure, overpromising or making decisions based on excitement alone."
        ),
        "relationships": (
            "Emotions can run hot during this phase, so avoid reacting too quickly in sensitive moments."
        ),
        "personal_growth": (
            "Your energy may come in waves, so protect yourself from burnout and overstimulation."
        ),
    },
    "Earth": {
        "career_wealth": (
            "Be mindful of carrying too much responsibility or becoming overly cautious with change."
        ),
        "relationships": (
            "Supporting others is valuable, but do not lose your own needs in the process."
        ),
        "personal_growth": (
            "Stability is helpful, but avoid getting stuck in routines that no longer support you."
        ),
    },
    "Metal": {
        "career_wealth": (
            "Be mindful of becoming too rigid, overcritical or trapped in perfectionism."
        ),
        "relationships": (
            "High standards are useful, but emotional distance can grow if you become too guarded."
        ),
        "personal_growth": (
            "Discernment is a strength, but leave room for flexibility and softness too."
        ),
    },
    "Water": {
        "career_wealth": (
            "Be mindful of hesitation, overthinking or staying too long in observation mode."
        ),
        "relationships": (
            "Emotional depth is powerful, but unspoken feelings may create confusion if left buried."
        ),
        "personal_growth": (
            "Rest and reflection matter, but do not disappear too deeply into self-doubt or withdrawal."
        ),
    },
}


GUIDANCE_TEXT = {
    "Wood": (
        "What helps most now is steady movement. Focus on clear direction, simple action and healthy patience."
    ),
    "Fire": (
        "What helps most now is balanced expression. Let yourself shine, but protect your energy and pace yourself."
    ),
    "Earth": (
        "What helps most now is strong grounding. Build slowly, stay practical and create support that lasts."
    ),
    "Metal": (
        "What helps most now is clean structure. Simplify, prioritise and trust the power of clear decisions."
    ),
    "Water": (
        "What helps most now is inner alignment. Listen carefully, restore your energy and move when your clarity becomes stronger."
    ),
}


ELEMENT_RELATION = {
    "Wood": {
        "same": "This year tends to amplify your natural style and pushes your growth themes more strongly.",
        "produces": "This year can strengthen your confidence and help supportive conditions form around you.",
        "controls": "This year may bring pressure, demands or situations that force you to sharpen yourself.",
        "drains": "This year may pull more energy out of you through output, responsibilities or constant action.",
        "controlled_by": "This year may bring practical concerns, expectations or reality checks that test your balance.",
    },
    "Fire": {
        "same": "This year tends to intensify your natural energy, expression and emotional activity.",
        "produces": "This year can strengthen your confidence and make it easier to feel supported or seen.",
        "controls": "This year may bring pressure through responsibility, discipline or external expectations.",
        "drains": "This year may ask you to give more, perform more or spread your energy widely.",
        "controlled_by": "This year may bring practical or emotional realities that force you to slow down and stabilise.",
    },
    "Earth": {
        "same": "This year tends to reinforce themes of responsibility, stability and carrying important foundations.",
        "produces": "This year can strengthen your sense of support, confidence and internal steadiness.",
        "controls": "This year may bring pressure through structure, deadlines or situations that require stronger discipline.",
        "drains": "This year may pull your energy into caregiving, management or practical commitments.",
        "controlled_by": "This year may challenge you through change, growth pressure or the need to stay flexible.",
    },
    "Metal": {
        "same": "This year tends to intensify your natural standards, decision-making and need for clarity.",
        "produces": "This year can strengthen your confidence, support and ability to hold your ground.",
        "controls": "This year may bring pressure through responsibility, visibility or situations that require stronger performance.",
        "drains": "This year may pull your energy into communication, output or constantly responding to demands.",
        "controlled_by": "This year may challenge you through softer emotional or practical concerns that are harder to force into order.",
    },
    "Water": {
        "same": "This year tends to amplify your natural sensitivity, reflection and intuitive processing.",
        "produces": "This year can strengthen your resilience, support and deeper emotional understanding.",
        "controls": "This year may bring pressure through busyness, expectations or situations that demand clearer action.",
        "drains": "This year may pull your energy into planning, thinking, advising or emotional processing for others.",
        "controlled_by": "This year may test you through structure, deadlines or firmer conditions that reduce your freedom to drift.",
    },
}


YEAR_OPPORTUNITY_TEXT = {
    "same": "There can be stronger momentum when you work with your natural strengths instead of fighting yourself.",
    "produces": "Supportive people, resources or timing may feel easier to access this year.",
    "controls": "Pressure can become productive if you turn it into focus, skill and better decision-making.",
    "drains": "This year can open opportunities through visibility, contribution and sharing what you know.",
    "controlled_by": "Practical situations may push you to become sharper, more grounded and more realistic in useful ways.",
}


YEAR_MINDFUL_TEXT = {
    "same": "Be mindful of overdoing familiar habits, because too much of your own style can become imbalance.",
    "produces": "Be mindful of becoming too comfortable and missing the need for timely action.",
    "controls": "Be mindful of stress, tension or reacting too defensively under pressure.",
    "drains": "Be mindful of burnout, over-giving or scattering your energy across too many directions.",
    "controlled_by": "Be mindful of feeling boxed in by practical reality or becoming discouraged too quickly.",
}


def _relation_of_year_to_day_master(dm_element: str, year_element: str) -> str:
    # same element
    if dm_element == year_element:
        return "same"

    # produces DM
    produces_map = {
        "Wood": "Water",
        "Fire": "Wood",
        "Earth": "Fire",
        "Metal": "Earth",
        "Water": "Metal",
    }
    if produces_map[dm_element] == year_element:
        return "produces"

    # DM controls year
    controls_map = {
        "Wood": "Earth",
        "Fire": "Metal",
        "Earth": "Water",
        "Metal": "Wood",
        "Water": "Fire",
    }
    if controls_map[dm_element] == year_element:
        return "drains"

    # year controls DM
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
    year_stem = year_pillar.stem
    year_branch = year_pillar.branch
    year_element = STEM_ELEMENT.get(year_stem, "Unknown")

    return {
        "pillar": f"{year_stem}{year_branch}",
        "stem": year_stem,
        "branch": year_branch,
        "element": year_element,
        "gregorian_year": now.year,
    }


def generate_current_phase_reading(chart):
    """
    Input:
        chart -> BaziChart from bazi_core.compute_placeholder_bazi()

    Output:
        structured JSON-friendly dict for frontend / API response
    """

    day_master = chart.day_master
    day_branch = chart.day.branch

    element = STEM_ELEMENT.get(day_master, "Unknown")
    underlying_element = BRANCH_ELEMENT.get(day_branch, "Unknown")

    personality = DAY_MASTER_PERSONALITY.get(
        day_master,
        "You have your own unique way of approaching life and challenges."
    )

    current_phase = CURRENT_PHASE_TEXT.get(
        element,
        "You are in a period of transition where deeper self-understanding becomes especially important."
    )

    underlying_rhythm = UNDERLYING_RHYTHM_TEXT.get(
        underlying_element,
        "At a deeper level, your inner rhythm may be asking for more awareness, steadiness and self-understanding."
    )

    opportunities = OPPORTUNITIES_TEXT.get(
        element,
        {
            "career_wealth": "Opportunities may be developing in practical but subtle ways.",
            "relationships": "Relationships may improve through greater awareness and communication.",
            "personal_growth": "This is a period for personal reflection and steady growth.",
        }
    )

    mindful_of = MINDFUL_TEXT.get(
        element,
        {
            "career_wealth": "Be mindful of acting too quickly or losing focus.",
            "relationships": "Be mindful of misunderstandings caused by unspoken expectations.",
            "personal_growth": "Be mindful of habits that drain your confidence or clarity.",
        }
    )

    guidance = GUIDANCE_TEXT.get(
        element,
        "What helps most now is moving with awareness, patience and consistency."
    )

    current_year = _current_year_info()
    year_element = current_year["element"]
    relation = _relation_of_year_to_day_master(element, year_element)

    year_base = ELEMENT_RELATION.get(element, {}).get(
        relation,
        "This year is bringing a mix of activity, learning and adjustment."
    )
    year_opportunity = YEAR_OPPORTUNITY_TEXT.get(
        relation,
        "This year may still open doors through awareness and steady action."
    )
    year_mindful = YEAR_MINDFUL_TEXT.get(
        relation,
        "Be mindful of imbalance and keep your energy well-managed."
    )

    return {
        "tool_role": (
            "This tool helps you understand what’s happening in your life right now, "
            "what opportunities are opening up, and what to be mindful of."
        ),
        "day_master": day_master,
        "day_master_element": element,
        "day_branch": day_branch,
        "day_branch_element": underlying_element,
        "current_phase": {
            "title": "What’s Happening In Your Life Right Now",
            "summary": f"{personality} {current_phase} {underlying_rhythm}"
        },
        "this_year": {
            "title": "What This Year Is Bringing",
            "gregorian_year": current_year["gregorian_year"],
            "year_pillar": current_year["pillar"],
            "year_element": year_element,
            "summary": year_base,
            "opportunity": year_opportunity,
            "mindful_of": year_mindful,
        },
        "opportunities": {
            "title": "Opportunities Opening Up",
            "career_wealth": opportunities["career_wealth"],
            "relationships": opportunities["relationships"],
            "personal_growth": opportunities["personal_growth"]
        },
        "mindful_of": {
            "title": "What To Be Mindful Of",
            "career_wealth": mindful_of["career_wealth"],
            "relationships": mindful_of["relationships"],
            "personal_growth": mindful_of["personal_growth"]
        },
        "guidance": {
            "title": "What Helps Most Now",
            "summary": guidance
        },
        "cta": {
            "title": "Go Deeper",
            "summary": (
                "This is a surface-level reading. A full chart reading can reveal why this phase feels this way, "
                "which areas are becoming more active, and how to navigate the timing more clearly."
            )
        }
    }
