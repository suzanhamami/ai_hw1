from collections import deque
import random
import sys


cells = (["M"]*39 + ["X"]*9 + ["S"] + ["G"] + ["D"]*3 + ["."]*91)
random.shuffle(cells)
grid = [cells[i:i+12] for i in range(0, 144, 12)]

def print_grid():
    for row in grid:
        print(" ".join(row))
    print()

def check_boundaries(row, col):
    return 0 <= row <= 11 and 0 <= col <= 11

def is_valid(row, col):
    return check_boundaries(row, col) and grid[row][col] != "X"

def find_position():
    start = None
    goal = None
    destinations = []
    for r in range(12):
        for c in range(12):
            if grid[r][c] == "S":
                start = (r, c)
            elif grid[r][c] == "G":
                goal = (r, c)
            elif grid[r][c] == "D":
                destinations.append((r, c))
    return start, goal, destinations


def get_neighbors(state, all_destinations):
    neighbors = []
    row, col, visited_destinations = state

    moves = {
        "UP": (-1, 0),
        "DOWN": (1, 0),
        "RIGHT": (0, 1),
        "LEFT": (0, -1)
    }

    for move_name, (dr, dc) in moves.items():
        new_row = row + dr
        new_col = col + dc

        if is_valid(new_row, new_col):
            new_visited = visited_destinations

            if grid[new_row][new_col] == "D":
                new_visited = visited_destinations | {(new_row, new_col)}

            if grid[new_row][new_col] == "G":
                if len(new_visited) != len(all_destinations):
                    continue

            new_state = (new_row, new_col, frozenset(new_visited))
            neighbors.append((new_state, move_name))

    return neighbors


def prepare_solution(path, steps_taken, state):
    solution = [(state, None)]
    while state in path:
        solution.append((path[state], steps_taken[state]))
        state = path[state]
    solution.reverse()
    return solution



def dfs(start, goal, destinations):
    start_state = (start[0], start[1], frozenset())
    stack = [start_state]
    visited = set([start_state])
    path = {}
    steps_taken = {}

    while stack:
        state = stack.pop()
        row, col, visited_D = state
        if (row, col) == goal and len(visited_D) == len(destinations):
            return prepare_solution(path, steps_taken, state)
        neighbors = get_neighbors(state, destinations)
        for n, move in neighbors:
            if n not in visited:
                visited.add(n)
                stack.append(n)
                path[n] = state
                steps_taken[n] = move
    return None

def bfs(start, goal, destinations):
    start_state = (start[0], start[1], frozenset())
    queue = deque([start_state])
    visited = set([start_state])
    path = {}
    steps_taken = {}

    while queue:
        state = queue.popleft()
        row, col, visited_D = state
        if (row, col) == goal and len(visited_D) == len(destinations):
            return prepare_solution(path, steps_taken, state)
        neighbors = get_neighbors(state, destinations)
        for n, move in neighbors:
            if n not in visited:
                visited.add(n)
                queue.append(n)
                path[n] = state
                steps_taken[n] = move
    return None


from PyQt6.QtWidgets import QApplication, QWidget
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush
from PyQt6.QtCore import QTimer, Qt

CELL_SIZE = 40
GRID_SIZE = 12
WINDOW_SIZE = CELL_SIZE * GRID_SIZE

COLOR_MAP = {
    "M": QColor(139, 69, 19),
    "X": QColor(0, 0, 0),
    ".": QColor(200, 200, 200),
    "D": QColor(0, 0, 255),
    "S": QColor(255, 0, 255),
    "G": QColor(0, 255, 0),
}

AGENT_COLOR = QColor(255, 255, 0)

class SimulationWindow(QWidget):
    def __init__(self, grid, solution, title):
        super().__init__()
        self.grid = grid
        self.solution = solution
        self.step_index = 0

        self.setWindowTitle(title)
        self.setFixedSize(WINDOW_SIZE, WINDOW_SIZE)

        self.timer = QTimer()
        self.timer.timeout.connect(self.next_step)
        self.timer.start(300)

    def next_step(self):
        if self.step_index < len(self.solution) - 1:
            self.step_index += 1
            self.update()
        else:
            self.timer.stop()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.GlobalColor.black, 1))

        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                cell = self.grid[r][c]
                color = COLOR_MAP.get(cell, QColor(255, 255, 255))
                painter.setBrush(QBrush(color))
                painter.drawRect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)

        state, _ = self.solution[self.step_index]
        row, col, _ = state

        painter.setBrush(QBrush(AGENT_COLOR))
        painter.drawEllipse(
            col * CELL_SIZE + 5,
            row * CELL_SIZE + 5,
            CELL_SIZE - 10,
            CELL_SIZE - 10
        )

def run_simulation(grid, solution, title):
    app = QApplication(sys.argv)
    window = SimulationWindow(grid, solution, title)
    window.show()
    app.exec()


print("Generated Grid:\n")
print_grid()

start, goal, destinations = find_position()

print("Start:", start)
print("Goal:", goal)
print("Destinations:", destinations)

bfs_solution = bfs(start, goal, destinations)
if bfs_solution:
    print("\nRunning BFS Simulation...")
    run_simulation(grid, bfs_solution, "BFS Simulation")
else:
    print("No BFS solution found.")

dfs_solution = dfs(start, goal, destinations)
if dfs_solution:
    print("\nRunning DFS Simulation...")
    run_simulation(grid, dfs_solution, "DFS Simulation")
else:
    print("No DFS solution found.")