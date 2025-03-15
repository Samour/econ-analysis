from dataclasses import dataclass
import decimal
import json
import typing
import re


@dataclass(frozen=True)
class TaxBracket:
    start: decimal.Decimal
    end: decimal.Decimal
    # TODO Change these to correct decimal type
    rate: decimal.Decimal


@dataclass(frozen=True)
class TaxTable:
    # This is the year that the financial year starts in
    # IE for FY 2022-23, year = 2022
    year: int
    brackets: list[TaxBracket]


@dataclass(frozen=True)
class MultiYearTaxTable:
    year_tables: list[TaxTable]


def load_tax_tables(fname: str) -> MultiYearTaxTable:
    with open(fname, "r") as fh:
        return _load_tax_tables_from_content(json.load(fh))


def _load_tax_tables_from_content(
    content: list[typing.Any],
) -> MultiYearTaxTable:
    assert type(content) == list
    return MultiYearTaxTable(year_tables=[_load_tax_table(e) for e in content])


def _load_tax_table(content: dict[typing.Any, typing.Any]) -> TaxTable:
    assert type(content) == dict
    year = content["year"]
    assert type(year) == str
    brackets = content["brackets"]
    assert type(brackets) == list
    return TaxTable(
        year=_parse_financial_year(year),
        brackets=[_load_tax_bracket(b) for b in brackets],
    )


def _parse_financial_year(fy: str) -> int:
    if fy == "1999-2000":
        return 1999

    match = re.match("(\\d{4})-(\\d{2})", fy)
    assert match is not None
    year = int(match.group(1))
    assert 2000 + int(match.group(2)) - year == 1

    return year


def _load_tax_bracket(content: dict[typing.Any, typing.Any]) -> TaxBracket:
    assert type(content) == dict
    b_min = content["min"]
    assert type(b_min) == str
    b_max = content["max"]
    assert type(b_max) == str
    b_rate = content["rate"]
    assert type(b_rate) == str

    bracket = TaxBracket(
        start=decimal.Decimal(b_min),
        end=decimal.Decimal(b_max),
        rate=decimal.Decimal(b_rate),
    )
    assert bracket.start < bracket.end
    assert bracket.rate >= 0
    assert bracket.rate <= 1

    return bracket
