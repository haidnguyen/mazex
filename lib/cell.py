from lib.line import Line
from lib.point import Point
from lib.window import Window
from dataclasses import dataclass


@dataclass
class Cell:
    win: Window
    x1: int
    y1: int
    x2: int
    y2: int
    has_left_wall: bool
    has_right_wall: bool
    has_top_wall: bool
    has_bottom_wall: bool
    visited: bool = False

    def draw(self):
        topLeft = Point(x=self.x1, y=self.y1)
        topRight = Point(x=self.x2, y=self.y1)
        bottomRight = Point(x=self.x2, y=self.y2)
        bottomLeft = Point(x=self.x1, y=self.y2)

        if self.has_left_wall:
            self.win.draw_line(Line(start=topLeft, end=bottomLeft), fill_color="black")
        else:
            self.win.draw_line(Line(start=topLeft, end=bottomLeft), fill_color="white")

        if self.has_right_wall:
            self.win.draw_line(
                Line(start=topRight, end=bottomRight), fill_color="black"
            )
        else:
            self.win.draw_line(
                Line(start=topRight, end=bottomRight), fill_color="white"
            )

        if self.has_top_wall:
            self.win.draw_line(Line(start=topLeft, end=topRight), fill_color="black")
        else:
            self.win.draw_line(Line(start=topLeft, end=topRight), fill_color="white")

        if self.has_bottom_wall:
            self.win.draw_line(
                Line(start=bottomLeft, end=bottomRight), fill_color="black"
            )
        else:
            self.win.draw_line(
                Line(start=bottomLeft, end=bottomRight), fill_color="white"
            )

    def draw_move(self, to_cell: "Cell", undo=False):
        center = Point(x=(self.x1 + self.x2) // 2, y=(self.y1 + self.y2) // 2)
        to_cell_center = Point(
            (to_cell.x1 + to_cell.x2) // 2, (to_cell.y1 + to_cell.y2) // 2
        )
        path = Line(start=center, end=to_cell_center)

        self.win.draw_line(path, fill_color="gray" if undo else "red")
