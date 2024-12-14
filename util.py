# Util functions for advent-of-code problems
from __future__ import annotations

from typing import Any, Callable

type Entry = str | int
type Parse = Callable[
    [str], Entry
]  # Parsing characters should be an int or char
type Index = tuple[int, int]
type MatrixVal = Any


def add(index1: Index, index2: Index) -> Index:
    i1, j1 = index1
    i2, j2 = index2
    return (i1 + i2, j1 + j2)


class Matrix:
    # We assume the matrix is regular (each row same length)
    # For now, only works if each 'field' is one character
    def __init__(
        self, text: str, parse: Parse = (lambda x: x), *, is_wrap: bool = False
    ) -> None:
        self.matrix = [[parse(x) for x in line] for line in text.split("\n")]
        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0])
        self.is_wrap = is_wrap

    # Pretty printing
    def __str__(self) -> str:
        return "\n".join("".join(str(x) for x in row) for row in self.matrix)

    def is_valid_index(self, index: Index) -> bool:
        (i, j) = index
        return (0 <= i < self.cols) and (0 <= j < self.rows)

    def entry(self, index: Index) -> MatrixVal | None:
        """Get entry of matrix at given entry, if applicable."""
        i, j = index[0] if len(index) == 1 else index
        if self.is_valid_index((i, j)):
            return self.matrix[j][i]
        return None

    def entry_ij(self, i: int, j: int) -> MatrixVal | None:
        # Entry passing indices directly, rather than as a tuple
        return self.entry((i, j))

    def move(self, start: Index, step: Index) -> tuple[Index, MatrixVal] | None:
        # args: First value is current index, second value is change in index
        new_index = add(start, step)
        if val := self.entry(new_index):  # Checks if None
            return (new_index, val)
        return None

    # def move(self, start: Index, step: Index) -> Index | None:
    #     # Returns index in direction, if it has a value (if we don't care
    #     # whether it has a value, we could just use 'add' above instead)
    #     new_index = add(start, step)
    #     if self.entry(new_index) is None:
    #         return None
    #     return new_index
