# current_phase_engine.py
# Purpose:
# New lead-magnet interpretation engine for:
# "This tool helps you understand what’s happening in your life right now,
# what opportunities are opening up, and what to be mindful of."

def generate_current_phase_reading(chart):
    """
    Input:
        chart -> BaziChart from bazi_core.compute_placeholder_bazi()

    Output:
        structured JSON-friendly dict for frontend / API response
    """

    return {
        "tool_role": (
            "This tool helps you understand what’s happening in your life right now, "
            "what opportunities are opening up, and what to be mindful of."
        ),
        "current_phase": {
            "title": "Your Current Phase",
            "summary": "Placeholder: this is where the main current-life insight will go."
        },
        "opportunities": {
            "career_wealth": "Placeholder",
            "relationships": "Placeholder",
            "personal_growth": "Placeholder"
        },
        "mindful_of": {
            "career_wealth": "Placeholder",
            "relationships": "Placeholder",
            "personal_growth": "Placeholder"
        },
        "guidance": {
            "title": "What Helps Most Now",
            "summary": "Placeholder: this is where practical advice will go."
        },
        "cta": {
            "title": "Go Deeper",
            "summary": (
                "This is a surface-level reading. Your full chart can reveal why this phase is "
                "happening and how to navigate it more clearly."
            )
        }
    }
