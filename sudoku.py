from __future__ import annotations
from typing import Iterable, Sequence


class Sudoku:
    """A mutable sudoku puzzle."""

    def __init__(self, puzzle: Iterable[Iterable]):
        self._grid = []

        for puzzle_row in puzzle:
            row = ""

            for element in puzzle_row:
                row += str(element)

            self._grid.append(row)

    def place(self, value: int, x: int, y: int) -> None:
        """Place value at x,y."""
        row = self._grid[y]
        new_row = ""

        for i in range(9):
            if i == x:
                new_row += str(value)
            else:
                new_row += row[i]

        self._grid[y] = new_row

    def copy(self) -> "Sudoku":
        """Creates a deepcopy of this Sudoku puzzle."""
        return Sudoku(self._grid)

    def value_at(self, x: int, y: int) -> int:
        """Returns the value at x,y."""
        row = self._grid[y]
        return int(row[x])

    def options_at(self, x: int, y: int) -> Sequence[int]:
        """Returns all possible values (options) at x,y."""
        options = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        # Remove all values from the row
        for value in self.row_values(y):
            if value in options:
                options.remove(value)

        # Remove all values from the column
        for value in self.column_values(x):
            if value in options:
                options.remove(value)

        # Get the index of the block based from x,y
        block_index = (y // 3) * 3 + x // 3

        # Remove all values from the block
        for value in self.block_values(block_index):
            if value in options:
                options.remove(value)

        return options

    def next_empty_index(self) -> tuple[int, int]:
        """
        Returns the next index (x,y) that is empty (value 0).
        If there is no empty spot, returns (-1,-1)
        """
        for y in range(9):
            for x in range(9):
                if self.value_at(x, y) == 0:
                    return x, y
        return -1, -1

    def row_values(self, i: int) -> Sequence[int]:
        """Returns all values at i-th row."""
        values = []

        for j in range(9):
            values.append(self.value_at(j, i))

        return values

    def column_values(self, i: int) -> Sequence[int]:
        """Returns all values at i-th column."""
        values = []

        for j in range(9):
            values.append(self.value_at(i, j))

        return values

    def block_values(self, i: int) -> Sequence[int]:
        """
        Returns all values at i-th block.
        The blocks are arranged as follows:
        0 1 2
        3 4 5
        6 7 8
        """
        values = []

        x_start = (i % 3) * 3
        y_start = (i // 3) * 3

        for x in range(x_start, x_start + 3):
            for y in range(y_start, y_start + 3):
                values.append(self.value_at(x, y))

        return values

    def is_solved(self) -> bool:
        """
        Returns True if and only if all rows, columns and blocks contain
        only the numbers 1 through 9. False otherwise.
        """
        values = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        for i in range(9):
            for value in values:
                if value not in self.column_values(i):
                    return False

                if value not in self.row_values(i):
                    return False

                if value not in self.block_values(i):
                    return False

        return True

    def __str__(self) -> str:
        representation = ""

        for row in self._grid:
            representation += row + "\n"

        return representation.strip()


def load_from_file(filename: str) -> Sudoku:
    """Load a Sudoku from filename."""
    puzzle = []

    with open(filename) as f:
        for line in f:

            # strip newline and remove all commas
            line = line.strip().replace(",", "")

            puzzle.append(line)

    return Sudoku(puzzle)
