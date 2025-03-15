import matplotlib.pyplot as plt
import pandas as pd
from analysis import inflation, labels


def _show_inflation_rates() -> None:
    cpi_inflation = inflation.load_inflation(measure=inflation.InflationMeasure.CPI)
    wpi_inflation = inflation.load_inflation(measure=inflation.InflationMeasure.WPI)

    fy_index = [labels.financial_year(i.year) for i in reversed(cpi_inflation.years)]
    df = pd.DataFrame(
        {
            "CPI": [float(i.achange * 100) for i in reversed(cpi_inflation.years)],
            "WPI": [float(i.achange * 100) for i in reversed(wpi_inflation.years)],
        },
        index=fy_index,
    )
    x_to_fy = labels.create_x_to_fy(fy_index)

    df.plot()
    plt.gca().format_coord = lambda x, y: f"y={x_to_fy(x)}, {y:.1f}%"  # type: ignore[method-assign]
    plt.show()


if __name__ == "__main__":
    _show_inflation_rates()
