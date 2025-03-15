from dataclasses import dataclass
import decimal
import enum
import json
import typing
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

    def adjust(
        self, amount: decimal.Decimal, from_year: int, to_year: int
    ) -> decimal.Decimal:
        assert from_year <= to_year
        assert to_year <= self.years[0].year + 1
        assert from_year >= self.years[-1].year
        if from_year == to_year:
            return amount

        for year in self.years:
            if to_year <= year.year:
                continue
            if from_year > year.year:
                break
            amount *= year.achange + 1

        return amount


def load_inflation(
    fname: str = "data/aus_inflation.json",
    measure: InflationMeasure = InflationMeasure.CPI,
) -> Inflation:
    with open(fname, "r") as fh:
        return _load_inflation_from_content(json.load(fh), measure)


def _load_inflation_from_content(
    content: list[typing.Any], measure: InflationMeasure
) -> Inflation:
    assert type(content) == list
    key = "cpi" if measure == InflationMeasure.CPI else "wpi"
    years = [
        InflationYear(
            year=parse.parse_financial_year(r["year"]),
            achange=decimal.Decimal(r[key]),
        )
        for r in content
    ]

    years.sort(key=lambda i: i.year, reverse=True)
    return Inflation(years=years)
