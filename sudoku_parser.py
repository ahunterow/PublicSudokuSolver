import pandas as pd
import numpy as nu


import settings
from settings import *


def create_sudoku_list():
    """Returns a tuple of lists of sudokus. INSPIRED BY SHIVAVARMA'S DATA PREPROCESSING"""
    # Removing Pandas truncation for easier debug printing
    pd.set_option("display.max_colwidth", None)

    # Chunk size is the number of sudokus we wish to select
    chunk_size = read_in_amount

    # A list of tuples; the first element of tuples is the puzzle, the second the solution
    normalized_puzzles = []
    formatted_solutions = []

    # Creating our pandas datagram, starting at starting_row and ending at starting_row + chunk_size
    sudoku_file = pd.read_csv("sudoku.csv", skiprows=settings.row_offset,
                              nrows=chunk_size, header=None, names=["puzzle", "solution"])

    puzzles = sudoku_file["puzzle"]
    solutions = sudoku_file["solution"]

    for puzzle in puzzles:
        initial_arr = nu.array([int(x)
                               for x in str(puzzle)]).reshape((9, 9, 1))

        normalized_puzzles.append(initial_arr)

    # Mean-centered Normalization.
    normalized_puzzles = nu.array(normalized_puzzles)
    normalized_puzzles = normalized_puzzles / 9
    normalized_puzzles = normalized_puzzles - 0.5

    for solution in solutions:
        initial_arr = nu.array([int(x)
                                # Uncomment this for training, comment it for the demo.
                               # for x in str(solution)]).reshape((81, 1)) - 1

                                # Uncomment this for the demo, comment this for training.
                                for x in str(solution)]).reshape(9, 9, 1)

        formatted_solutions.append(initial_arr)

    formatted_solutions = nu.array(formatted_solutions)

    # Tuple of numpy arrays of puzzles and solutions, which are numpy arrays that differ by shape.
    sudoku_list = (normalized_puzzles, formatted_solutions)


    return sudoku_list
