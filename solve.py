from __future__ import annotations
from typing import Union

import argparse
import os
import sys

from sudoku import Sudoku, load_from_file


def solve(sudoku: Sudoku) -> Union[Sudoku, None]:
    """
    Solve a Sudoku puzzle using Depth First Search (DFS).
    Returns a Sudoku puzzle if the puzzle is solvable, None otherwise.
    """
    stack = [sudoku]

    while stack:
        sudoku = stack.pop()

        if sudoku.is_solved():
            return sudoku

        x, y = sudoku.next_empty_index()

        for option in sudoku.options_at(x, y):
            child_sudoku = sudoku.copy()
            child_sudoku.place(option, x, y)
            stack.append(child_sudoku)

    return None


if __name__ == "__main__":
    # Create a command line argument parser
    parser = argparse.ArgumentParser(description='Solve a sudoku puzzle.')
    parser.add_argument("puzzle", type=int, help="identifier of the puzzle to be solved")
    parser.add_argument("-n", type=int, default=1, dest="number_of_runs", help="number of runs")

    # Parse the command line arguments
    args = parser.parse_args()

    puzzle_path = f"puzzles/{args.puzzle}.csv"

    # If the puzzle does not exist, exit
    if not os.path.exists(puzzle_path):
        print(f"puzzle {args.puzzle} does not exist")
        sys.exit(1)

    # Load the puzzle
    sudoku = load_from_file(puzzle_path)

    # Show the puzzle to the user
    print(sudoku)
    print()

    # Solve the puzzle args.number_of_runs times
    print("SOLVING...")
    for i in range(args.number_of_runs):
        solved_sudoku = solve(sudoku)
    print("DONE SOLVING")

    # Show the solution
    print()
    print(solved_sudoku)
