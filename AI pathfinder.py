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

# Minahil part
class Visualizer:
    def __init__(self, algo_name):
        self.algo_name = algo_name
        plt.ion()
        self.fig = plt.figure(figsize=(10, 9))
        self.fig.canvas.manager.set_window_title("GOOD PERFORMANCE TIME APP")
        self.fig.patch.set_facecolor("#1A202C")
        gs = gridspec.GridSpec(2, 1, height_ratios=[14,1], hspace=0.08)
        self.ax = self.fig.add_subplot(gs[0])
        self.ax2 = self.fig.add_subplot(gs[1])
        self.ax2.axis('off')
        self.ax.set_facecolor("#1A202C")
        self.ax.set_title(f"GOOD PERFORMANCE TIME APP — {algo_name}", color="white", fontsize=13, fontweight='bold', pad=10)
        self.ax.tick_params(colors='#4A5568')
        for spine in self.ax.spines.values():
            spine.set_edgecolor('#4A5568')

        # legend
        legend_patches = [
            mpatches.Patch(color="#22C55E", label="Start"),
            mpatches.Patch(color="#EF4444", label="Target"),
            mpatches.Patch(color="#60A5FA", label="Frontier"),
            mpatches.Patch(color="#BFDBFE", label="Explored"),
            mpatches.Patch(color="#FBBF24", label="Final Path"),
            mpatches.Patch(color="#2D3748", label="Wall"),
            mpatches.Patch(color="#F97316", label="Dynamic Wall"),
        ]
        self.ax.legend(handles=legend_patches, loc='upper right', fontsize=7, facecolor='#2D3748', labelcolor='white', framealpha=0.9, ncol=2)

        self.img = None
        self.status_text = self.ax2.text(0.5, 0.5, "", ha='center', va='center', color='white', fontsize=10, transform=self.ax2.transAxes)

    def _to_display(self, grid):
        """Map grid values to colormap indices (wall -1 → 1)."""
        d = grid.copy().astype(float)
        d[d == WALL] = 1
        return d

    def draw(self, grid, status=""):
        d = self._to_display(grid)
        if self.img is None:
            self.img = self.ax.imshow(d, cmap=cmap, vmin=0, vmax=7, interpolation='nearest', aspect='equal')
            # grid lines
            rows, cols = grid.shape
            for x in range(cols+1):
                self.ax.axvline(x-0.5, color='#4A5568', linewidth=0.4)
            for y in range(rows+1):
                self.ax.axhline(y-0.5, color='#4A5568', linewidth=0.4)
            self.ax.set_xticks(range(cols))
            self.ax.set_yticks(range(rows))
            self.ax.set_xticklabels(range(cols), color='#718096', fontsize=6)
            self.ax.set_yticklabels(range(rows), color='#718096', fontsize=6)
        else:
            self.img.set_data(d)
        self.status_text.set_text(status)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()
        time.sleep(STEP_DELAY)

    def final(self, grid, path, stats):
        # Draw final path
        g = grid.copy()
        for r,c in path:
            if g[r][c] not in (START, TARGET):
                g[r][c] = PATH
        self.draw(g, stats)
        plt.ioff()
        plt.show(block=True)
