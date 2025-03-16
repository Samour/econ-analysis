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

    fy_index = []
    rows = []
    for year in reversed(tax_tables.year_tables):
        fy_index.append(labels.financial_year(year.year))
        tax_amount = year.calculate_tax(d_income)
        rows.append(
            {
                "income": int(d_income),
                "tax": int(tax_amount),
                "etr": float(tax_amount / d_income * 100),
            }
        )

    _, ax = plt.subplots()
    df = pd.DataFrame(rows, index=fy_index)
    df.plot(secondary_y=["etr"], ax=ax)
    ax.set_ylim(bottom=0)
    ax.right_ax.set_ylim(bottom=0)  # type: ignore[attr-defined]
    plt.show()


if __name__ == "__main__":
    _show_tax_paid(100_000)
