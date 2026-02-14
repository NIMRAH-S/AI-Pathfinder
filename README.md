# AI Pathfinder – Grid Search Visualizer
### AI 2002 – Artificial Intelligence (Spring 2026) | Assignment 1 – Question 7

> **GOOD PERFORMANCE TIME APP** — A step-by-step animated visualizer for 6 uninformed search algorithms on a dynamic grid.

---

## 📋 Overview

This project implements **6 uninformed (blind) search algorithms** that navigate a grid from a **Start (S)** to a **Target (T)** while avoiding static and dynamically spawning walls. The GUI animates every step so you can watch the algorithm "flood" the grid in real time.

---

## 🔍 Algorithms Implemented

| # | Algorithm | Key Property |
|---|-----------|-------------|
| 1 | **BFS** – Breadth-First Search | Shortest path (unweighted), explores level by level |
| 2 | **DFS** – Depth-First Search | Memory efficient, not optimal |
| 3 | **UCS** – Uniform-Cost Search | Optimal with step costs (diagonal = √2) |
| 4 | **DLS** – Depth-Limited Search | DFS with a depth cap (default limit = 8) |
| 5 | **IDDFS** – Iterative Deepening DFS | Combines DFS memory + BFS optimality |
| 6 | **Bidirectional BFS** | Searches from both ends simultaneously |

---

## 🎨 GUI Color Legend

| Color | Meaning |
|-------|---------|
| 🟩 Green | Start node |
| 🟥 Red | Target node |
| 🟦 Blue | Frontier (in queue/stack) |
| 🩵 Light Blue | Explored nodes |
| 🟨 Gold | Final path |
| ⬛ Dark | Static wall |
| 🟧 Orange | Dynamic wall (spawned at runtime) |

---

## 🚀 How to Run

### 1. Prerequisites

```bash
pip install matplotlib numpy
```

> Python 3.8+ required.

### 2. Run the program

```bash
python ai_pathfinder.py
```

### 3. Select an algorithm

```
========================================
   GOOD PERFORMANCE TIME APP — AI Pathfinder
========================================
  [1]  BFS  – Breadth-First Search
  [2]  DFS  – Depth-First Search
  [3]  UCS  – Uniform-Cost Search
  [4]  DLS  – Depth-Limited Search
  [5]  IDDFS – Iterative Deepening DFS
  [6]  BIDI – Bidirectional Search
  [7]  RUN ALL 6 algorithms one by one
  [0]  Exit
```

Enter a number and a **15×15 grid** will be randomly generated and the algorithm will animate on screen.

---

## ⚙️ Configuration (top of file)

```python
GRID_ROWS    = 15       # grid height
GRID_COLS    = 15       # grid width
WALL_RATIO   = 0.20     # fraction of cells that are static walls
DYNAMIC_PROB = 0.03     # probability of a new dynamic wall per step
DLS_LIMIT    = 8        # depth limit for DLS
STEP_DELAY   = 0.06     # seconds between animation frames (lower = faster)
```

---

## 🔄 Dynamic Obstacles

At each step of every algorithm, there is a **3% chance** that a new orange wall spawns on any empty cell. If this new wall blocks the current planned path, the algorithm **automatically re-plans** from the current node to the target.

---

## 🧭 Movement Directions

All 8 directions are supported:

| Direction | Δrow | Δcol |
|-----------|------|------|
| Up | -1 | 0 |
| Right | 0 | +1 |
| Down | +1 | 0 |
| Down-Right (diagonal) | +1 | +1 |
| Left | 0 | -1 |
| Top-Left (diagonal) | -1 | -1 |
| Top-Right (diagonal) | -1 | +1 |
| Down-Left (diagonal) | +1 | -1 |

---

## 📁 File Structure

```
├── ai_pathfinder.py   # Main source code (all algorithms + GUI)
└── README.md          # This file
```

---

## 📊 Algorithm Comparison

| Algorithm | Complete? | Optimal? | Time | Space |
|-----------|-----------|----------|------|-------|
| BFS | ✅ Yes | ✅ Yes (unweighted) | O(b^d) | O(b^d) |
| DFS | ✅ Yes (finite) | ❌ No | O(b^m) | O(bm) |
| UCS | ✅ Yes | ✅ Yes (with costs) | O(b^(C*/ε)) | O(b^(C*/ε)) |
| DLS | ❌ No (if goal > limit) | ❌ No | O(b^l) | O(bl) |
| IDDFS | ✅ Yes | ✅ Yes (unweighted) | O(b^d) | O(bd) |
| Bidirectional | ✅ Yes | ✅ Yes | O(b^(d/2)) | O(b^(d/2)) |

*b = branching factor, d = depth of solution, m = max depth, l = depth limit*

---

## 📝 Notes

- Each algorithm run uses a **freshly generated random grid**, so results vary each time.
- Close the matplotlib window to return to the menu and run another algorithm.
- For **IDDFS**, the visualization resets each depth iteration — watch the algorithm explore deeper layers progressively.
