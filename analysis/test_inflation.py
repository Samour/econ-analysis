import decimal
import json
import unittest
from analysis import inflation


class InflationTests(unittest.TestCase):

    def test_adjust(self) -> None:
        self._check_adjust(amount=100, from_year=2022, to_year=2024, expected="105.06")

    def test_adjust_to_current_year(self) -> None:
        self._check_adjust(amount=100, from_year=2024, to_year=2024, expected="100")

    def test_adjust_to_earlier_year(self) -> None:
        self._check_adjust(amount=100, from_year=2021, to_year=2023, expected="108.15")

    def test_adjust_backwards(self) -> None:
        with self.assertRaises(AssertionError):
            self._adjust(amount=100, from_year=2024, to_year=2023)

    def test_adjust_before_data(self) -> None:
        with self.assertRaises(AssertionError):
            self._adjust(amount=100, from_year=2019, to_year=2023)

    def test_adjust_after_data(self) -> None:
        with self.assertRaises(AssertionError):
            self._adjust(amount=100, from_year=2022, to_year=2026)

    def _check_adjust(
        self, amount: int, from_year: int, to_year: int, expected: str
    ) -> None:
        result = self._adjust(amount=amount, from_year=from_year, to_year=to_year)

        self.assertEqual(result, decimal.Decimal(expected))

    def _adjust(self, amount: int, from_year: int, to_year: int) -> decimal.Decimal:
        return self._load_inflation().adjust(
            amount=decimal.Decimal(amount), from_year=from_year, to_year=to_year
        )

    def _load_inflation(self) -> inflation.Inflation:
        data = """
        [
          {
            "year": "2023-24",
            "cpi": "0.02"
          },
          {
            "year": "2022-23",
            "cpi": "0.03"
          },
          {
            "year": "2021-22",
            "cpi": "0.05"
          }
        ]
        """
        return inflation._load_inflation_from_content(
            json.loads(data), inflation.InflationMeasure.CPI
        )
