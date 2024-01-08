"""A driver for training the sudoku network, and has the methods for the incremental prediction approach."""
import sudoku_parser
import tensorflow
import keras
from network import *
from settings import *
import numpy as nu
from sklearn import model_selection
import math


def test_sudoku_network():
    """Used for training the sudoku network."""
    sudoku_set = sudoku_parser.create_sudoku_list()

    xtest = sudoku_set[0]
    ytrain = sudoku_set[1]

    # Splits data
    xtrain, xtest, ytrain, ytest = model_selection.train_test_split(sudoku_set[0], sudoku_set[1], test_size=0.2)

    network = Network((sudoku_dim, sudoku_dim, 1))

    print(network.model.summary())

    # Loads network from file
    network.model = tensorflow.keras.models.load_model("our_model2.h5")

    # Just trains the network.
    # network.model.fit(xtrain, ytrain, epochs=2, batch_size=batch_size)

    # Trains the network and does validation testing on a whole-table scale.
    # network.model.fit(xtrain, ytrain, epochs=2, batch_size=batch_size, validation_data=(xtest,ytest))

    # Saves the model
    # network.model.save("our_model2.h5")


def denormalize(data):
    """Returns a denormalized form of the passed datapoint."""
    new_data = []

    for index, row in enumerate(data):
        new_data.append([])
        for jindex, col in enumerate(row):
            new_data[index].append(int(((data[index][jindex]+0.5) * 9)))

    return new_data


def predict_likely(sudoku, model):
    """Predicts a single cell in a sudoku grid."""
    results = model.predict(nu.array([sudoku]))

    max = (0, 0, 0, 0)
    for index, element_set in enumerate(results[0]):
        for jindex, element in enumerate(element_set):
            if max[0] < element:
                # Find most likely element in all the element sets. Return it normalized.
                pmax = (element, (((jindex + 1)/9) - 0.5),
                        (math.trunc(index/9)), (index % 9))

                if sudoku[pmax[2]][pmax[3]] == -0.5:  # if not already filled.
                    max = pmax

    prediction = (max[1], max[2], max[3])

    return prediction


def solve_sudoku(sudoku, model):
    """Takes in a sudoku and solves it."""
    while (not is_finished(sudoku)):
        guess = predict_likely(sudoku, model)

        sudoku[guess[1]][guess[2]] = guess[0]

    for index, row in enumerate(sudoku):
        for jindex, element in enumerate(row):
            # taking it out of numpy array
            sudoku[index][jindex] = sudoku[index][jindex][0]

    return denormalize(sudoku)


def is_finished(sudoku):
    """Returns True if a sudoku is finished."""
    for row in sudoku:
        for cell in row:
            if cell == -0.5:  # Normalized blank
                return False

    return True

# Runs the training function.
# test_sudoku_network()
