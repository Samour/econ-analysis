import decimal
import matplotlib.pyplot as plt
import pandas as pd
import typing
from analysis import inflation, labels, tax


def _show_tax_paid(
    income: int, inflation_adjusted: typing.Optional[inflation.InflationMeasure] = None
) -> None:
    d_income = decimal.Decimal(income)
    tax_tables = tax.load_tax_tables()
    inflation_adjustment: typing.Callable[[int, decimal.Decimal], decimal.Decimal] = (
        lambda _, x: x
    )

    if inflation_adjusted is not None:
        inflate = inflation.load_inflation(measure=inflation_adjusted)
        tax_tables = tax_tables.adjusted_for_inflation(inflate)
        to_year = max(t.year for t in tax_tables.year_tables)
        # inflation_adjustment = lambda y, x: inflate.adjust(
        # amount=x, from_year=y, to_year=to_year
        # )

    fy_index = []
    rows = []
    for year in reversed(tax_tables.year_tables):
        fy_index.append(labels.financial_year(year.year))
        adjusted_income = inflation_adjustment(year.year, d_income)
        tax_amount = year.calculate_tax(adjusted_income)
        rows.append(
            {
                "income": int(adjusted_income),
                "tax": int(tax_amount),
                "etr": float(tax_amount / adjusted_income * 100),
            }
        )

    _, ax = plt.subplots()
    df = pd.DataFrame(rows, index=fy_index)
    df.plot(secondary_y=["etr"], ax=ax)
    ax.set_ylim(bottom=0)
    ax.right_ax.set_ylim(bottom=0)  # type: ignore[attr-defined]
    plt.show()


if __name__ == "__main__":
    _show_tax_paid(income=50_000, inflation_adjusted=inflation.InflationMeasure.WPI)
