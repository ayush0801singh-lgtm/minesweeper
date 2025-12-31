import tkinter as tk
from game import Minesweeper
from constants import GRID_SIZE


class MinesweeperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")

        self.game = Minesweeper()
        self.buttons = [[None for _ in range(GRID_SIZE)]
                        for _ in range(GRID_SIZE)]

        self._create_grid()
        self._create_restart_button()

    def _create_grid(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                btn = tk.Button(
                    self.root,
                    width=2,
                    height=1,
                    font=("Arial", 14),
                    command=lambda r=r, c=c: self.left_click(r, c)
                )
                btn.bind("<Button-3>",
                         lambda e, r=r, c=c: self.right_click(r, c))
                btn.grid(row=r, column=c)
                self.buttons[r][c] = btn

    def _create_restart_button(self):
        restart_btn = tk.Button(
            self.root,
            text="Restart",
            font=("Arial", 12),
            command=self.restart_game
        )
        restart_btn.grid(
            row=GRID_SIZE,
            column=0,
            columnspan=GRID_SIZE,
            pady=5
        )

    def left_click(self, r, c):
        if self.game.game_over or self.game.win:
            return

        self.game.reveal(r, c)
        self.update_ui()

        if self.game.game_over:
            self.show_game_over()
        elif self.game.win:
            self.show_win()

    def right_click(self, r, c):
        cell = self.game.board[r][c]
        if cell.is_revealed:
            return

        cell.is_flagged = not cell.is_flagged
        self.update_ui()

    def update_ui(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                cell = self.game.board[r][c]
                btn = self.buttons[r][c]

                if cell.is_revealed:
                    if cell.is_mine:
                        btn.config(text="💣", bg="red", relief=tk.SUNKEN)
                    else:
                        text = str(cell.adjacent_mines) if cell.adjacent_mines else ""
                        btn.config(text=text, bg="lightgray", relief=tk.SUNKEN)

                elif cell.is_flagged:
                    btn.config(text="🚩", fg="red")

                else:
                    btn.config(text="", bg="SystemButtonFace",
                               relief=tk.RAISED, state="normal")

    def show_game_over(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                cell = self.game.board[r][c]
                if cell.is_mine:
                    self.buttons[r][c].config(text="💣", bg="red")
                self.buttons[r][c].config(state="disabled")

        self.root.title("Minesweeper - Game Over")

    def show_win(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                self.buttons[r][c].config(state="disabled")

        self.root.title("Minesweeper - You Win! 🎉")

    def restart_game(self):
        self.game = Minesweeper()
        self.root.title("Minesweeper")

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                self.buttons[r][c].config(
                    text="",
                    bg="SystemButtonFace",
                    relief=tk.RAISED,
                    state="normal"
                )


if __name__ == "__main__":
    root = tk.Tk()
    MinesweeperGUI(root)
    root.mainloop()
