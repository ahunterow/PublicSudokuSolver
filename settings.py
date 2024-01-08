"""A collection of constants that change how parts of the program behave."""
TOTAL_ROWS = 9000000  # Amount of data in CSV file
read_in_amount = 10  # Amount of data to read in
sudoku_dim = 9  # Dimension of sudoku grid
batch_size = 64  # Batch size for training

# Indicates where the data is read from in the csv file, the GUI will overwrite this for random
# data selection. Our training data was up to 1000000.
row_offset = 8000000
learning_rate = 0.001 # Learning rate for the network

# The number of samples our demo network was trained on.
training_offset = 1000000