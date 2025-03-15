import decimal
import json
import unittest
from analysis import tax


class ParseFinancialYearTests(unittest.TestCase):

    def test_parse_valid_financial_year(self) -> None:
        result = tax._parse_financial_year("2022-23")

        self.assertEqual(result, 2022)

    def test_parse_millenial_financial_year(self) -> None:
        result = tax._parse_financial_year("1999-2000")

        self.assertEqual(result, 1999)

    def test_parse_financial_year_wrong_format(self) -> None:
        with self.assertRaises(AssertionError):
            tax._parse_financial_year("2022-2024")

    def test_parse_financial_year_too_long(self) -> None:
        with self.assertRaises(AssertionError):
            tax._parse_financial_year("2022-24")

    def test_parse_financial_year_backwards(self) -> None:
        with self.assertRaises(AssertionError):
            tax._parse_financial_year("2022-21")

    def test_parse_financial_year_single(self) -> None:
        with self.assertRaises(AssertionError):
            tax._parse_financial_year("2022")

    def test_parse_financial_year_repeated(self) -> None:
        with self.assertRaises(AssertionError):
            tax._parse_financial_year("2022-22")

    def test_parse_financial_year_not_numeric(self) -> None:
        with self.assertRaises(AssertionError):
            tax._parse_financial_year("year-ab")


class LoadTaxBracketTests(unittest.TestCase):

    def test_load_tax_bracket(self) -> None:
        bracket = """
        {
            "min": "0",
            "max": "500",
            "rate": "0.30"
        }
        """
        result = tax._load_tax_bracket(json.loads(bracket))

        self.assertEqual(
            result,
            tax.TaxBracket(
                start=decimal.Decimal(0),
                end=decimal.Decimal(500),
                rate=decimal.Decimal("0.3"),
            ),
        )

    def test_load_tax_bracket_zero_rate(self) -> None:
        bracket = """
        {
            "min": "0",
            "max": "500",
            "rate": "0"
        }
        """
        result = tax._load_tax_bracket(json.loads(bracket))

        self.assertEqual(
            result,
            tax.TaxBracket(
                start=decimal.Decimal(0),
                end=decimal.Decimal(500),
                rate=decimal.Decimal(0),
            ),
        )

    def test_load_tax_bracket_end_equal_start(self) -> None:
        bracket = """
        {
            "min": "500",
            "max": "500",
            "rate": "0.3"
        }
        """
        with self.assertRaises(AssertionError):
            tax._load_tax_bracket(json.loads(bracket))

    def test_load_tax_bracket_end_below_start(self) -> None:
        bracket = """
        {
            "min": "500",
            "max": "400",
            "rate": "0.3"
        }
        """
        with self.assertRaises(AssertionError):
            tax._load_tax_bracket(json.loads(bracket))

    def test_load_tax_bracket_negative_rate(self) -> None:
        bracket = """
        {
            "min": "0",
            "max": "500",
            "rate": "-0.3"
        }
        """
        with self.assertRaises(AssertionError):
            tax._load_tax_bracket(json.loads(bracket))

    def test_load_tax_bracket_rate_over_one(self) -> None:
        bracket = """
        {
            "min": "0",
            "max": "500",
            "rate": "1.30"
        }
        """
        with self.assertRaises(AssertionError):
            tax._load_tax_bracket(json.loads(bracket))

    def test_load_tax_bracket_min_number_type(self) -> None:
        bracket = """
        {
            "min": 0,
            "max": "500",
            "rate": "0.30"
        }
        """
        with self.assertRaises(AssertionError):
            tax._load_tax_bracket(json.loads(bracket))

    def test_load_tax_bracket_non_numeric_min(self) -> None:
        bracket = """
        {
            "min": "zero",
            "max": "500",
            "rate": "0.30"
        }
        """
        with self.assertRaises(decimal.InvalidOperation):
            tax._load_tax_bracket(json.loads(bracket))

    def test_load_tax_bracket_max_number_type(self) -> None:
        bracket = """
        {
            "min": "0",
            "max": 500,
            "rate": "0.30"
        }
        """
        with self.assertRaises(AssertionError):
            tax._load_tax_bracket(json.loads(bracket))

    def test_load_tax_bracket_non_numeric_max(self) -> None:
        bracket = """
        {
            "min": "0",
            "max": "Five hundred",
            "rate": "0.30"
        }
        """
        with self.assertRaises(decimal.InvalidOperation):
            tax._load_tax_bracket(json.loads(bracket))

    def test_load_tax_bracket_rate_number_type(self) -> None:
        bracket = """
        {
            "min": "0",
            "max": "500",
            "rate": 0.30
        }
        """
        with self.assertRaises(AssertionError):
            tax._load_tax_bracket(json.loads(bracket))

    def test_load_tax_bracket_non_numeric_rate(self) -> None:
        bracket = """
        {
            "min": "0",
            "max": "500",
            "rate": "30 %"
        }
        """
        with self.assertRaises(decimal.InvalidOperation):
            tax._load_tax_bracket(json.loads(bracket))
