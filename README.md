# Sudoku Solver

Phil Incorporated:

Andrew Hunter-Owega
ahunterow@unbc.ca

Daniel Strickland
dstrickla@unbc.ca

Nicholas Hirt
nhirt@unbc.ca

# Files

## main.py:

This has the methods needed for training a network, and
has the methods for predicting data.

## network.py: 

This defines the actual structure of the neural network by its layers.
It is inspired by Shiva Verma's model, and anything commented with:

\# BORROWED

is taken and or heavily inspired from his model.

## gui.py:

This is the driver program for the model, and defines the structure of our GUI.

## settings.py:

This declares a bunch of constants that affect the running of the rest of the program.

## sudoku_parser.py:

This has the methods for parsing in the data from the csv file.
It is somewhat inspired by Shiva Verma's data preprocessing, but
less so than our network class.

## sudoku.csv:

This contains the dataset we used, it has 9000000 puzzles. We trained on the first 1000000 puzzles.

## our_model2.h5:

This is the saved file representing our model, and is loaded for predictions.

# How to Run
You will need to download the dataset at:

https://www.kaggle.com/datasets/rohanrao/sudoku

It's very large so it would not be prudent to hand it in directly.

This project uses python, so you will need a python environment.
You will need to have installed tensorflow, pandas, sklearn, tkinter, and numpy libraries
for this project to work. 

To run the project, run the gui.py file. This will open up the GUI which will solve a number of randomly selected puzzles that were not in the training data.
It will provide accuracy of prediction by cell and by table.

The model will read from the "sudoku.csv" file.

To train new models, use the test_sudoku_network() function in main.py, uncommenting the saves, loads, and splits as desired.
The constants in settings will need to be changed as well to reflect the size of data used, and the amount
You wish to train on.
In sudoku_parser.py, comment the demo output format and uncomment the training format. Then,
uncomment the test_sudoku_network() function in main.py and run it.

Please note, the ability to train new models is not intended for the average user nor is it
an intended feature. 

# Sources:

Our Dataset:

Vopani, “9 million Sudoku puzzles and solutions,” Kaggle, 14-Nov-2019. [Online]. Available: https://www.kaggle.com/datasets/rohanrao/sudoku.

Inspired by:

S. Verma, “Shivaverma/Sudoku-solver: Solving sudoku with convolution neural networks.,” GitHub. [Online]. Available: https://github.com/shivaverma/Sudoku-Solver. [Accessed: 29-Mar-2023].

