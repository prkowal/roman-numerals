import unittest

from roman_numerals import from_roman, is_valid, to_roman


class ToRomanTests(unittest.TestCase):
    def test_known_values(self):
        cases = {
            1: "I",
            4: "IV",
            9: "IX",
            14: "XIV",
            40: "XL",
            49: "XLIX",
            90: "XC",
            444: "CDXLIV",
            1994: "MCMXCIV",
            3999: "MMMCMXCIX",
        }
        for number, numeral in cases.items():
            self.assertEqual(to_roman(number), numeral)

    def test_rejects_out_of_range(self):
        with self.assertRaises(ValueError):
            to_roman(0)
        with self.assertRaises(ValueError):
            to_roman(4000)

    def test_rejects_non_int(self):
        with self.assertRaises(TypeError):
            to_roman("14")
        with self.assertRaises(TypeError):
            to_roman(True)


class FromRomanTests(unittest.TestCase):
    def test_known_values(self):
        cases = {
            "I": 1,
            "IV": 4,
            "IX": 9,
            "XIV": 14,
            "XL": 40,
            "XLIX": 49,
            "XC": 90,
            "CDXLIV": 444,
            "MCMXCIV": 1994,
            "MMMCMXCIX": 3999,
        }
        for numeral, number in cases.items():
            self.assertEqual(from_roman(numeral), number)

    def test_rejects_malformed_numerals(self):
        for numeral in ("IIII", "VV", "IC", "VX", "MMMM", "", "iv", "XIVI"):
            with self.assertRaises(ValueError):
                from_roman(numeral)

    def test_round_trip(self):
        for number in range(1, 4000):
            self.assertEqual(from_roman(to_roman(number)), number)

    def test_lowercase_rejected_by_default(self):
        with self.assertRaises(ValueError):
            from_roman("mcmxciv")

    def test_lowercase_accepted_when_opted_in(self):
        self.assertEqual(from_roman("mcmxciv", normalize_case=True), 1994)
        self.assertEqual(from_roman("McmXciv", normalize_case=True), 1994)

    def test_opt_in_still_rejects_malformed_numerals(self):
        with self.assertRaises(ValueError):
            from_roman("iiii", normalize_case=True)


class IsValidTests(unittest.TestCase):
    def test_accepts_canonical_forms(self):
        self.assertTrue(is_valid("MCMXCIV"))

    def test_rejects_bad_shapes_without_raising(self):
        self.assertFalse(is_valid("IIII"))
        self.assertFalse(is_valid(""))
        self.assertFalse(is_valid(None))

    def test_lowercase_rejected_by_default(self):
        self.assertFalse(is_valid("mcmxciv"))

    def test_lowercase_accepted_when_opted_in(self):
        self.assertTrue(is_valid("mcmxciv", normalize_case=True))
        self.assertFalse(is_valid("iiii", normalize_case=True))


if __name__ == "__main__":
    unittest.main()
