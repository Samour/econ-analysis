import re


def parse_financial_year(fy: str) -> int:
    if fy == "1999-2000":
        return 1999

    match = re.match("(\\d{4})-(\\d{2})", fy)
    assert match is not None
    year = int(match.group(1))
    assert 2000 + int(match.group(2)) - year == 1, f"Invalid financial year: {fy}"

    return year
