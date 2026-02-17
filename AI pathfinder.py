import tkinter as tk
from tkinter import ttk, messagebox
import time
import heapq

grid_size = 10  
cell_size = 50  
delay = 0.05    #animation delay (seconds)

color_empty = "white"
color_obstacle = "red"   #-1
color_start = "green"   #S
color_target = "blue"   #T
color_frontier = "orange" #nodes in queue/stack
color_path = "purple" #final path

moves = [
    (-1, 0),  # Up
    (0, 1),   # Right
    (1, 0),   # Bottom
    (1, 1),   # Bottom-Right 
    (0, -1),  # Left
    (-1, -1)  # Top-Left 
]

class Node:
    def __init__(self, r, c, parent=None, cost=0):
        self.r = r
        self.c = c
        self.parent = parent
        self.cost = cost

    def get_pos(self):
        return (self.r, self.c)

class PathfinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pathfinding App") 
        
        self.grid_data = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        self.rects = {} # Stores canvas rectangle IDs
        self.start_pos = None
        self.target_pos = None
        self.running = False
        self.visit_count = 0
        
        # UI Layout
        self.setup_ui()
        self.init_grid()

    def setup_ui(self):
        # Control Panel
        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

        tk.Label(control_frame, text="Algorithm:", font=("Arial", 12, "bold")).pack(pady=5)
        
        self.algo_var = tk.StringVar()
        self.algo_combo = ttk.Combobox(control_frame, textvariable=self.algo_var, state="readonly")
        self.algo_combo['values'] = ("BFS", "DFS", "UCS", "DLS", "IDDFS", "Bidirectional")
        self.algo_combo.current(0)
        self.algo_combo.pack(pady=5)

        tk.Button(control_frame, text="Set Start (S)", command=lambda: self.set_mode("S"), bg="#ddffdd").pack(fill=tk.X, pady=2)
        tk.Button(control_frame, text="Set Target (T)", command=lambda: self.set_mode("T"), bg="#ddddff").pack(fill=tk.X, pady=2)
        tk.Button(control_frame, text="Toggle Wall (-1)", command=lambda: self.set_mode("Wall"), bg="#ffdddd").pack(fill=tk.X, pady=2)
        
        tk.Frame(control_frame, height=10).pack() # Spacer

        tk.Frame(control_frame, height=10).pack() # Spacer

        self.run_btn = tk.Button(control_frame, text="RUN SEARCH", command=self.start_search, bg="black", fg="white", font=("Arial", 10, "bold"))
        self.run_btn.pack(fill=tk.X, pady=10)

        tk.Button(control_frame, text="Reset Grid", command=self.reset_grid).pack(fill=tk.X, pady=5)
        tk.Button(control_frame, text="Clear Path Only", command=self.clear_path).pack(fill=tk.X, pady=5)

        self.status_lbl = tk.Label(control_frame, text="Status: Ready", wraplength=150)
        self.status_lbl.pack(pady=20)

        self.mode = "Wall" # Default click mode

        # Canvas for Grid
        self.canvas = tk.Canvas(self.root, width=grid_size*cell_size, height=grid_size*cell_size, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_click) # Allow dragging to paint walls

    def init_grid(self):
        self.canvas.delete("all")
        self.rects = {}
        for r in range(grid_size):
            for c in range(grid_size):
                x1, y1 = c * cell_size, r * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color_empty, outline="black")
                self.rects[(r, c)] = rect
                # Draw text overlay for 0 or -1
                self.canvas.create_text(x1+cell_size/2, y1+cell_size/2, text="0", tag=f"text_{r}_{c}", fill="#ddd")

    def set_mode(self, mode):
        self.mode = mode
        self.status_lbl.config(text=f"Mode: {mode}")

    def on_click(self, event):
        if self.running: 
            return
        c, r = event.x // cell_size, event.y // cell_size
        if 0 <= r < grid_size and 0 <= c < grid_size:
            self.handle_cell_update(r, c)

    def handle_cell_update(self, r, c):
        if self.mode == "S":
            # Clear old start
            if self.start_pos:
                self.update_visual(self.start_pos[0], self.start_pos[1], color_empty, "0")
                self.grid_data[self.start_pos[0]][self.start_pos[1]] = 0
            self.start_pos = (r, c)
            self.update_visual(r, c, color_start, "S")
            self.grid_data[r][c] = 0 

        elif self.mode == "T":
            # Clear old target
            if self.target_pos:
                self.update_visual(self.target_pos[0], self.target_pos[1], color_empty, "0")
                self.grid_data[self.target_pos[0]][self.target_pos[1]] = 0
            self.target_pos = (r, c)
            self.update_visual(r, c, color_target, "T")
            self.grid_data[r][c] = 0 

        elif self.mode == "Wall":
            # Don't overwrite S or T
            if (r, c) == self.start_pos or (r, c) == self.target_pos: 
                return
            
            # Toggle
            if self.grid_data[r][c] == -1:
                self.grid_data[r][c] = 0
                self.update_visual(r, c, color_empty, "0")
            else:
                self.grid_data[r][c] = -1
                self.update_visual(r, c, color_obstacle, "-1")

    def update_visual(self, r, c, color, text=None):
        self.canvas.itemconfig(self.rects[(r, c)], fill=color)
        if text:
            self.canvas.itemconfigure(f"text_{r}_{c}", text=text)
            if color == color_obstacle:
                self.canvas.itemconfigure(f"text_{r}_{c}", fill="white")
            else:
                self.canvas.itemconfigure(f"text_{r}_{c}", fill="black")

    def reset_grid(self):
        self.running = False
        self.grid_data = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        self.start_pos = None
        self.target_pos = None
        self.init_grid()
        self.status_lbl.config(text="Grid Reset")

    def clear_path(self):
        self.visit_count = 0
        # Clears visualization but keeps walls, S, and T
        for r in range(grid_size):
            for c in range(grid_size):
                if self.grid_data[r][c] == -1:
                    continue
                color = color_empty
                text = "0"
                if (r,c) == self.start_pos: 
                    color = color_start
                    text = "S"
                elif (r,c) == self.target_pos: 
                    color = color_target
                    text = "T"
                
                self.update_visual(r, c, color, text)

    def get_neighbors(self, node):
        neighbors = []
        for dr, dc in moves:
            nr, nc = node.r + dr, node.c + dc
            
            # Check bounds
            if 0 <= nr < grid_size and 0 <= nc < grid_size:
                # Check Obstacles 
                if self.grid_data[nr][nc] != -1:
                    neighbors.append(Node(nr, nc, node, node.cost + 1))
        return neighbors

    def start_search(self):
        if not self.start_pos or not self.target_pos:
            messagebox.showerror("Error", "Please place both Start (S) and Target (T)")
            return
        
        self.clear_path()
        self.running = True
        self.visit_count = 0
        self.status_lbl.config(text="Searching...")
        algo = self.algo_var.get()
        
        found_node = None
        depth = None
        if algo == "BFS":
            found_node = self.bfs()
        elif algo == "DFS":
            found_node = self.dfs()
        elif algo == "UCS":
            found_node = self.ucs()
        elif algo == "DLS":
            found_node = self.dls(limit=10) 
        elif algo == "IDDFS":
            depth, found_node = self.iddfs()
        elif algo == "Bidirectional":
            found_node = self.bidirectional()

        if found_node:
            self.reconstruct_path(found_node)
            if depth is not None:
                self.status_lbl.config(text=f"Target Found! Depth: {depth}")
            else:
                self.status_lbl.config(text="Target Found!")
        elif self.running: 
            self.status_lbl.config(text="No Path Found.")
        
        self.running = False

    def step_visualization(self, current_node, is_frontier=False):
        if not self.running: 
            return
        r, c = current_node.r, current_node.c
        
        # Don't recolor Start or Target
        if (r, c) == self.start_pos or (r, c) == self.target_pos:
            return
        
        color = color_frontier
        text=None
        if not is_frontier:
            self.visit_count += 1
            text = str(self.visit_count)
            
        self.update_visual(r, c, color, text)
        self.root.update()
        time.sleep(delay)