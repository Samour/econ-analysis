import unittest
from analysis import parse


class ParseFinancialYearTests(unittest.TestCase):

    def test_parse_valid_financial_year(self) -> None:
        result = parse.parse_financial_year("2022-23")

        self.assertEqual(result, 2022)

    def test_parse_millenial_financial_year(self) -> None:
        result = parse.parse_financial_year("1999-2000")

        self.assertEqual(result, 1999)

    def test_parse_financial_year_wrong_format(self) -> None:
        with self.assertRaises(AssertionError):
            parse.parse_financial_year("2022-2024")

    def test_parse_financial_year_too_long(self) -> None:
        with self.assertRaises(AssertionError):
            parse.parse_financial_year("2022-24")

    def test_parse_financial_year_backwards(self) -> None:
        with self.assertRaises(AssertionError):
            parse.parse_financial_year("2022-21")

    def test_parse_financial_year_single(self) -> None:
        with self.assertRaises(AssertionError):
            parse.parse_financial_year("2022")

    def test_parse_financial_year_repeated(self) -> None:
        with self.assertRaises(AssertionError):
            parse.parse_financial_year("2022-22")

    def test_parse_financial_year_not_numeric(self) -> None:
        with self.assertRaises(AssertionError):
            parse.parse_financial_year("year-ab")
