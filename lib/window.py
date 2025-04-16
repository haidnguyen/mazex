from tkinter import Tk, Canvas

from lib.line import Line


class Window:
    def __init__(self, width: int, height: int):
        self.root = Tk()
        self.root.title("Game")
        self.canvas = Canvas(self.root, width=width, height=height, background="white")
        self.canvas.pack()
        self.is_running = False

        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self.root.update_idletasks()
        self.root.update()

    def wait_for_close(self):
        self.is_running = True
        while self.is_running:
            self.redraw()

    def draw_line(self, line: Line, fill_color: str):
        line.draw(self.canvas, fill_color)

    def close(self):
        self.is_running = False
