from lib.cell import Cell
from lib.window import Window
import time
import random


class Maze:
    def __init__(
        self,
        x1: int,
        y1: int,
        num_rows: int,
        num_cols: int,
        cel_size_x: int,
        cel_size_y: int,
        win: Window | None = None,
        seed: int | None = None,
    ):
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cel_size_x = cel_size_x
        self.cel_size_y = cel_size_y
        self.win = win
        self._cells: list[list[Cell]] = []
        if seed is not None:
            self.seed = random.seed(seed)

        self._create_cells()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        for col in range(self.num_cols):
            self._cells.append([])
            for row in range(self.num_rows):
                cell = Cell(
                    win=self.win,
                    x1=self.x1 + col * self.cel_size_x,
                    y1=self.y1 + row * self.cel_size_y,
                    x2=self.x1 + (col * self.cel_size_x) + self.cel_size_x,
                    y2=self.y1 + (row * self.cel_size_y) + self.cel_size_y,
                    has_left_wall=True,
                    has_right_wall=True,
                    has_top_wall=True,
                    has_bottom_wall=True,
                )
                self._cells[col].append(cell)
                self._draw_cell(col, row)

        self._break_entrance_and_exit()

    def _draw_cell(self, col, row):
        cell = self._cells[col][row]
        if self.win and cell:
            cell.draw()
            self._animate()

    def _break_entrance_and_exit(self):
        entrance_cell = self._cells[0][0]
        entrance_cell.has_top_wall = False
        self._draw_cell(0, 0)

        exit_cell = self._cells[self.num_cols - 1][self.num_rows - 1]
        exit_cell.has_bottom_wall = False
        self._draw_cell(self.num_cols - 1, self.num_rows - 1)

    def _break_walls_r(self, i: int, j: int):
        current_cell = self._cells[i][j]
        current_cell.visited = True
        while True:
            to_visit: list[tuple[int, int]] = [
                (i - 1, j),
                (i, j - 1),
                (i + 1, j),
                (i, j + 1),
            ]
            adjacent_unvisited_cells = [
                (x, y, self._cells[x][y])
                for (x, y) in to_visit
                if x >= 0
                and y >= 0
                and x < self.num_cols
                and y < self.num_rows
                and not self._cells[x][y].visited
            ]
            if len(adjacent_unvisited_cells) == 0:
                current_cell.draw()
                return
            rand_direction = random.randrange(0, len(adjacent_unvisited_cells), 1)
            x, y, chosen_cell = adjacent_unvisited_cells[rand_direction]
            if x == i - 1:
                current_cell.has_left_wall = False
                chosen_cell.has_right_wall = False
            elif x == i + 1:
                current_cell.has_right_wall = False
                chosen_cell.has_left_wall = False
            elif y == j + 1:
                current_cell.has_bottom_wall = False
                chosen_cell.has_top_wall = False
            elif y == j - 1:
                current_cell.has_top_wall = False
                chosen_cell.has_bottom_wall = False
            self._break_walls_r(x, y)

    def _animate(self):
        self.win.redraw()
        time.sleep(0.05)

    def _reset_cells_visited(self):
        for cell_row in self._cells:
            for cell in cell_row:
                cell.visited = False

    def _solve_r(self, i: int, j: int):
        self._animate()
        current_cell = self._cells[i][j]
        current_cell.visited = True
        if i == self.num_cols - 1 and j == self.num_rows - 1:
            return True

        directions = [(i - 1, j), (i, j - 1), (i + 1, j), (i, j + 1)]
        for idx, (x, y) in enumerate(directions):
            if x < self.num_cols and y < self.num_rows and x >= 0 and y >= 0:
                cell = self._cells[x][y]
                if idx == 0 and not cell.has_right_wall and not cell.visited:
                    current_cell.draw_move(cell)
                    if self._solve_r(x, y):
                        return True
                    else:
                        cell.draw_move(current_cell, undo=True)
                if idx == 1 and not cell.has_bottom_wall and not cell.visited:
                    current_cell.draw_move(cell)
                    if self._solve_r(x, y):
                        return True
                    else:
                        cell.draw_move(current_cell, undo=True)
                if idx == 2 and not cell.has_left_wall and not cell.visited:
                    current_cell.draw_move(cell)
                    if self._solve_r(x, y):
                        return True
                    else:
                        cell.draw_move(current_cell, undo=True)
                if idx == 3 and not cell.has_top_wall and not cell.visited:
                    current_cell.draw_move(cell)
                    if self._solve_r(x, y):
                        return True
                    else:
                        cell.draw_move(current_cell, undo=True)
        return False

    def solve(self):
        self._solve_r(0, 0)
