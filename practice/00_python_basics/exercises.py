"""
Module 00 — Python Fundamentals (refresher)

Ten exercises, ramping from warm-up to the kind of code you actually write in a
data pipeline. Replace each `raise NotImplementedError` with a real implementation.

Run the grader:
    pytest 00_python_basics -v
    pytest 00_python_basics -v -k evens     # just one exercise
    pytest 00_python_basics -x              # stop at first failure

Standard library only for this module. No numpy, no pandas — that's next.
"""

from __future__ import annotations


# ---------------------------------------------------------------------------
# 1. Comprehensions
# ---------------------------------------------------------------------------
def evens(n: int) -> list[int]:
    """Return the even numbers in [0, n) in ascending order.

    >>> evens(10)
    [0, 2, 4, 6, 8]
    >>> evens(0)
    []

    Hint: one list comprehension. If you reach for `for` + `.append()`, that
    works too — but the comprehension is the idiom you'll read everywhere.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# 2. Dicts as counters
# ---------------------------------------------------------------------------
def word_count(text: str) -> dict[str, int]:
    """Count word frequencies, case-insensitively.

    Words are whitespace-separated tokens. Strip surrounding punctuation
    (.,!?;:'" and parentheses) from each token. Tokens that become empty after
    stripping are dropped.

    >>> word_count("The cat sat. The CAT!")
    {'the': 2, 'cat': 2, 'sat': 1}

    Hint: `str.strip()` accepts a string of characters to remove, not just
    whitespace. `collections.Counter` is legal and idiomatic — but a Counter is
    not a plain dict, so convert before returning.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# 3. Exceptions
# ---------------------------------------------------------------------------
def safe_divide(a: float, b: float, default: float = 0.0) -> float:
    """Return a / b, or `default` when the division is undefined.

    Undefined means: b is zero, OR either argument isn't a number you can
    divide (e.g. a string, None). Catch the exception — don't pre-check types
    with isinstance. This is the "easier to ask forgiveness than permission"
    style Python prefers.

    >>> safe_divide(10, 4)
    2.5
    >>> safe_divide(1, 0)
    0.0
    >>> safe_divide("x", 2, default=-1.0)
    -1.0

    Hint: ZeroDivisionError and TypeError. Catch both, nothing wider — a bare
    `except:` would swallow bugs you want to see.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# 4. Sorting with a key
# ---------------------------------------------------------------------------
def top_n(counts: dict[str, int], n: int) -> list[tuple[str, int]]:
    """Return the n highest-count (key, value) pairs, highest first.

    Ties break alphabetically by key, ascending. If n exceeds the number of
    items, return all of them.

    >>> top_n({'a': 3, 'b': 5, 'c': 3}, 2)
    [('b', 5), ('a', 3)]

    Hint: `sorted(..., key=lambda item: ...)`. To sort one field descending and
    another ascending in a single pass, negate the numeric one in the key.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# 5. Nested structures
# ---------------------------------------------------------------------------
def flatten(nested: list) -> list:
    """Flatten an arbitrarily nested list of lists into a flat list.

    Order is preserved, depth-first. Non-list elements pass through unchanged.

    >>> flatten([1, [2, [3, 4]], 5])
    [1, 2, 3, 4, 5]
    >>> flatten([[], [[[]]], [1]])
    [1]

    Hint: recursion. For each element, ask "is this a list?" — if yes, recurse
    and extend; if no, append.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# 6. Slicing
# ---------------------------------------------------------------------------
def chunk(seq: list, size: int) -> list[list]:
    """Split `seq` into consecutive chunks of length `size`.

    The final chunk may be shorter. Raise ValueError if size < 1.

    >>> chunk([1, 2, 3, 4, 5], 2)
    [[1, 2], [3, 4], [5]]

    This is the batching primitive behind every "send 500 rows per API call"
    loop you'll ever write.

    Hint: `range(0, len(seq), size)` plus slicing. Slices past the end don't
    raise — they just come back short, which is exactly what you want here.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# 7. Grouping
# ---------------------------------------------------------------------------
def group_by(records: list[dict], key: str) -> dict:
    """Group a list of dict records by the value of `records[i][key]`.

    Records missing the key are skipped entirely. Within each group, records
    keep their original relative order.

    >>> rows = [{'city': 'NY', 'n': 1}, {'city': 'LA', 'n': 2}, {'city': 'NY', 'n': 3}]
    >>> group_by(rows, 'city')
    {'NY': [{'city': 'NY', 'n': 1}, {'city': 'NY', 'n': 3}], 'LA': [{'city': 'LA', 'n': 2}]}

    Hint: `collections.defaultdict(list)` avoids the "if key not in d" dance.
    Return a plain dict — defaultdict compares equal to dict, but callers that
    do `d['missing']` would silently get [] instead of a KeyError.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# 8. Generators
# ---------------------------------------------------------------------------
def moving_average(values: list[float], window: int):
    """Yield the mean of each consecutive `window`-sized slice of `values`.

    Yields nothing if the window is larger than the input. Raise ValueError if
    window < 1.

    >>> list(moving_average([1, 2, 3, 4], 2))
    [1.5, 2.5, 3.5]

    Note the signature: this is a *generator* — use `yield`, not `return
    [...]`. Generators are how you process a 40GB log file on a laptop: values
    are produced one at a time instead of all being held in memory.

    Hint: your `chunk` used a step of `size`; here the step is 1 and the
    windows overlap.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# 9. File I/O
# ---------------------------------------------------------------------------
def read_csv_column(path: str, column: str) -> list[str]:
    """Read a CSV file and return every value in the named column, in order.

    The first row is the header. Raise KeyError if the column isn't in the
    header. Values come back as strings — no type conversion.

    >>> read_csv_column("data/sales.csv", "amount")
    ['100', '250', '75']

    Hint: `csv.DictReader` handles quoting and embedded commas correctly.
    Hand-rolled `line.split(',')` breaks on the first quoted field containing a
    comma, and it will be real data that breaks it. Use a `with` block so the
    file closes even if something raises.
    """
    raise NotImplementedError


# ---------------------------------------------------------------------------
# 10. Classes
# ---------------------------------------------------------------------------
class RunningStats:
    """Accumulate numbers one at a time and report count / mean / variance.

    Streaming stats: you never store the values, only running aggregates. This
    is how you compute statistics over a dataset too large to hold in memory.

        >>> s = RunningStats()
        >>> for x in [2, 4, 4, 4, 5, 5, 7, 9]:
        ...     s.add(x)
        >>> s.count
        8
        >>> s.mean
        5.0
        >>> s.variance          # population variance (divide by n)
        4.0

    Requirements:
      - `add(x)` accumulates one value and returns None.
      - `count` is an int, 0 on a fresh object.
      - `mean` is 0.0 when count == 0.
      - `variance` is 0.0 when count < 2. Use the *population* formula (/ n).
      - Do NOT keep a list of the values. Keep running sums only.

    Hint: track n, sum(x), and sum(x**2). Then
    variance = sum(x**2)/n - mean**2.
    """

    def __init__(self) -> None:
        raise NotImplementedError

    def add(self, x: float) -> None:
        raise NotImplementedError

    @property
    def count(self) -> int:
        raise NotImplementedError

    @property
    def mean(self) -> float:
        raise NotImplementedError

    @property
    def variance(self) -> float:
        raise NotImplementedError
