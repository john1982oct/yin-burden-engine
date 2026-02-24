# elemental_blueprint_engine.py
# Purpose: Generate "Primary Constitution" + "Underlying Restoration Layer"
# using Day Stem (Day Master) + Day Branch element mapping.
#
# Tone: modern wellness + luxury (not mystical, not medical).

from merit_engine import STEM_ELEMENT, BRANCH_ELEMENT


# ----------------------------------------
# Element Display (English + Chinese)
# ----------------------------------------

ELEMENT_DISPLAY = {
    "Wood":  {"en": "Wood",  "zh": "木"},
    "Fire":  {"en": "Fire",  "zh": "火"},
    "Earth": {"en": "Earth", "zh": "土"},
    "Metal": {"en": "Metal", "zh": "金"},
    "Water": {"en": "Water", "zh": "水"},
}


# ----------------------------------------
# Visual Layer (for frontend rendering)
# ----------------------------------------

ELEMENT_VISUAL = {
    "Wood":  {"key": "wood",  "emoji": "🌿"},
    "Fire":  {"key": "fire",  "emoji": "🔥"},
    "Earth": {"key": "earth", "emoji": "🜃"},
    "Metal": {"key": "metal", "emoji": "⚙️"},
    "Water": {"key": "water", "emoji": "💧"},
}


# ----------------------------------------
# Primary Constitution Text
# ----------------------------------------

PRIMARY_CONST_TEXT = {
    "Wood": (
        "Your system expresses through movement, renewal and forward momentum. "
        "When balanced, you recover best with smooth flow and gentle expansion."
    ),
    "Fire": (
        "Your system expresses through warmth, visibility and circulatory rhythm. "
        "When balanced, your radiance comes easily — but overstimulation can drain you quickly."
    ),
    "Earth": (
        "Your system expresses through stability, nourishment and grounded presence. "
        "When balanced, your beauty shows as steadiness, fullness and calm resilience."
    ),
    "Metal": (
        "Your system expresses through structure, refinement and boundary awareness. "
        "When balanced, you look clear, composed and quietly luminous."
    ),
    "Water": (
        "Your system expresses through depth, sensitivity and restorative rhythm. "
        "When balanced, you feel calm, steady and deeply replenished."
    ),
}


# ----------------------------------------
# Underlying Restoration Layer Text
# ----------------------------------------

UNDERLYING_LAYER_TEXT = {
    "Wood": (
        "Your deeper recovery improves when internal rhythm stays smooth — "
        "tension release and gentle movement matter more than pushing harder."
    ),
    "Fire": (
        "Your deeper recovery depends on warmth regulation — "
        "protecting your sleep rhythm and reducing overstimulation restores glow."
    ),
    "Earth": (
        "Your deeper recovery depends on steady nourishment — "
        "when your center feels supported, energy and appearance stabilise."
    ),
    "Metal": (
        "Your deeper recovery depends on barrier rhythm and breath regulation — "
        "consistency supports a refined, clear and resilient look."
    ),
    "Water": (
        "Your deeper recovery depends on deep rest and replenishment cycles — "
        "slow recovery is not weakness; it’s your power source."
    ),
}


# ----------------------------------------
# Disclaimer
# ----------------------------------------

DISCLAIMER = (
    "Disclaimer: This result is a wellness-oriented interpretation inspired by elemental philosophy. "
    "It is not medical advice and is not intended to diagnose, treat, cure, or prevent any condition. "
    "For medical concerns, consult a qualified healthcare professional."
)


# ----------------------------------------
# Internal Helpers
# ----------------------------------------

def _display(element):
    if not element:
        return None
    return ELEMENT_DISPLAY.get(element, {"en": element, "zh": ""})


def _visual(element):
    if not element:
        return None
    return ELEMENT_VISUAL.get(element)


# ----------------------------------------
# Main Blueprint Generator
# ----------------------------------------

def generate_elemental_blueprint(chart):
    """
    Input: chart (from compute_placeholder_bazi)
    Output: structured blueprint JSON for frontend rendering
    """

    primary = STEM_ELEMENT.get(chart.day_master)
    underlying = BRANCH_ELEMENT.get(chart.day.branch)

    return {
        "signature": f"{primary}-{underlying}" if primary and underlying else None,

        "primary_constitution": _display(primary),
        "underlying_restoration_layer": _display(underlying),

        "visual": {
            "primary": _visual(primary),
            "underlying": _visual(underlying),
        },

        "primary_text": PRIMARY_CONST_TEXT.get(primary),
        "underlying_text": UNDERLYING_LAYER_TEXT.get(underlying),

        "disclaimer": DISCLAIMER,
    }
