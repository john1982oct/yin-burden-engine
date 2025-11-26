# bazi_core.py
"""
Core BaZi structures for Aido Yin Burden Engine.

IMPORTANT:
- This is a FIRST STEP scaffold.
- The pillar calculation is still a placeholder and NOT yet used
  by the main merit engine.
- Later we will replace the placeholder logic with a proper
  BaZi algorithm (year/month/day/hour pillars, solar terms, etc.).
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


# 10 Heavenly Stems (天干)
HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 12 Earthly Branches (地支)
EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]


@dataclass
class Pillar:
    """One BaZi pillar = Stem + Branch, e.g. 戊午."""
    stem: str
    branch: str

    def __str__(self) -> str:
        return f"{self.stem}{self.branch}"


@dataclass
class BaziChart:
    """
    Basic BaZi chart container.

    For now we keep it simple:
    - 4 main pillars
    - Day master convenience field
    Later we can add:
    - hidden stems
    - luck pillars
    - ten-god mapping, etc.
    """
    year: Pillar
    month: Pillar
    day: Pillar
    hour: Pillar
    day_master: str  # e.g. "戊"


def _ganzhi_from_index(index: int) -> Pillar:
    """
    Convert 0–59 index to a stem-branch pair.
    Index 0 corresponds to 甲子.
    """
    stem = HEAVENLY_STEMS[index % 10]
    branch = EARTHLY_BRANCHES[index % 12]
    return Pillar(stem=stem, branch=branch)


def compute_year_pillar_approx(dt: datetime) -> Pillar:
    """
    APPROXIMATE year pillar from Gregorian year.
    Uses the common formula:
        ganzhi_index = (year - 4) % 60
    NOTE:
    - This ignores the Li Chun (立春) solar-term boundary.
    - Later we will refine to use the solar calendar properly.
    """
    index = (dt.year - 4) % 60
    return _ganzhi_from_index(index)


def compute_placeholder_bazi(dt: datetime) -> BaziChart:
    """
    TEMPORARY helper to return a simple, approximate BaZi chart.

    Right now:
    - Year pillar: approximate calculation (no Li Chun adjustment).
    - Month/Day/Hour pillars: simple placeholder guesses based
      on the datetime; NOT accurate BaZi.
    - This function is NOT yet used in the main engine. It exists
      so we can start wiring and testing structures.

    Later we will replace this with a proper BaZi implementation.
    """
    year_pillar = compute_year_pillar_approx(dt)

    # --- PLACEHOLDER logic for month/day/hour pillars ---
    # These are only dummies for structure, not real BaZi maths.
    # We will fully replace them in the next steps.

    # Fake month index 0–11
    month_index = (dt.month - 1) % 12
    # Tie month stem loosely to year stem for now
    month_stem_index = (HEAVENLY_STEMS.index(year_pillar.stem) * 2 + month_index) % 10
    month_pillar = Pillar(
        stem=HEAVENLY_STEMS[month_stem_index],
        branch=EARTHLY_BRANCHES[month_index],
    )

    # Fake day pillar from ordinal day of year
    day_of_year = dt.timetuple().tm_yday  # 1..366
    day_index = (day_of_year + 20) % 60
    day_pillar = _ganzhi_from_index(day_index)

    # Fake hour pillar from hour 0–23
    hour_branch_index = (dt.hour + 1) // 2 % 12  # every 2 hours = one branch
    hour_stem_index = (HEAVENLY_STEMS.index(day_pillar.stem) * 2 + hour_branch_index) % 10
    hour_pillar = Pillar(
        stem=HEAVENLY_STEMS[hour_stem_index],
        branch=EARTHLY_BRANCHES[hour_branch_index],
    )

    day_master = day_pillar.stem

    return BaziChart(
        year=year_pillar,
        month=month_pillar,
        day=day_pillar,
        hour=hour_pillar,
        day_master=day_master,
    )


def describe_bazi_chart(chart: BaziChart) -> dict:
    """
    Convenience helper: turn a BaziChart into a simple dict
    that we can JSON-serialize for debugging or logging.
    """
    return {
        "year": str(chart.year),
        "month": str(chart.month),
        "day": str(chart.day),
        "hour": str(chart.hour),
        "day_master": chart.day_master,
    }
