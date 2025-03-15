from dataclasses import dataclass


@dataclass(frozen=True)
class TaxBracket:
    start: int
    end: int
    # TODO Change these to correct decimal type
    rate: float


@dataclass(frozen=True)
class TaxTable:
    year: int
    brackets: list[TaxBracket]


@dataclass(frozen=True)
class MultiYearTaxTable:
    year_tables: list[TaxTable]


def load_tax_tables(fname: str) -> MultiYearTaxTable:
    pass
