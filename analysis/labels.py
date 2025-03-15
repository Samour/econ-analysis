import typing


_clamp: typing.Callable[[int, int, int], int] = lambda x, y, z: max(x, min(y, z))


def financial_year(year: int) -> str:
    if year == 1999:
        return "1999-2000"
    else:
        return f"{year}-{year % 100 + 1:02}"


def create_x_to_fy(years: list[str]) -> typing.Callable[[float], str]:
    assert len(years) > 0

    year_index: list[str] = []
    for y in years:
        if len(year_index) == 0 or year_index[-1] != y:
            year_index.append(y)

    return lambda x: year_index[_clamp(0, round(x), len(year_index) - 1)]
