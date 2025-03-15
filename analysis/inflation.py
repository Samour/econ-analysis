from dataclasses import dataclass
import decimal
import enum
import json
from analysis import parse


class InflationMeasure(enum.Enum):
    CPI = "CPI"
    WPI = "WPI"


@dataclass(frozen=True)
class InflationYear:
    year: int
    achange: decimal.Decimal


@dataclass(frozen=True)
class Inflation:
    years: list[InflationYear]


def load_inflation(
    fname: str = "data/aus_inflation.json",
    measure: InflationMeasure = InflationMeasure.CPI,
) -> Inflation:
    key = "cpi" if measure == InflationMeasure.CPI else "wpi"
    with open(fname, "r") as fh:
        content = json.load(fh)
        assert type(content) == list
        years = [
            InflationYear(
                year=parse.parse_financial_year(r["year"]),
                achange=decimal.Decimal(r[key]),
            )
            for r in content
        ]

    years.sort(key=lambda i: i.year, reverse=True)
    return Inflation(years=years)
