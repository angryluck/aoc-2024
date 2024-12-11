# Util functions for advent-of-code problems
from __future__ import annotations

from typing import Any, Callable

type Entry = str | int
type Parse = Callable[str, Entry] # Parsing characters should be an
type Index = (int, int)
# int or char
type MatrixVal = Any
class Matrix:
    # We assume the matrix is regular (each row same length)
    def __init__(self, text:str, parse:Parse = (lambda x: x),
                 *, is_wrap:bool=False)->None:
        self.matrix = [[parse(x) for x in line] for line in text.split("\n")]
        self.rows = len(self.matrix)
        self.cols = len(self.matrix[0])
        self.is_wrap = is_wrap

    def is_valid_index(self, index:Index) -> bool:
        (i,j) = index
        return (0<=i<self.cols) and (0<=j<self.rows)

    def entry(self, *index:Index) -> MatrixVal | None:
        """Get entry of matrix at given entry, if applicable."""
        i, j = index[0] if len(index) == 1 else index
        if self.is_valid_index((i,j)):
            return self.matrix[j][i]
        return None

    def move(self, *args: Index | int) -> (Index, MatrixVal | None):
        # args: First value is current index, second value is change in index
        max_args = 2
        if len(args) == max_args:
            (i, j), (di,dj) = args
        else:
            i,j,di,dj=args
        new_index = (i+di, j+dj)
        return (new_index, self.entry(new_index))


# test = Matrix("123\n456\n789")

### Graveyard
    # def up(self, index:Index) -> Index | None:
    #     (i,j) = index
    #     new_index = (i,j-1)
    #     return new_index if self.is_valid_index(new_index) else None

    # def down(self, index:Index) -> MatrixVal:
    #     (i,j) = index
    #     new_index = (i,j+1)
    #     return new_index if self.is_valid_index(new_index) else None
    #
    # def left(self, index:Index) -> Index | None:
    #     (i,j) = index
    #     new_index = (i+1, j)
    #     return new_index if self.is_valid_index(new_index) else None
    #
    # def right(self, index:Index) -> Index | None:
    #     (i,j) = index
    #     new_index = (i-1, j)
    #     return new_index if self.is_valid_index(new_index) else None
    #
    # def upright(self, index:Index) -> Index | None:
    #     (i,j) = index
    #     new_index = (i+1, j-1)
    #     return new_index if self.is_valid_index(new_index) else None
    #
    # def upleft(self, index:Index) -> Index | None:
    #     (i,j) = index
    #     new_index = (i-1, j-1)
    #     return new_index if self.is_valid_index(new_index) else None
    #
    # def downright(self, index:Index) -> Index | None:
    #     (i,j) = index
    #     new_index = (i+1, j+1)
    #     return new_index if self.is_valid_index(new_index) else None
    #
    # def downleft(self, index:Index) -> Index | None:
    #     (i,j) = index
    #     new_index = (i-1, j+1)
    #     return new_index if self.is_valid_index(new_index) else None


