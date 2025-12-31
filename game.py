import random
from cell import Cell
from constants import GRID_SIZE, MINES_COUNT


class Minesweeper:
    def __init__(self):
        self.game_over = False
        self.win = False
        self.board = [[Cell(r, c) for c in range(GRID_SIZE)]
                      for r in range(GRID_SIZE)]
        self._place_mines()
        self._calculate_adjacent_mines()

    def _place_mines(self):
        positions = random.sample(
            [(r, c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)],
            MINES_COUNT
        )

        for r, c in positions:
            self.board[r][c].is_mine = True

    def _calculate_adjacent_mines(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                if self.board[r][c].is_mine:
                    continue

                count = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                            if self.board[nr][nc].is_mine:
                                count += 1

                self.board[r][c].adjacent_mines = count

    def reveal(self, row, col):
        cell = self.board[row][col]

        if cell.is_revealed or cell.is_flagged:
            return

        cell.is_revealed = True

        if cell.is_mine:
            self.game_over = True
            return

        if cell.adjacent_mines == 0:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = row + dr, col + dc
                    if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                        self.reveal(nr, nc)

        if self.check_win():
            self.win = True

    def check_win(self):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                cell = self.board[row][col]
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True
