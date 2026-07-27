"""Grader for Module 00. Do not edit — this file defines "correct".

Failure messages are written to tell you what was expected. Read them.
"""

import inspect

import pytest

from exercises import (
    RunningStats,
    chunk,
    evens,
    flatten,
    group_by,
    moving_average,
    read_csv_column,
    safe_divide,
    top_n,
    word_count,
)


# --- 1. evens -------------------------------------------------------------
class TestEvens:
    def test_basic(self):
        assert evens(10) == [0, 2, 4, 6, 8]

    def test_upper_bound_is_exclusive(self):
        assert evens(9) == [0, 2, 4, 6, 8], "n is exclusive: evens(9) must not include 9"
        assert evens(8) == [0, 2, 4, 6], "8 is excluded because the range is [0, n)"

    def test_empty(self):
        assert evens(0) == []
        assert evens(1) == [0]

    def test_negative_n_is_empty(self):
        assert evens(-5) == [], "range(-5) is empty; don't special-case it, just let it be"

    def test_returns_a_list(self):
        assert isinstance(evens(4), list), "return a list, not a generator or range object"


# --- 2. word_count --------------------------------------------------------
class TestWordCount:
    def test_basic(self):
        assert word_count("the cat sat") == {"the": 1, "cat": 1, "sat": 1}

    def test_case_insensitive(self):
        assert word_count("The THE the") == {"the": 3}

    def test_strips_punctuation(self):
        assert word_count("Hello, world! Hello.") == {"hello": 2, "world": 1}

    def test_punctuation_only_tokens_dropped(self):
        assert word_count("hi ... there") == {"hi": 1, "there": 1}, (
            "'...' strips down to the empty string — drop it, don't count '' as a word"
        )

    def test_internal_punctuation_kept(self):
        assert word_count("it's a well-known fact.") == {
            "it's": 1,
            "a": 1,
            "well-known": 1,
            "fact": 1,
        }, "only strip punctuation from the ENDS of a token, not the middle"

    def test_empty_string(self):
        assert word_count("") == {}

    def test_returns_plain_dict(self):
        result = word_count("a a b")
        assert type(result) is dict, (
            f"return a plain dict, got {type(result).__name__}. "
            "A Counter is fine to use internally — call dict() on it before returning."
        )


# --- 3. safe_divide -------------------------------------------------------
class TestSafeDivide:
    def test_normal_division(self):
        assert safe_divide(10, 4) == 2.5

    def test_divide_by_zero(self):
        assert safe_divide(1, 0) == 0.0

    def test_custom_default(self):
        assert safe_divide(1, 0, default=-1.0) == -1.0

    def test_non_numeric(self):
        assert safe_divide("x", 2, default=-1.0) == -1.0
        assert safe_divide(2, None, default=-1.0) == -1.0

    def test_does_not_swallow_unrelated_errors(self):
        """A bare `except:` passes every test above and is still wrong."""

        class Exploding:
            def __truediv__(self, other):
                raise KeyboardInterrupt("this must propagate")

        with pytest.raises(KeyboardInterrupt):
            safe_divide(Exploding(), 2)


# --- 4. top_n -------------------------------------------------------------
class TestTopN:
    def test_basic(self):
        assert top_n({"a": 3, "b": 5, "c": 1}, 2) == [("b", 5), ("a", 3)]

    def test_ties_break_alphabetically(self):
        assert top_n({"c": 3, "a": 3, "b": 3}, 3) == [("a", 3), ("b", 3), ("c", 3)], (
            "equal counts must be ordered by key ascending"
        )

    def test_n_larger_than_input(self):
        assert top_n({"a": 1}, 10) == [("a", 1)]

    def test_n_zero_and_empty_input(self):
        assert top_n({"a": 1}, 0) == []
        assert top_n({}, 5) == []

    def test_returns_tuples(self):
        result = top_n({"a": 1}, 1)
        assert isinstance(result[0], tuple), "each element must be a (key, value) tuple"


# --- 5. flatten -----------------------------------------------------------
class TestFlatten:
    def test_basic(self):
        assert flatten([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]

    def test_already_flat(self):
        assert flatten([1, 2, 3]) == [1, 2, 3]

    def test_deeply_nested(self):
        assert flatten([[[[[1]]]]]) == [1]

    def test_empty_lists_vanish(self):
        assert flatten([[], [[[]]], [1]]) == [1]

    def test_mixed_types_pass_through(self):
        assert flatten(["a", [None, [1.5]], True]) == ["a", None, 1.5, True]

    def test_strings_are_not_flattened(self):
        assert flatten([["ab"], "cd"]) == ["ab", "cd"], (
            "a str is iterable but is not a list — it must pass through whole, "
            "not become ['a','b']"
        )


# --- 6. chunk -------------------------------------------------------------
class TestChunk:
    def test_even_split(self):
        assert chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]

    def test_ragged_final_chunk(self):
        assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]

    def test_size_larger_than_input(self):
        assert chunk([1, 2], 10) == [[1, 2]]

    def test_empty_input(self):
        assert chunk([], 3) == []

    def test_invalid_size_raises(self):
        with pytest.raises(ValueError):
            chunk([1, 2, 3], 0)
        with pytest.raises(ValueError):
            chunk([1, 2, 3], -1)


