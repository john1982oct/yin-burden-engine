# bazi_core.py
from dataclasses import dataclass
from datetime import datetime

# 10 Heavenly Stems
HEAVENLY_STEMS = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]

# 12 Earthly Branches
EARTHLY_BRANCHES = ["子", "丑", "寅", "卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥"]


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
# Placeholder logic for Month, Day, Hour pillars
# -------------------------------------------------------------
def _stem_branch_from_int(seed: int) -> Pillar:
    return Pillar(
        HEAVENLY_STEMS[seed % 10],
        EARTHLY_BRANCHES[seed % 12],
    )


def compute_placeholder_bazi(dt: datetime) -> BaziChart:
    # REAL YEAR PILLAR (NOW ACCURATE)
    year_pillar = compute_year_pillar_basic(dt)

    # SAFE placeholder pillars (will upgrade later)
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
