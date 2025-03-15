from dataclasses import dataclass
import decimal
import json
import typing
import re


@dataclass(frozen=True)
class TaxBracket:
    start: decimal.Decimal
    end: typing.Optional[decimal.Decimal]
    rate: decimal.Decimal

    def compute_tax(self, amount: decimal.Decimal) -> decimal.Decimal:
        if amount < self.start:
            return decimal.Decimal(0)
        if self.end is not None and amount > self.end:
            amount = self.end
        return (amount - self.start + 1) * self.rate


@dataclass(frozen=True)
class TaxTable:
    # This is the year that the financial year starts in
    # IE for FY 2022-23, year = 2022
    year: int
    brackets: list[TaxBracket]

    def calculate_tax(self, taxable_income: decimal.Decimal) -> decimal.Decimal:
        tax_amount = decimal.Decimal(0)
        for bracket in self.brackets:
            if bracket.start > taxable_income:
                break
            tax_amount += bracket.compute_tax(taxable_income)

        return tax_amount


@dataclass(frozen=True)
class MultiYearTaxTable:
    year_tables: list[TaxTable]


def load_tax_tables(fname: str = "data/aus_tax_table.json") -> MultiYearTaxTable:
    with open(fname, "r") as fh:
        return _load_tax_tables_from_content(json.load(fh))


def _load_tax_tables_from_content(
    content: list[typing.Any],
) -> MultiYearTaxTable:
    assert type(content) == list
    return MultiYearTaxTable(year_tables=[_load_tax_table(e) for e in content])


def _load_tax_table(content: dict[typing.Any, typing.Any]) -> TaxTable:
    assert type(content) == dict
    fy = content["year"]
    assert type(fy) == str
    brackets_data = content["brackets"]
    assert type(brackets_data) == list

    year = _parse_financial_year(fy)
    brackets: list[TaxBracket] = []
    for b in brackets_data:
        bracket = _load_tax_bracket(b, fy=fy)
        if len(brackets) > 0:
            assert brackets[-1].end is not None
            assert (
                bracket.start == brackets[-1].end + 1
            ), f"Non contiguous tax bracket in fy {fy}: {bracket.start}"
        else:
            assert bracket.start == 0
        brackets.append(bracket)
    assert len(brackets) > 0
    assert brackets[-1].end is None

    return TaxTable(
        year=year,
        brackets=brackets,
    )


def _parse_financial_year(fy: str) -> int:
    if fy == "1999-2000":
        return 1999

    match = re.match("(\\d{4})-(\\d{2})", fy)
    assert match is not None
    year = int(match.group(1))
    assert 2000 + int(match.group(2)) - year == 1, f"Invalid financial year: {fy}"

    return year


def _load_tax_bracket(content: dict[typing.Any, typing.Any], fy: str) -> TaxBracket:
    assert type(content) == dict
    b_min = content["min"]
    assert type(b_min) == str
    b_max = content["max"]
    assert b_max is None or type(b_max) == str
    b_rate = content["rate"]
    assert type(b_rate) == str

    bracket = TaxBracket(
        start=decimal.Decimal(b_min),
        end=decimal.Decimal(b_max) if b_max is not None else None,
        rate=decimal.Decimal(b_rate),
    )
    assert (
        bracket.end is None or bracket.start < bracket.end
    ), f"Invalid tax bracket range in {fy}: {bracket.start} to {bracket.end}"
    assert bracket.rate >= 0
    assert bracket.rate <= 1

    return bracket
