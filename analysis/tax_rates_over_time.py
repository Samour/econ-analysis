import matplotlib.pyplot as plt
import pandas as pd
from analysis import tax


_clamp = lambda x, y, z: max(x, min(y, z))


def _show_tax_tables() -> None:
    tax_tables = tax.load_tax_tables()

    rows = []
    for year in tax_tables.year_tables:
        fy = (
            "1999-2000"
            if year.year == 1999
            else f"{year.year}-{year.year % 100 + 1:02}"
        )
        for bracket in year.brackets:
            rows.append({"year": fy, "start": bracket.start, "rate": bracket.rate})
    rows.sort(key=lambda r: (r["year"], r["start"]))
    year_index: list[str] = []
    for row in rows:
        if len(year_index) == 0 or year_index[-1] != row["year"]:
            year_index.append(row["year"])  # type: ignore[arg-type]

    tax_rates_table = pd.DataFrame(rows)
    tax_rates_table.plot.scatter(x="year", y="start", figsize=(14, 6))
    plt.xticks(rotation=40)
    plt.gca().format_coord = (  # type: ignore[method-assign]
        lambda x, y: f"fy={year_index[_clamp(0, round(x), len(year_index) - 1)]}, ${y:,.0f}"  # type: ignore[no-untyped-call]
    )
    plt.show()


if __name__ == "__main__":
    _show_tax_tables()
