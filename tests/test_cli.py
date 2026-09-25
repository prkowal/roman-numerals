import contextlib
import io
import unittest

from roman_numerals.cli import main


def run(argv):
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        status = main(argv)
    return status, stdout.getvalue().strip(), stderr.getvalue().strip()


class CliTests(unittest.TestCase):
    def test_arabic_to_roman(self):
        status, out, err = run(["1994"])
        self.assertEqual(status, 0)
        self.assertEqual(out, "MCMXCIV")
        self.assertEqual(err, "")

    def test_roman_to_arabic(self):
        status, out, err = run(["MCMXCIV"])
        self.assertEqual(status, 0)
        self.assertEqual(out, "1994")
        self.assertEqual(err, "")

    def test_out_of_range_int_fails_cleanly(self):
        status, out, err = run(["4000"])
        self.assertEqual(status, 1)
        self.assertEqual(out, "")
        self.assertIn("4000", err)

    def test_malformed_numeral_fails_cleanly(self):
        status, out, err = run(["IIII"])
        self.assertEqual(status, 1)
        self.assertEqual(out, "")
        self.assertIn("IIII", err)

    def test_lowercase_numeral_fails_cleanly_by_default(self):
        status, out, err = run(["mcmxciv"])
        self.assertEqual(status, 1)
        self.assertEqual(out, "")
        self.assertIn("mcmxciv", err)

    def test_lowercase_numeral_accepted_with_ignore_case_flag(self):
        status, out, err = run(["--ignore-case", "mcmxciv"])
        self.assertEqual(status, 0)
        self.assertEqual(out, "1994")
        self.assertEqual(err, "")

    def test_missing_argument_is_a_usage_error(self):
        with self.assertRaises(SystemExit) as ctx:
            run([])
        self.assertEqual(ctx.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
