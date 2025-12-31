import tkinter as tk
from game import Minesweeper
from constants import GRID_SIZE


class MinesweeperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")

        self.game = Minesweeper()
        self.buttons = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

        self._create_grid()

    def _create_grid(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                button = tk.Button(
                    self.root,
                    width=2,
                    height=1,
                    font=("Arial", 14),
                    command=lambda r=row, c=col: self.left_click(r, c)
                )
                button.bind("<Button-3>", lambda event, r=row, c=col: self.right_click(r, c))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def left_click(self, row, col):
        if self.game.game_over:
            return

        self.game.reveal(row, col)
        self.update_ui()

        if self.game.game_over:
            self.show_game_over()

    def right_click(self, row, col):
        cell = self.game.board[row][col]
        if cell.is_revealed:
            return

        cell.is_flagged = not cell.is_flagged
        self.update_ui()

    def update_ui(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = self.game.board[row][col]
                button = self.buttons[row][col]

                if cell.is_revealed:
                    if cell.is_mine:
                        button.config(text="💣", bg="red", relief=tk.SUNKEN)
                    else:
                        text = str(cell.adjacent_mines) if cell.adjacent_mines > 0 else ""
                        button.config(text=text, bg="lightgray", relief=tk.SUNKEN)

                elif cell.is_flagged:
                    button.config(text="🚩", fg="red")

                else:
                    button.config(text="", bg="SystemButtonFace", relief=tk.RAISED)

    def show_game_over(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = self.game.board[row][col]
                if cell.is_mine:
                    self.buttons[row][col].config(text="💣", bg="red")


if __name__ == "__main__":
    root = tk.Tk()
    MinesweeperGUI(root)
    root.mainloop()
