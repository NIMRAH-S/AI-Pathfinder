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


# Minahil part
def bfs(self):
        start_node = Node(self.start_pos[0], self.start_pos[1])
        q = [start_node]    
        visited = {self.start_pos}
        while q and self.running:
            curr = q.pop(0)

            if (curr.r, curr.c) == self.target_pos:
                return curr
            
            self.step_visualization(curr)

            for neighbor in self.get_neighbors(curr):
                pos = (neighbor.r, neighbor.c)
                if pos not in visited:
                    visited.add(pos)
                    q.append(neighbor)      
        return None

    def dfs(self):
        start_node = Node(self.start_pos[0], self.start_pos[1])
        stack = [start_node]
        visited = set()

        while stack and self.running:
            curr = stack.pop()
            
            if (curr.r, curr.c) == self.target_pos:
                return curr
            
            pos = (curr.r, curr.c)
            if pos in visited: 
                continue
            visited.add(pos)

            self.step_visualization(curr)

            neighbors = self.get_neighbors(curr)
            for neighbor in reversed(neighbors):
                if (neighbor.r, neighbor.c) not in visited:
                    stack.append(neighbor)
                    # self.step_visualization(neighbor, is_frontier=True)
        return None

    def ucs(self):
        pq = []   
        start_node = Node(self.start_pos[0], self.start_pos[1], cost=0)
        # using id(node) ensures we never compare node objects directly if costs are equal
        heapq.heappush(pq, (0, id(start_node), start_node))
        visited = {}
        while pq and self.running:
            cost, _, curr = heapq.heappop(pq)

            if (curr.r, curr.c) == self.target_pos:
                return curr

            pos = (curr.r, curr.c)
            if pos in visited and visited[pos] <= cost:
                continue
            visited[pos] = cost

            self.step_visualization(curr)

            for neighbor in self.get_neighbors(curr):
                new_cost = cost + 1 
                if (neighbor.r, neighbor.c) not in visited or new_cost < visited.get((neighbor.r, neighbor.c), float('inf')):
                    heapq.heappush(pq, (new_cost, id(neighbor), neighbor))
                    # self.step_visualization(neighbor, is_frontier=True)          
        return None

    def dls(self, limit):
        return self._dls_recursive(Node(self.start_pos[0], self.start_pos[1]), limit, set())

    def _dls_recursive(self, curr, limit, visited):
        if not self.running: 
            return None

        if (curr.r, curr.c) == self.target_pos:
            return curr
        
        if limit <= 0:
            return None

        visited.add((curr.r, curr.c))
        self.step_visualization(curr)

        for neighbor in self.get_neighbors(curr):
            if (neighbor.r, neighbor.c) not in visited:
                result = self._dls_recursive(neighbor, limit-1, visited)
                if result: 
                    return result
        return None

    def iddfs(self):
        depth = 0
        while self.running:
            self.status_lbl.config(text=f"IDDFS Depth: {depth}")
            self.clear_path() 
            result = self.dls(depth)
            if result:
                return depth, result
            depth += 1
            if depth > grid_size * grid_size: # Safety break
                break
        return None

    def bidirectional(self):
        # Forward Search
        start_node = Node(self.start_pos[0], self.start_pos[1])
        q1 = [start_node]
        visited1 = {self.start_pos: start_node}

        # Backward Search
        target_node = Node(self.target_pos[0], self.target_pos[1])
        q2 = [target_node]
        visited2 = {self.target_pos: target_node}

        while q1 and q2 and self.running:
            # Expand Forward
            if q1:
                curr_f = q1.pop(0)
                self.step_visualization(curr_f)
                
                if (curr_f.r, curr_f.c) in visited2:
                    return self.merge_paths(curr_f, visited2[(curr_f.r, curr_f.c)])

                for n in self.get_neighbors(curr_f):
                    pos = (n.r, n.c)
                    if pos not in visited1:
                        visited1[pos] = n
                        q1.append(n)
                        # self.step_visualization(n, is_frontier=True)

            # Expand Backward
            if q2:
                curr_b = q2.pop(0)
                self.step_visualization(curr_b)

                if (curr_b.r, curr_b.c) in visited1:
                    return self.merge_paths(visited1[(curr_b.r, curr_b.c)], curr_b)

                for n in self.get_neighbors(curr_b):
                    pos = (n.r, n.c)
                    if pos not in visited2:
                        visited2[pos] = n
                        q2.append(n)
                        # self.step_visualization(n, is_frontier=True)
                curr_f = q1.pop(0)
                self.step_visualization(curr_f)
                
                if (curr_f.r, curr_f.c) in visited2:
                    return self.merge_paths(curr_f, visited2[(curr_f.r, curr_f.c)])

                for n in self.get_neighbors(curr_f):
                    pos = (n.r, n.c)
                    if pos not in visited1:
                        visited1[pos] = n
                        q1.append(n)
                        # self.step_visualization(n, is_frontier=True)

            # Expand Backward
            if not q2:
                break
            curr_b = q2.pop(0)
            self.step_visualization(curr_b)

            if (curr_b.r, curr_b.c) in visited1:
                return self.merge_paths(visited1[(curr_b.r, curr_b.c)], curr_b)

            for n in self.get_neighbors(curr_b):
                pos = (n.r, n.c)
                if pos not in visited2:
                    visited2[pos] = n
                    q2.append(n)
                    # self.step_visualization(n, is_frontier=True)
        return None

    def merge_paths(self, node_f, node_b):
        # reconstruct path from start to meeting point
        path_nodes = []
        curr = node_f
        while curr:
            path_nodes.append(curr)
            curr = curr.parent
        path_nodes.reverse()

        # reconstruct path from meeting point to target
        curr = node_b.parent 
        while curr:
            path_nodes.append(curr)
            curr = curr.parent
        
        # visualize merged path
        for n in path_nodes:
            if (n.r, n.c) != self.start_pos and (n.r, n.c) != self.target_pos:
                self.update_visual(n.r, n.c, color_path)
        return node_f 

    def reconstruct_path(self, node):
        curr = node
        path = []
        while curr:
            path.append((curr.r, curr.c))
            curr = curr.parent
        
        for r, c in path:
            if (r, c) != self.start_pos and (r, c) != self.target_pos:
                self.update_visual(r, c, color_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = PathfinderApp(root)
    root.mainloop()