import random
cells = (["M"]*39 + ["X"]*9 + ["S"] + ["G"] + ["D"]*3 + ["."]*91)
random.shuffle(cells)
# print(cells)
grid = [cells[i:i+12] for i in range (0,144,12)]
score = 28
# print(grid)

def check_boundaries(row, col):
    return row >=0 and row <=11 and col >=0 and col<=11

def is_valid(row, col):
    return check_boundaries(row, col) and grid[row][col] != "X"
    
def calculate_move(symbol):
    if (symbol=="M"):
        score-=5
    elif (symbol == "."):
        score-=1
    elif (symbol == "D"):
        score+=2

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
            
            neighbors.append(((new_row, new_col, {new_visited}), move_name))

    return neighbors
