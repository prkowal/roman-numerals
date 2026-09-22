# roman-numerals

A parser and pretty printer for roman numerals, in the range 1-3999.

The interesting part isn't converting a number to roman digits, it's
deciding what counts as a *valid* roman numeral going the other direction.
A parser that just walks the string summing values (add a symbol's value,
subtract it if a smaller value comes before a larger one) will accept
strings no one actually writes, like `IIII` instead of `IV`, or `IC`
instead of `XCIX`. This library validates the numeral's shape before it
converts, so `from_roman` only accepts canonical forms.

## Usage

```python
from roman_numerals import from_roman, is_valid, to_roman

to_roman(1994)          # "MCMXCIV"
from_roman("MCMXCIV")   # 1994

is_valid("IIII")        # False, not canonical
from_roman("IIII")      # raises ValueError

to_roman(0)              # raises ValueError, no roman numeral for zero
to_roman(4000)            # raises ValueError, out of representable range
```

All three public functions are pure: same input, same output, no shared
state, no I/O. `is_valid` never raises; `from_roman` and `to_roman` raise
`ValueError` (or `TypeError` for bad input types) instead of returning a
sentinel, so callers can't accidentally ignore a bad conversion.

### Command line

```
romannum 1994      # MCMXCIV
romannum MCMXCIV   # 1994
```

The direction is inferred from the argument: all digits means
arabic-to-roman, anything else is parsed as a roman numeral. A bad
conversion prints an error to stderr and exits with status 1 instead of
raising.

## Design

- `to_roman` builds the numeral greedily from a fixed table of
  value/symbol pairs ordered high to low, including the subtractive pairs
  (`CM`, `CD`, `XC`, `XL`, `IX`, `IV`) as single table entries. That keeps
  the subtraction logic out of the code entirely.
- `is_valid` checks the numeral against a regular expression that encodes
  the actual grammar (at most one subtractive pair per magnitude, at most
  three repeats of a base symbol).
- `from_roman` calls `is_valid` first, then sums using the same table
  `to_roman` uses, so encoding and decoding agree on what a symbol is
  worth by construction.

## Status

Early skeleton. Core conversion and validation work and are tested for the
full 1-3999 range. See the roadmap for what's still missing.

## License

MIT, see [LICENSE](LICENSE).
