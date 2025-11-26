# bazi_core.py
from dataclasses import dataclass
from datetime import datetime, date

# 10 Heavenly Stems
HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 12 Earthly Branches
EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]

# Month branches always start from 寅月
MONTH_BRANCH_SEQUENCE = ["寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑"]

# Hour branches from 子时 to 亥时
HOUR_BRANCH_SEQUENCE = ["子", "丑", "寅", "卯", "辰", "巳",
                        "午", "未", "申", "酉", "戌", "亥"]


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
# Helper: adjust BaZi year by Li Chun
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
def compute_year_pillar(dt: datetime) -> Pillar:
    bazi_year = adjust_year_for_li_chun(dt)

    base = bazi_year - 4
    stem_index = base % 10
    branch_index = base % 12

    return Pillar(
        stem=HEAVENLY_STEMS[stem_index],
        branch=EARTHLY_BRANCHES[branch_index],
    )


# -------------------------------------------------------------
# BaZi Month Index (1–12) based on approximate solar terms
# (good enough for 1960–2040 range)
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
# REAL Month Pillar
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
# REAL Day Pillar using 60 JiaZi cycle
#
# Reference: 1984-02-02 (Gregorian) is treated as 甲子日.
# -------------------------------------------------------------
JIA_ZI_REF_DATE = date(1984, 2, 2)  # assumed 甲子日


def compute_day_pillar(dt: datetime) -> Pillar:
    # Work with date only (local)
    current_date = dt.date()
    delta_days = (current_date - JIA_ZI_REF_DATE).days

    # Normalize to positive cycle index 0..59
    index = delta_days % 60

    stem_index = index % 10
    branch_index = index % 12

    stem = HEAVENLY_STEMS[stem_index]
    branch = EARTHLY_BRANCHES[branch_index]

    return Pillar(stem=stem, branch=branch)


# -------------------------------------------------------------
# Helper: hour branch index (0..11) from clock time
# 子: 23:00–00:59, 丑: 01:00–02:59, ... , 亥: 21:00–22:59
# -------------------------------------------------------------
def get_hour_branch_index(hour: int, minute: int) -> int:
    # normalize 24:xx if ever
    h = hour % 24

    if h == 23 or h == 0:
        return 0  # 子
    if 1 <= h <= 2:
        return 1  # 丑
    if 3 <= h <= 4:
        return 2  # 寅
    if 5 <= h <= 6:
        return 3  # 卯
    if 7 <= h <= 8:
        return 4  # 辰
    if 9 <= h <= 10:
        return 5  # 巳
    if 11 <= h <= 12:
        return 6  # 午
    if 13 <= h <= 14:
        return 7  # 未
    if 15 <= h <= 16:
        return 8  # 申
    if 17 <= h <= 18:
        return 9  # 酉
    if 19 <= h <= 20:
        return 10  # 戌
    # 21–22
    return 11  # 亥


# -------------------------------------------------------------
# REAL Hour Pillar
#
# Formula:
#   hour_branch_index = 0..11 (子..亥)
#   day_stem_index = index of day stem in HEAVENLY_STEMS
#   hour_stem_index = (2 * day_stem_index + hour_branch_index) % 10
#
# This reproduces the classic groups:
#   甲/己日 → 子时甲
#   乙/庚日 → 子时丙
#   丙/辛日 → 子时戊
#   丁/壬日 → 子时庚
#   戊/癸日 → 子时壬
# and cycles naturally for all 12 hours.
# -------------------------------------------------------------
def compute_hour_pillar(dt: datetime, day_pillar: Pillar) -> Pillar:
    hour = dt.hour
    minute = dt.minute

    hb_index = get_hour_branch_index(hour, minute)
    branch = HOUR_BRANCH_SEQUENCE[hb_index]

    day_stem_index = HEAVENLY_STEMS.index(day_pillar.stem)
    stem_index = (2 * day_stem_index + hb_index) % 10
    stem = HEAVENLY_STEMS[stem_index]

    return Pillar(stem=stem, branch=branch)


# -------------------------------------------------------------
# Main entry: compute full BaZi chart
# -------------------------------------------------------------
def compute_bazi_chart(dt: datetime) -> BaziChart:
    year_pillar = compute_year_pillar(dt)
    month_pillar = compute_month_pillar(dt, year_pillar)
    day_pillar = compute_day_pillar(dt)
    hour_pillar = compute_hour_pillar(dt, day_pillar)

    day_master = day_pillar.stem

    return BaziChart(
        year=year_pillar,
        month=month_pillar,
        day=day_pillar,
        hour=hour_pillar,
        day_master=day_master,
    )


# Backwards-compatible name for existing code
def compute_placeholder_bazi(dt: datetime) -> BaziChart:
    return compute_bazi_chart(dt)


def describe_bazi_chart(chart: BaziChart) -> dict:
    return {
        "year": str(chart.year),
        "month": str(chart.month),
        "day": str(chart.day),
        "hour": str(chart.hour),
        "day_master": chart.day_master,
    }