# --- 7. group_by ----------------------------------------------------------
class TestGroupBy:
    ROWS = [
        {"city": "NY", "n": 1},
        {"city": "LA", "n": 2},
        {"city": "NY", "n": 3},
    ]

    def test_basic(self):
        assert group_by(self.ROWS, "city") == {
            "NY": [{"city": "NY", "n": 1}, {"city": "NY", "n": 3}],
            "LA": [{"city": "LA", "n": 2}],
        }

    def test_preserves_order_within_group(self):
        rows = [{"k": "a", "i": i} for i in range(5)]
        assert [r["i"] for r in group_by(rows, "k")["a"]] == [0, 1, 2, 3, 4]

    def test_missing_key_records_skipped(self):
        rows = [{"city": "NY"}, {"other": 1}, {"city": "LA"}]
        assert group_by(rows, "city") == {"NY": [{"city": "NY"}], "LA": [{"city": "LA"}]}

    def test_empty_input(self):
        assert group_by([], "city") == {}

    def test_returns_plain_dict(self):
        result = group_by(self.ROWS, "city")
        assert type(result) is dict, (
            f"return a plain dict, got {type(result).__name__}. "
            "A defaultdict silently invents empty groups for missing keys — "
            "call dict() on it before returning."
        )


# --- 8. moving_average ----------------------------------------------------
class TestMovingAverage:
    def test_basic(self):
        assert list(moving_average([1, 2, 3, 4], 2)) == [1.5, 2.5, 3.5]

    def test_window_of_one_is_identity(self):
        assert list(moving_average([1, 2, 3], 1)) == [1.0, 2.0, 3.0]

    def test_window_equals_length(self):
        assert list(moving_average([2, 4], 2)) == [3.0]

    def test_window_too_large_yields_nothing(self):
        assert list(moving_average([1, 2], 5)) == []

    def test_invalid_window_raises(self):
        with pytest.raises(ValueError):
            list(moving_average([1, 2, 3], 0))

    def test_is_actually_a_generator(self):
        result = moving_average([1, 2, 3], 2)
        assert inspect.isgenerator(result), (
            f"must be a generator function using `yield`, got {type(result).__name__}. "
            "Building a list and returning it defeats the point."
        )

    def test_is_lazy(self):
        """Calling a generator function runs none of its body."""
        gen = moving_average([1, 2, 3, 4], 2)
        assert inspect.getgeneratorstate(gen) == "GEN_CREATED", (
            "no code should have run yet — a generator body doesn't execute "
            "until the first next()"
        )
        assert next(gen) == 1.5
        assert inspect.getgeneratorstate(gen) == "GEN_SUSPENDED"

    def test_produces_one_window_at_a_time(self):
        """Pulling one value must not require computing all of them."""
        gen = moving_average(list(range(1_000_000)), 3)
        assert next(gen) == pytest.approx(1.0)


# --- 9. read_csv_column ---------------------------------------------------
class TestReadCsvColumn:
    @pytest.fixture
    def csv_path(self, tmp_path):
        p = tmp_path / "sales.csv"
        p.write_text("region,amount\nNorth,100\nSouth,250\nWest,75\n")
        return str(p)

    def test_reads_column(self, csv_path):
        assert read_csv_column(csv_path, "amount") == ["100", "250", "75"]

    def test_reads_other_column(self, csv_path):
        assert read_csv_column(csv_path, "region") == ["North", "South", "West"]

    def test_values_stay_strings(self, csv_path):
        assert all(isinstance(v, str) for v in read_csv_column(csv_path, "amount"))

    def test_missing_column_raises_keyerror(self, csv_path):
        with pytest.raises(KeyError):
            read_csv_column(csv_path, "nope")

    def test_header_only_file(self, tmp_path):
        p = tmp_path / "empty.csv"
        p.write_text("a,b\n")
        assert read_csv_column(str(p), "a") == []

    def test_handles_quoted_commas(self, tmp_path):
        """The reason you use the csv module instead of str.split(',')."""
        p = tmp_path / "quoted.csv"
        p.write_text('name,amount\n"Smith, John",100\n"Doe, Jane",250\n')
        assert read_csv_column(str(p), "amount") == ["100", "250"], (
            "line.split(',') puts the amount in the wrong position here — "
            "use csv.DictReader"
        )
        assert read_csv_column(str(p), "name") == ["Smith, John", "Doe, Jane"]


# --- 10. RunningStats -----------------------------------------------------
class TestRunningStats:
    SAMPLE = [2, 4, 4, 4, 5, 5, 7, 9]

    def test_fresh_object(self):
        s = RunningStats()
        assert s.count == 0
        assert s.mean == 0.0
        assert s.variance == 0.0

    def test_single_value(self):
        s = RunningStats()
        s.add(5)
        assert s.count == 1
        assert s.mean == 5.0
        assert s.variance == 0.0, "variance of one observation is 0.0, not a crash"

    def test_known_sample(self):
        s = RunningStats()
        for x in self.SAMPLE:
            s.add(x)
        assert s.count == 8
        assert s.mean == pytest.approx(5.0)
        assert s.variance == pytest.approx(4.0), (
            "use the POPULATION formula (divide by n). Dividing by n-1 "
            "(sample variance) gives 4.571 here."
        )

    def test_count_is_an_int(self):
        s = RunningStats()
        s.add(1)
        assert isinstance(s.count, int) and not isinstance(s.count, bool)

    def test_add_returns_none(self):
        assert RunningStats().add(1) is None

    def test_handles_floats(self):
        s = RunningStats()
        for x in [1.5, 2.5, 3.5]:
            s.add(x)
        assert s.mean == pytest.approx(2.5)

    def test_does_not_store_the_values(self):
        """Streaming means O(1) memory — the whole point of the exercise."""
        s = RunningStats()
        for x in range(1000):
            s.add(x)
        for name, value in vars(s).items():
            if isinstance(value, (list, tuple, set, dict, frozenset)):
                assert len(value) < 100, (
                    f"attribute {name!r} is holding {len(value)} items. "
                    "Keep running sums (n, sum(x), sum(x**2)) — not the values."
                )
