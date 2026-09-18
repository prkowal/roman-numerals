"""Parsing and printing for standard-form roman numerals (1-3999).

A naive summing parser (walk the string, add each symbol's value, subtract
when a smaller value precedes a larger one) will happily "parse" strings no
Roman ever wrote, like IIII, VV, or IC. It accepts those because it never
checks the *shape* of the numeral, only the running total. The parser here
validates against the actual grammar first and only sums once the shape is
confirmed, so from_roman rejects anything that isn't a canonical numeral.
"""

import re

# Ordered high to low so greedy matching in both directions works: building
# a numeral consumes the largest chunk first, and reading one back does too.
_VALUES = (
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
)

# Each group allows at most one subtractive pair, or up to three repeats of
# the base symbol (or one "half step" symbol followed by up to three of the
# base symbol). That shape is what rules out IIII, IC, VX, and similar.
_NUMERAL_PATTERN = re.compile(
    r"^M{0,3}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$"
)

MIN_VALUE = 1
MAX_VALUE = 3999


def is_valid(text: str) -> bool:
    """Return True if `text` is a canonical roman numeral, False otherwise.

    Never raises. Anything that isn't a non-empty string is simply not
    valid, including the empty string itself (there is no roman numeral
    for zero).
    """
    if not isinstance(text, str) or not text:
        return False
    return _NUMERAL_PATTERN.match(text) is not None


def from_roman(text: str) -> int:
    """Convert a canonical roman numeral to its integer value.

    Raises ValueError if `text` is not a valid numeral.
    """
    if not is_valid(text):
        raise ValueError(f"not a valid roman numeral: {text!r}")

    total = 0
    position = 0
    for value, symbol in _VALUES:
        while text[position:position + len(symbol)] == symbol:
            total += value
            position += len(symbol)
    return total


def to_roman(number: int) -> str:
    """Convert an integer in [1, 3999] to its canonical roman numeral.

    Raises TypeError for non-int input, ValueError if out of range.
    """
    if isinstance(number, bool) or not isinstance(number, int):
        raise TypeError(f"expected int, got {type(number).__name__}")
    if not MIN_VALUE <= number <= MAX_VALUE:
        raise ValueError(
            f"{number} is outside the representable range "
            f"[{MIN_VALUE}, {MAX_VALUE}]"
        )

    parts = []
    remaining = number
    for value, symbol in _VALUES:
        count, remaining = divmod(remaining, value)
        parts.append(symbol * count)
    return "".join(parts)
