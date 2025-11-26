# bazi_core.py
"""
Very simple, SAFE BaZi scaffold for Aido Yin Burden Engine.

NOTE:
- This is NOT accurate BaZi yet.
- It only gives a stable "4 pillars" structure so that
  /bazi-debug can work without errors.
- Later we will upgrade each part step by step.
"""

from dataclasses import dataclass
from datetime import datetime


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
    Basic BaZi chart container (placeholder).
    """
    year: Pillar
    month: Pillar
    day: Pillar
    hour: Pillar
    day_master: str  # e.g. "戊"


# -------------------------------------------------------------
# REAL YEAR PILLAR (no Li Chun yet)
# -------------------------------------------------------------
def compute_year_pillar_basic(dt: datetime) -> Pillar:
    """
    Basic, *real* BaZi year pillar from Gregorian year.

    Formula (without Li Chun adjustment):
      - Stem index = (year - 4) % 10
      - Branch index = (year - 4) % 12

    Example:
      1984 -> 甲子
      1982 -> 壬戌
    """
    base = dt.year - 4
    stem_index = base % len(HEAVENLY_STEMS)
    branch_index = base % len(EARTHLY_BRANCHES)
    return Pillar(
        stem=HEAVENLY_STEMS[stem_index],
        branch=EARTHLY_BRANCHES[branch_index],
    )


def _stem_branch_from_int(seed: int) -> Pillar:
    """Safe helper: any integer -> one pillar, by modulo."""
    stem = HEAVENLY_STEMS[seed % len(HEAVENLY_STEMS)]
    branch = EARTHLY_BRANCHES[seed % len(EARTHLY_BRANCHES)]
    return Pillar(stem=stem, branch=branch)


def compute_placeholder_bazi(dt: datetime) -> BaziChart:
    """
    SAFE placeholder BaZi:

    - Uses REAL year pillar formula
    - Other pillars still deterministic placeholders.
    """
    # REAL year pillar
    year_pillar = compute_year_pillar_basic(dt)

    # Placeholder month pillar
    month_seed = (dt.year * 12 + dt.month)
    month_pillar = _stem_branch_from_int(month_seed)

    # Placeholder day pillar
    day_seed = dt.timetuple().tm_yday
    day_pillar = _stem_branch_from_int(day_seed)

    # Placeholder hour pillar
    hour_seed = dt.hour + day_seed * 24
    hour_pillar = _stem_branch_from_int(hour_seed)

    day_master = day_pillar.stem

    return BaziChart(
        year=year_pillar,
        month=month_pillar,
        day=day_pillar,
        hour=hour_pillar,
        day_master=day_master,
    )


def describe_bazi_chart(chart: BaziChart) -> dict:
    """Convert chart to JSON dict."""
    return {
        "year": str(chart.year),
        "month": str(chart.month),
        "day": str(chart.day),
        "hour": str(chart.hour),
        "day_master": chart.day_master,
    }
