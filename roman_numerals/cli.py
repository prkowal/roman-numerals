"""Command-line entry point: convert a value to or from roman numerals.

The direction is inferred from the argument's shape rather than a flag:
all-digit input goes arabic-to-roman, anything else is treated as a roman
numeral going the other way. One argument, one job, no mode switches to
remember.
"""

import argparse
import sys

from .core import from_roman, to_roman


def _convert(value: str) -> str:
    if value.isdigit():
        return to_roman(int(value))
    return str(from_roman(value))


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="romannum",
        description="Convert between integers and canonical roman numerals.",
    )
    parser.add_argument(
        "value",
        help="an integer 1-3999, or a canonical roman numeral to convert",
    )
    args = parser.parse_args(argv)

    try:
        result = _convert(args.value)
    except (TypeError, ValueError) as exc:
        print(f"romannum: {exc}", file=sys.stderr)
        return 1

    print(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
