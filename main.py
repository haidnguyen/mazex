from lib.maze import Maze
from lib.window import Window


def main():
    # cell.draw_move(cell2)

    win = Window(width=800, height=600)
    _maze = Maze(
        x1=100, y1=100, num_rows=15, num_cols=15, cel_size_x=25, cel_size_y=25, win=win
    )

    _maze.solve()

    win.wait_for_close()


if __name__ == "__main__":
    main()
