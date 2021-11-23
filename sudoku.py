from __future__ import annotations
from typing import Iterable


class Sudoku:
    """A mutable sudoku puzzle."""

    def __init__(self, puzzle: Iterable[Iterable]):
        self._grid: list[list[int]] = []

        for puzzle_row in puzzle:
            self._grid.append([int(el) for el in puzzle_row])

        self._generate_options()
        self._generate_indices()
        self._empty_index = 0
        self._empty_spots = list(self._indices.keys())
        self._empty_spots.sort(key=lambda e: len(self._options[e]))
        self._n_empty_spots = len(self._empty_spots)

    def _generate_options(self):
        self._options = {}
        options = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        for i, puzzle_row in enumerate(self._grid):
            for j, element in enumerate(puzzle_row):
                if element == 0:
                    self._options[(j, i)] = options - \
                        (self.row_values(i) | self.column_values(j) | self.block_values((i // 3) * 3 + j // 3))

    def _generate_indices(self):
        self._indices = {}
        for loc in self._options:
            self._indices[loc] = []

            for other_loc in self._options:
                if loc == other_loc:
                    continue

                if loc[0] == other_loc[0] or\
                   loc[1] == other_loc[1] or\
                   (loc[0] // 3) * 3 + loc[1] // 3 == (other_loc[0] // 3) * 3 + other_loc[1] // 3:
                    self._indices[loc].append(other_loc)

    def place(self, value: int, x: int, y: int) -> None:
        """Place value at x,y."""
        self._grid[y][x] = value
        self._empty_index += 1

    def unplace(self, x: int, y: int) -> None:
        """Remove (unplace) a number at x,y."""
        self._grid[y][x] = 0
        self._empty_index -= 1

    def value_at(self, x: int, y: int) -> int:
        """Returns the value at x,y."""
        return self._grid[y][x]

    def options_at(self, x: int, y: int) -> Iterable[int]:
        """Returns all possible values (options) at x,y."""
        loc = (x, y)
        return self._options[loc] - {self._grid[i][j] for j, i in self._indices[loc]}

    def next_empty_index(self) -> tuple[int, int]:
        """
        Returns the next index (x,y) that is empty (value 0).
        If there is no empty spot, returns (-1,-1)
        """
        try:
            return self._empty_spots[self._empty_index]
        except IndexError:
            return -1, -1

    def row_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th row."""
        return {self._grid[i][j] for j in [0, 1, 2, 3, 4, 5, 6, 7, 8]}

    def column_values(self, i: int) -> Iterable[int]:
        """Returns all values at i-th column."""
        return {self._grid[j][i] for j in [0, 1, 2, 3, 4, 5, 6, 7, 8]}

    def block_values(self, i: int) -> Iterable[int]:
        """
        Returns all values at i-th block.
        The blocks are arranged as follows:
        0 1 2
        3 4 5
        6 7 8
        """
        x_start = (i % 3) * 3
        y_start = (i // 3) * 3

        return {self._grid[y][x]for x in range(x_start, x_start + 3) for y in range(y_start, y_start + 3)}

    def is_solved(self) -> bool:
        """
        Returns True if and only if all rows, columns and blocks contain
        only the numbers 1 through 9. False otherwise.
        """
        return self._empty_index >= self._n_empty_spots

    def __str__(self) -> str:
        representation = ""

        for row in self._grid:
            representation += str(row) + "\n"

        return representation.strip()


def load_from_file(filename: str) -> Sudoku:
    """Load a Sudoku from filename."""
    puzzle: list[str] = []

    with open(filename) as f:
        for line in f:

            # strip newline and remove all commas
            line = line.strip().replace(",", "")

            puzzle.append(line)

    return Sudoku(puzzle)
