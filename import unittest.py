import unittest
from number_converter_project import NumberConverter

class TestNumberConverter(unittest.TestCase):
    def test_binary_to_decimal(self):
        result = NumberConverter.convert("1010", '1')
        self.assertEqual(result['results']['Decimal'], "10")

    def test_hex_fraction_to_decimal(self):
        result = NumberConverter.convert("A.8", '4')
        self.assertEqual(result['results']['Decimal'], "10.5")

    def test_invalid_input(self):
        with self.assertRaises(Exception):
            NumberConverter.convert("1021", '1')  # '2' is invalid in Binary

if __name__ == "__main__":
    unittest.main()