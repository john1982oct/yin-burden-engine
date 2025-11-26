# bazi_core.py
from dataclasses import dataclass
from datetime import datetime

# 10 Heavenly Stems
HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 12 Earthly Branches
EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]


@dataclass
class Pillar:
    stem: str
    branch: str

    def __str__(self):
        return f"{self.stem}{self.branch}"


@dataclass
class BaziChart:
    year: Pillar
    month: Pillar
    day: Pillar
    hour: Pillar
    day_master: str


# ---------------------------
# REAL YEAR PILLAR
# ---------------------------
def compute_year_pillar_basic(dt: datetime) -> Pillar:
    """
    Real BaZi Year Pillar (without Li Chun).
    Formula:
      stem_index = (year - 4) % 10
      branch_index = (year - 4) % 12
    """
    base = dt.year - 4
    stem_index = base % 10
    branch_index = base % 12
    return Pillar(
        stem=HEAVENLY_STEMS[stem_index],
        branch=EARTHLY_BRANCHES[branch_index],
    )


def _stem_branch_from_int(seed: int) -> Pillar:
    stem = HEAVENLY_STEMS[seed % 10]
    branch = EARTHLY_BRANCHES[seed % 12]
    return Pillar(stem, branch)


def compute_placeholder_bazi(dt: datetime) -> BaziChart:
    """
    Uses REAL year pillar now.
    Other pillars remain placeholder until upgraded.
    """
    # REAL BaZi year pillar
    year_pillar = compute_year_pillar_basic(dt)

    # Placeholder logic for other pillars
    month_pillar = _stem_branch_from_int(dt.year * 12 + dt.month)
    day_pillar = _stem_branch_from_int(dt.timetuple().tm_yday)
    hour_pillar = _stem_branch_from_int(dt.hour + dt.timetuple().tm_yday * 24)

    day_master = day_pillar.stem

    return BaziChart(
        year=year_pillar,
        month=month_pillar,
        day=day_pillar,
        hour=hour_pillar,
        day_master=day_master,
    )


def describe_bazi_chart(chart: BaziChart) -> dict:
    return {
        "year": str(chart.year),
        "month": str(chart.month),
        "day": str(chart.day),
        "hour": str(chart.hour),
        "day_master": chart.day_master,
    }
