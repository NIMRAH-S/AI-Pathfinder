# GRID CONFIGURATION
GRID_ROWS = 15
GRID_COLS = 15
WALL_RATIO = 0.20
DYNAMIC_PROB = 0.03
DLS_LIMIT = 8
STEP_DELAY = 0.06

EMPTY  = 0
WALL   = -1
START  = 2
TARGET = 3
FRONTIER  = 4
EXPLORED  = 5
PATH      = 6
DYN_WALL  = 7

DIRECTIONS = [(-1,0),(0,1),(1,0),(1,1),(0,-1),(-1,-1),(-1,1),(1,-1)]

def make_grid(rows=GRID_ROWS, cols=GRID_COLS):
    grid = np.zeros((rows, cols), dtype=int)

    wall_count = int(rows * cols * WALL_RATIO)
    positions = [(r,c) for r in range(rows) for c in range(cols)]
    random.shuffle(positions)

    for i in range(wall_count):
        r,c = positions[i]
        grid[r][c] = WALL

    start = pick_empty(grid, rows, cols)
    target = pick_empty(grid, rows, cols, exclude={start})

    grid[start] = START
    grid[target] = TARGET

    return grid, start, target

def pick_empty(grid, rows, cols, exclude=set()):
    while True:
        r = random.randint(0, rows-1)
        c = random.randint(0, cols-1)
        if grid[r][c] == EMPTY and (r,c) not in exclude:
            return (r,c)

def get_neighbors(grid, node, rows=GRID_ROWS, cols=GRID_COLS):
    r,c = node
    neighbors = []

    for dr,dc in DIRECTIONS:
        nr,nc = r+dr, c+dc

        if 0 <= nr < rows and 0 <= nc < cols:
            if grid[nr][nc] != WALL and grid[nr][nc] != DYN_WALL:
                neighbors.append((nr,nc))

    return neighbors

def reconstruct_path(came_from, start, target):
    path = []
    node = target

    while node != start:
        path.append(node)
        node = came_from.get(node)

        if node is None:
            return []

    path.append(start)
    path.reverse()

    return path

def try_spawn_dynamic(grid, start, target):
    if random.random() < DYNAMIC_PROB:
        r = random.randint(0, GRID_ROWS-1)
        c = random.randint(0, GRID_COLS-1)

        if grid[r][c] == EMPTY:
            if (r,c) != start and (r,c) != target:
                grid[r][c] = DYN_WALL
                return (r,c)

    return None
