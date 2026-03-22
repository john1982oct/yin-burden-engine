# current_phase_engine.py
# Purpose:
# New lead-magnet interpretation engine for:
# "This tool helps you understand what’s happening in your life right now,
# what opportunities are opening up, and what to be mindful of."

from merit_engine import STEM_ELEMENT


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


def generate_current_phase_reading(chart):
    """
    Input:
        chart -> BaziChart from bazi_core.compute_placeholder_bazi()

    Output:
        structured JSON-friendly dict for frontend / API response
    """

    day_master = chart.day_master
    element = STEM_ELEMENT.get(day_master, "Unknown")
    personality = DAY_MASTER_PERSONALITY.get(
        day_master,
        "You have your own unique way of approaching life and challenges."
    )

    current_phase = CURRENT_PHASE_TEXT.get(
        element,
        "You are in a period of transition where deeper self-understanding becomes especially important."
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

    return {
        "tool_role": (
            "This tool helps you understand what’s happening in your life right now, "
            "what opportunities are opening up, and what to be mindful of."
        ),
        "day_master": day_master,
        "day_master_element": element,
        "current_phase": {
            "title": "What’s Happening In Your Life Right Now",
            "summary": f"{personality} {current_phase}"
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
