from collections import deque
import random
cells = (["M"]*39 + ["X"]*9 + ["S"] + ["G"] + ["D"]*3 + ["."]*91)
random.shuffle(cells)
grid = [cells[i:i+12] for i in range (0,144,12)]

def print_grid():
    for row in grid:
        print(" ".join(row))
    print()

def check_boundaries(row, col):
    return row >=0 and row <=11 and col >=0 and col<=11

def is_valid(row, col):
    return check_boundaries(row, col) and grid[row][col] != "X"
    
def find_position():
    start = None
    goal = None
    destinations = []

    for r in range(12):
        for c in range(12):
            if grid[r][c] == "S":
                start = (r,c)
            elif grid[r][c] == "G":
                goal = (r,c)
            elif grid[r][c] == "D":
                destinations.append((r,c))
    return start, goal, destinations

def get_neighbors(state, all_destinations):
    neighbors = []
    row, col, visited_destinations  = state
    moves = {
        "UP" : (-1,0),
        "DOWN" : (1,0),
        "RIGHT" : (0,1),
        "LEFT" : (0,-1)
    }

    for move_name, (dr,dc) in moves.items():
        new_row = row + dr
        new_col = col +dc
        
        if (is_valid(new_row, new_col)):
            new_visited = visited_destinations

            if (grid[new_row][new_col]== "D"):
                new_visited = visited_destinations | {(new_row, new_col)}

            if (grid[new_row][new_col]=="G"):
                if(len(new_visited) != len(all_destinations)):
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

def print_solution(solution):
    for state, move in solution:
        row, col, visited_D = state

        print("Move:", move if move else "START")
        print("Position:", (row, col))
        print("Visited Destinations:", visited_D)
        print()

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

print("Generated Grid:\n")
print_grid()

start, goal, destinations = find_position()

print("Start:", start)
print("Goal:", goal)
print("Destinations:", destinations)
print("\n================ BFS ================\n")

bfs_solution = bfs(start, goal, destinations)

if bfs_solution:
    print_solution(bfs_solution)
else:
    print("No BFS solution found.")

print("\n================ DFS ================\n")

dfs_solution = dfs(start, goal, destinations)

if dfs_solution:
    print_solution(dfs_solution)
else:
    print("No DFS solution found.")