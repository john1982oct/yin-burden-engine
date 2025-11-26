# bazi_core.py
from dataclasses import dataclass
from datetime import datetime

# 10 Heavenly Stems
HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 12 Earthly Branches
EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# Month branches always start from 寅月
MONTH_BRANCH_SEQUENCE = ["寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑"]


# -------------------------------------------------------------
# Li Chun Table (Year → Month, Day)
# Covers 1960–2040 for Aido Engine usage
# -------------------------------------------------------------
LI_CHUN_DATES = {
    1960: (2, 4), 1961: (2, 4), 1962: (2, 4), 1963: (2, 4), 1964: (2, 5),
    1965: (2, 4), 1966: (2, 4), 1967: (2, 4), 1968: (2, 5), 1969: (2, 4),
    1970: (2, 4), 1971: (2, 4), 1972: (2, 5), 1973: (2, 4), 1974: (2, 4),
    1975: (2, 4), 1976: (2, 5), 1977: (2, 4), 1978: (2, 4), 1979: (2, 4),
    1980: (2, 5), 1981: (2, 4), 1982: (2, 4), 1983: (2, 4), 1984: (2, 4),
    1985: (2, 4), 1986: (2, 4), 1987: (2, 4), 1988: (2, 4), 1989: (2, 4),
    1990: (2, 4), 1991: (2, 4), 1992: (2, 4), 1993: (2, 4), 1994: (2, 4),
    1995: (2, 4), 1996: (2, 4), 1997: (2, 4), 1998: (2, 4), 1999: (2, 4),
    2000: (2, 4), 2001: (2, 4), 2002: (2, 4), 2003: (2, 4), 2004: (2, 4),
    2005: (2, 4), 2006: (2, 4), 2007: (2, 4), 2008: (2, 4), 2009: (2, 4),
    2010: (2, 4), 2011: (2, 4), 2012: (2, 4), 2013: (2, 4), 2014: (2, 4),
    2015: (2, 4), 2016: (2, 4), 2017: (2, 3), 2018: (2, 4), 2019: (2, 4),
    2020: (2, 4), 2021: (2, 3), 2022: (2, 4), 2023: (2, 4), 2024: (2, 4),
    2025: (2, 3), 2026: (2, 4), 2027: (2, 4), 2028: (2, 4), 2029: (2, 4),
    2030: (2, 3), 2031: (2, 4), 2032: (2, 4), 2033: (2, 4), 2034: (2, 4),
    2035: (2, 3), 2036: (2, 4), 2037: (2, 4), 2038: (2, 4), 2039: (2, 4),
    2040: (2, 3),
}


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


# -------------------------------------------------------------
# Helper: adjust year by Li Chun
# -------------------------------------------------------------
def adjust_year_for_li_chun(dt: datetime) -> int:
    """
    If birth is before Li Chun of that year → use previous year.
    After Li Chun → use current year.
    """
    y = dt.year

    if y not in LI_CHUN_DATES:
        return y

    m, d = LI_CHUN_DATES[y]
    li_chun_dt = datetime(y, m, d, 0, 0)

    if dt < li_chun_dt:
        return y - 1

    return y


# -------------------------------------------------------------
# REAL BaZi Year Pillar with Li Chun
# -------------------------------------------------------------
def compute_year_pillar_basic(dt: datetime) -> Pillar:
    bazi_year = adjust_year_for_li_chun(dt)

    base = bazi_year - 4
    stem_index = base % 10
    branch_index = base % 12

    return Pillar(
        stem=HEAVENLY_STEMS[stem_index],
        branch=EARTHLY_BRANCHES[branch_index],
    )


# -------------------------------------------------------------
# BaZi Month Index (1–12) based on solar terms (approx rules)
#
# 1  寅月: 2/4  – 3/5
# 2  卯月: 3/6  – 4/4
# 3  辰月: 4/5  – 5/5
# 4  巳月: 5/6  – 6/5
# 5  午月: 6/6  – 7/6
# 6  未月: 7/7  – 8/7
# 7  申月: 8/8  – 9/7
# 8  酉月: 9/8  – 10/7
# 9  戌月: 10/8 – 11/7
# 10 亥月: 11/8 – 12/6
# 11 子月: 12/7 – 1/5
# 12 丑月: 1/6  – 2/3
# -------------------------------------------------------------
def get_bazi_month_index(dt: datetime) -> int:
    m = dt.month
    d = dt.day

    # 寅月
    if (m == 2 and d >= 4) or (m == 3 and d <= 5):
        return 1
    # 卯月
    if (m == 3 and d >= 6) or (m == 4 and d <= 4):
        return 2
    # 辰月
    if (m == 4 and d >= 5) or (m == 5 and d <= 5):
        return 3
    # 巳月
    if (m == 5 and d >= 6) or (m == 6 and d <= 5):
        return 4
    # 午月
    if (m == 6 and d >= 6) or (m == 7 and d <= 6):
        return 5
    # 未月
    if (m == 7 and d >= 7) or (m == 8 and d <= 7):
        return 6
    # 申月
    if (m == 8 and d >= 8) or (m == 9 and d <= 7):
        return 7
    # 酉月
    if (m == 9 and d >= 8) or (m == 10 and d <= 7):
        return 8
    # 戌月
    if (m == 10 and d >= 8) or (m == 11 and d <= 7):
        return 9
    # 亥月
    if (m == 11 and d >= 8) or (m == 12 and d <= 6):
        return 10
    # 子月
    if (m == 12 and d >= 7) or (m == 1 and d <= 5):
        return 11
    # 丑月
    # (m == 1 and d >= 6) or (m == 2 and d <= 3)
    return 12


# -------------------------------------------------------------
# REAL Month Pillar (stem + branch)
#
# Month stem rule:
#   Year stem 甲/己 → 寅月丙, then cycle
#   Year stem 乙/庚 → 寅月戊
#   Year stem 丙/辛 → 寅月庚
#   Year stem 丁/壬 → 寅月壬
#   Year stem 戊/癸 → 寅月甲
# Then add (month_index - 1) to stem index (mod 10).
# -------------------------------------------------------------
def compute_month_pillar(dt: datetime, year_pillar: Pillar) -> Pillar:
    month_index = get_bazi_month_index(dt)  # 1..12
    year_stem = year_pillar.stem

    # 寅月 starting stem based on year stem
    if year_stem in ("甲", "己"):
        start_stem = "丙"
    elif year_stem in ("乙", "庚"):
        start_stem = "戊"
    elif year_stem in ("丙", "辛"):
        start_stem = "庚"
    elif year_stem in ("丁", "壬"):
        start_stem = "壬"
    else:  # 戊, 癸
        start_stem = "甲"

    start_index = HEAVENLY_STEMS.index(start_stem)
    stem_index = (start_index + (month_index - 1)) % 10
    stem = HEAVENLY_STEMS[stem_index]

    branch = MONTH_BRANCH_SEQUENCE[month_index - 1]

    return Pillar(stem=stem, branch=branch)


# -------------------------------------------------------------
# Placeholder logic for Day, Hour pillars
# -------------------------------------------------------------
def _stem_branch_from_int(seed: int) -> Pillar:
    return Pillar(
        HEAVENLY_STEMS[seed % 10],
        EARTHLY_BRANCHES[seed % 12],
    )


def compute_placeholder_bazi(dt: datetime) -> BaziChart:
    # REAL YEAR PILLAR
    year_pillar = compute_year_pillar_basic(dt)

    # REAL MONTH PILLAR (using year stem & solar month)
    month_pillar = compute_month_pillar(dt, year_pillar)

    # SAFE placeholder day/hour pillars (to be improved later)
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
