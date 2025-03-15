import matplotlib.pyplot as plt
import pandas as pd
import typing
from analysis import tax, labels, inflation


def _show_tax_tables(
    inflation_adjusted: typing.Optional[inflation.InflationMeasure] = None,
) -> None:
    tax_tables = tax.load_tax_tables()
    if inflation_adjusted is not None:
        tax_tables = tax_tables.adjusted_for_inflation(
            inflation.load_inflation(measure=inflation_adjusted)
        )

    rows = []
    for year in tax_tables.year_tables:
        for bracket in year.brackets:
            rows.append(
                {
                    "year": labels.financial_year(year.year),
                    "start": bracket.start,
                    "rate": f"{bracket.rate * 100:.0f}%",
                }
            )
    rows.sort(key=lambda r: (r["year"], r["start"]))
    x_to_fy = labels.create_x_to_fy([r["year"] for r in rows])  # type: ignore[misc]

    df = pd.DataFrame(rows)
    _, ax = plt.subplots()
    df.plot.scatter(
        x="year",
        y="start",
        ax=ax,
        figsize=(14, 6),
        ylabel="Tax bracket in $",
    )

    for _, row in df.iterrows():
        ax.annotate(
            row["rate"],
            (row["year"], row["start"]),
            xytext=(10, 10),
            textcoords="offset pixels",
        )

    plt.xticks(rotation=40)
    plt.gca().format_coord = (  # type: ignore[method-assign]
        lambda x, y: f"fy={x_to_fy(x)}, ${y:,.0f}"
    )
    plt.show()


if __name__ == "__main__":
    _show_tax_tables(inflation.InflationMeasure.CPI)
