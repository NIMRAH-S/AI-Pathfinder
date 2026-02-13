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

# person 2
# ─────────────────────────────────────────────
#  UCS (Uniform Cost Search)
# ─────────────────────────────────────────────
def ucs(grid_orig, start, target, viz):
    grid = grid_orig.copy()
    heap = [(0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    explored_count = 0
    step = 0

    while heap:
        try_spawn_dynamic(grid, start, target)

        cost, node = heapq.heappop(heap)
        r, c = node

        if grid[r][c] not in (START, TARGET, WALL, DYN_WALL):
            grid[r][c] = EXPLORED
        explored_count += 1
        step += 1

        if node == target:
            path = reconstruct_path(came_from, start, target)
            viz.final(grid, path,
                      f"UCS | Steps: {step} | Explored: {explored_count} | Cost: {cost:.2f} | Path: {len(path)}")
            return path

        for nb in get_neighbors(grid, node):
            nr, nc = nb
            if grid[nr][nc] == DYN_WALL:
                continue

            dr = abs(nr - r)
            dc = abs(nc - c)
            move_cost = 1.414 if (dr == 1 and dc == 1) else 1.0
            new_cost = cost + move_cost

            if nb not in cost_so_far or new_cost < cost_so_far[nb]:
                cost_so_far[nb] = new_cost
                came_from[nb] = node
                heapq.heappush(heap, (new_cost, nb))
                if grid[nr][nc] not in (START, TARGET):
                    grid[nr][nc] = FRONTIER

        if step % 2 == 0:
            viz.draw(grid, f"UCS | Step {step} | Cost so far: {cost:.2f}")

    viz.draw(grid, "UCS | No path found!")
    plt.ioff(); plt.show(block=True)
    return []


# ─────────────────────────────────────────────
#  DLS (Depth-Limited Search)
# ─────────────────────────────────────────────
def dls(grid_orig, start, target, viz, limit=DLS_LIMIT):
    grid = grid_orig.copy()
    stack = [(start, 0, [start])]
    visited = set()
    step = 0

    while stack:
        try_spawn_dynamic(grid, start, target)

        node, depth, path_so_far = stack.pop()
        r, c = node

        if node in visited:
            continue
        visited.add(node)

        if grid[r][c] not in (START, TARGET, WALL, DYN_WALL):
            grid[r][c] = EXPLORED
        step += 1

        if node == target:
            viz.final(grid, path_so_far,
                      f"DLS (limit={limit}) | Steps: {step} | Path: {len(path_so_far)}")
            return path_so_far

        if depth < limit:
            for nb in get_neighbors(grid, node):
                nr, nc = nb
                if nb not in visited and grid[nr][nc] != DYN_WALL:
                    stack.append((nb, depth+1, path_so_far + [nb]))
                    if grid[nr][nc] not in (START, TARGET):
                        grid[nr][nc] = FRONTIER

        if step % 2 == 0:
            viz.draw(grid,
                     f"DLS | Step {step} | Depth limit: {limit} | Current depth: {depth}")

    viz.draw(grid, f"DLS | No path within depth {limit}!")
    plt.ioff(); plt.show(block=True)
    return []


# ─────────────────────────────────────────────
#  IDDFS (Iterative Deepening DFS)
# ─────────────────────────────────────────────
def iddfs(grid_orig, start, target, viz):
    grid = grid_orig.copy()
    step = 0
    max_depth = GRID_ROWS * GRID_COLS

    for limit in range(0, max_depth):
        g_iter = grid.copy()
        stack = [(start, 0, [start])]
        visited = {}

        while stack:
            try_spawn_dynamic(grid, start, target)

            node, depth, path_so_far = stack.pop()
            r, c = node

            if node in visited and visited[node] <= depth:
                continue
            visited[node] = depth

            if g_iter[r][c] not in (START, TARGET, WALL, DYN_WALL):
                g_iter[r][c] = EXPLORED
            step += 1

            if node == target:
                viz.final(g_iter, path_so_far,
                          f"IDDFS | Limit reached: {limit} | Steps: {step} | Path: {len(path_so_far)}")
                return path_so_far

            if depth < limit:
                for nb in get_neighbors(g_iter, node):
                    nr, nc = nb
                    if (nb not in visited or visited[nb] > depth+1) and g_iter[nr][nc] != DYN_WALL:
                        stack.append((nb, depth+1, path_so_far + [nb]))
                        if g_iter[nr][nc] not in (START, TARGET):
                            g_iter[nr][nc] = FRONTIER

            if step % 3 == 0:
                viz.draw(g_iter,
                         f"IDDFS | Iteration (limit={limit}) | Step {step}")

    viz.draw(grid, "IDDFS | No path found!")
    plt.ioff(); plt.show(block=True)
    return []


# ─────────────────────────────────────────────
#  BIDIRECTIONAL SEARCH
# ─────────────────────────────────────────────
def bidirectional(grid_orig, start, target, viz):
    grid = grid_orig.copy()

    front_q = deque([start])
    back_q = deque([target])
    front_came = {start: None}
    back_came = {target: None}
    step = 0

    def build_full_path(meet):
        fwd = []
        n = meet
        while n is not None:
            fwd.append(n)
            n = front_came[n]
        fwd.reverse()

        bwd = []
        n = back_came[meet]
        while n is not None:
            bwd.append(n)
            n = back_came[n]
        return fwd + bwd

    while front_q and back_q:
        try_spawn_dynamic(grid, start, target)
        step += 1

        if front_q:
            node = front_q.popleft()
            if node in back_came:
                path = build_full_path(node)
                viz.final(grid, path,
                          f"Bidirectional | Steps: {step} | Path: {len(path)}")
                return path

            for nb in get_neighbors(grid, node):
                if nb not in front_came:
                    front_came[nb] = node
                    front_q.append(nb)

        if back_q:
            node = back_q.popleft()
            if node in front_came:
                path = build_full_path(node)
                viz.final(grid, path,
                          f"Bidirectional | Steps: {step} | Path: {len(path)}")
                return path

            for nb in get_neighbors(grid, node):
                if nb not in back_came:
                    back_came[nb] = node
                    back_q.append(nb)

        if step % 2 == 0:
            viz.draw(grid,
                     f"Bidirectional | Step {step} | Fwd: {len(front_q)} | Bwd: {len(back_q)}")

    viz.draw(grid, "Bidirectional | No path found!")
    plt.ioff(); plt.show(block=True)
    return []
