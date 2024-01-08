
import tkinter as tk
import sudoku_parser
from settings import *
import random
import tensorflow
import keras
import main
import time
from network import *

class GUI():

    """Class GUI contains the tkinter GUI that displays the menu for the network demo."""

    def __init__(self, root):
        """Constructor for the Tkinter application."""
        self.root = root
        self.WIDTH = root.winfo_screenwidth()
        self.HEIGHT = root.winfo_screenheight()
        self.MENU_COLOR = "#0d1b2a"
        self.OPTIONS_COLOR = "#1b263b"
        self.DISPLAY_COLOR = "#0d1b2a"
        self.BUTTON_COLOR = "#1b4965"
        self.DARK_ACCENT = "#000814"
        self.LIGHT_ACCENT = "#00b4d8"
        self.DIALOGUE_FONT = ("Cambria", 18)
        self.OPTIONS_FONT = ("Cambria", 18)
        self.PUZZLE_FONT = ("Open Sans", 24)
        self.cells = {}
        self.buttons = [
            (1, "Run Accuracy Test", lambda: GUI.run_test(self)),
        ]

        # Window Attribute Settings
        root.geometry("%dx%d+%d+%d" % (self.WIDTH, self.HEIGHT, 0, 0))
        root.config(bg=self.MENU_COLOR)
        root.title("Sudoku Artificial Neural Net")
        root.resizable(False, False)
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=3)

        # Options Frame
        options_frame = tk.Frame(root, bg=self.OPTIONS_COLOR)
        options_frame.grid(row=0,
                           column=0,
                           padx=(self.WIDTH/70, self.WIDTH/70),
                           pady=(self.HEIGHT/40, self.HEIGHT/40),
                           stick="nsew")
        options_frame.grid_columnconfigure(0, weight=1)

        # Options Title
        options_title = tk.Label(options_frame,
                                 bg=self.OPTIONS_COLOR,
                                 text="Statistics Menu",
                                 font=(
                                     self.OPTIONS_FONT[0], self.OPTIONS_FONT[1], 'underline'),
                                 foreground=self.LIGHT_ACCENT)
        options_title.grid(row=0, column=0, padx=10, pady=20)

        # Command buttons
        for button in self.buttons:
            temp_button = tk.Button(options_frame,
                                    bg=self.BUTTON_COLOR,
                                    foreground=self.LIGHT_ACCENT,
                                    font=self.OPTIONS_FONT,
                                    text=button[1],
                                    command=button[2])
            temp_button.grid(row=button[0], column=0, pady=20)

        accuracy_frame = tk.Frame(options_frame, bg=self.MENU_COLOR)
        accuracy_frame.grid(row=2,
                            column=0,
                            padx=(self.WIDTH/70, self.WIDTH/70),
                            pady=(self.HEIGHT/40, self.HEIGHT/20),
                            stick="nsew")
        accuracy_frame.grid_columnconfigure(0, weight=1)

        accuracy_title = tk.Label(accuracy_frame,
                                  bg=self.MENU_COLOR,
                                  text="Accuracy Test Breakdown",
                                  font=(
                                      self.OPTIONS_FONT[0], self.OPTIONS_FONT[1], 'underline'),
                                  foreground=self.LIGHT_ACCENT)
        accuracy_title.grid(row=0, column=0)

        self.accuracy_text = tk.Text(accuracy_frame,
                                     bg=self.MENU_COLOR,
                                     foreground=self.LIGHT_ACCENT,
                                     borderwidth=0,
                                     highlightthickness=0,
                                     font=(
                                         self.OPTIONS_FONT[0], self.OPTIONS_FONT[1]),
                                     width=5)
        self.accuracy_text.grid(row=1, column=0, sticky='nsew')
        self.accuracy_text.configure(state='disabled')

        # =====================================================================#
        # Display Frame
        display_frame = tk.Frame(root, bg=self.MENU_COLOR)
        display_frame.grid(row=0,
                           column=1,
                           padx=(self.WIDTH/40, self.WIDTH/40),
                           pady=(self.HEIGHT/40, self.HEIGHT/20),
                           stick="nsew")

        # Frame that holds Sudoku puzzle
        puzzle_frame = tk.Frame(display_frame)
        puzzle_frame.place(in_=display_frame,
                           relx=0.5,
                           rely=0.5,
                           anchor='c'
                           )

        # Create Sudoku Frame
        # Create Frame Quadrants
        for box_row in range(3):
            for box_col in range(3):
                box_cell = tk.Frame(puzzle_frame,
                                    borderwidth=7,
                                    relief='flat',
                                    highlightcolor=self.LIGHT_ACCENT,
                                    bg=self.DISPLAY_COLOR,
                                    width=int(0.15 * self.WIDTH),
                                    height=int(0.15 * self.WIDTH))
                box_cell.grid(row=box_row, column=box_col)

                # Create and Fill Quadrant Cells
                for cell_row in range(3):
                    for cell_col in range(3):
                        cell = tk.Frame(box_cell,
                                        bg=self.MENU_COLOR,
                                        highlightbackground=self.LIGHT_ACCENT,
                                        highlightcolor=self.LIGHT_ACCENT,
                                        highlightthickness=2,
                                        width=self.WIDTH/20,
                                        height=self.WIDTH/20,
                                        padx=3,
                                        pady=3)
                        cell.grid(row=cell_row, column=cell_col)

                        self.cells[(3*box_row + cell_row, 3 *
                                    box_col + cell_col)] = cell

    def clear_board(self):
        for row in range(9):
            for col in range(9):
                GUI.color_cell(self, row, col, self.MENU_COLOR)

    def display_puzzle(self, puzzle):
        """updates the puzzle displayed in the puzzle side of the application."""
        for row in range(9):
            for col in range(9):
                for wdg in self.cells[(row, col)].winfo_children():
                    wdg.destroy()
                temp = tk.Label(self.cells[(row, col)],
                                # bg=self.cells[(row, col)].cget('bg'),
                                bg=self.MENU_COLOR,
                                foreground=self.LIGHT_ACCENT,
                                font=self.PUZZLE_FONT)

                if str(puzzle[row][col]) == '0':
                    temp.config(text=' ')
                else:
                    temp.config(text=str(puzzle[row][col]))
                temp.place(in_=self.cells[(row, col)],
                           relx=0.5,
                           rely=0.5,
                           anchor='c')

    def color_cell(self, row, col, color):
        """Updates the cell placed at the coordinates by the given color."""
        # Changes cell bg to specified color
        cell = self.cells[(row, col)]
        cell.configure(bg=color)
        for wdg in cell.winfo_children():
            wdg.configure(bg=color)

    def display_puzzle_discrepancy(self, prediction, solution):
        """Displays the accuracy of the puzzle and colours the cells based on accuracy."""
        error_count = 0
        for row in range(9):
            for col in range(9):
                if prediction[row][col] != solution[row][col]:
                    GUI.color_cell(self, row, col, 'red')
                    error_count += 1

        prediction_accuracy = round(((81 - error_count)/81) * 100, 2)
        self.accuracy_text.configure(state='normal')
        self.accuracy_text.insert(
            tk.INSERT, f"\n\t{settings.row_offset}: {81 - error_count} / 81 = {prediction_accuracy}%\n")
        settings.row_offset += 1
        self.accuracy_text.configure(state='disabled')
        self.accuracy_text.update()
        return prediction_accuracy

    def run_test(self):
        """Runs the sudoku network demo."""
        settings.row_offset = settings.training_offset + \
                    int(random.random() * ((settings.TOTAL_ROWS - settings.training_offset) - settings.read_in_amount))

        self.accuracy_text.configure(state='normal')
        self.accuracy_text.delete('1.0', tk.END)
        self.accuracy_text.insert(
            tk.INSERT, f"\nTesting: {settings.row_offset} - {settings.row_offset + settings.read_in_amount}")
        self.accuracy_text.configure(state='disabled')

        test_data = sudoku_parser.create_sudoku_list()
        test_puzzle = test_data[0]
        test_solutions = test_data[1]
        accuracy_percentages = []

        network = Network((sudoku_dim, sudoku_dim, 1))
        network.model = tensorflow.keras.models.load_model("our_model2.h5")

        for i in range(read_in_amount):

            GUI.clear_board(self)

            GUI.display_puzzle(self, main.denormalize(test_puzzle[i]))

            self.root.update()

            time.sleep(2)

            prediction = main.solve_sudoku(
                test_puzzle[i], network.model)

            GUI.display_puzzle(self, prediction)

            self.root.update()

            print(test_solutions[i])
            print(prediction)

            accuracy_percentages.append(GUI.display_puzzle_discrepancy(
                self, prediction, test_solutions[i]))

            self.root.update()

            time.sleep(3)

        solved_count = 0
        for accuracy in accuracy_percentages:
            if accuracy == 100.0:
                solved_count += 1

        self.accuracy_text.configure(state='normal')
        self.accuracy_text.insert(
            tk.INSERT, f"\n\t Total Accuracy: {round(sum(accuracy_percentages) / len(accuracy_percentages) ,2)}%\n")
        self.accuracy_text.insert(
            tk.INSERT, f"\n\t Total Correctly Solved: {solved_count} / {len(accuracy_percentages)} = {round(solved_count / len(accuracy_percentages) ,2) * 100}%\n")
        self.accuracy_text.configure(state='disabled')
        self.accuracy_text.update()


root = tk.Tk()
GUI(root)
root.mainloop()
