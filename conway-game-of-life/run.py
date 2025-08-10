"""
A flexible life-like cellular automaton with real-time visualization.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random

# --------------------------
# Configuration
# --------------------------
grid_size = 50             # grid is grid_size x grid_size | Default: 100
init_mode = "random"         # "random", "glider", "blinker", or "custom_1"
init_density = 0.15          # used for random init: proportion of ON cells | Default: 0.15
rule_b = [2,]                 # birth counts (B)| Default: [3]
rule_s = [1, 2, 3]              # survival counts (S) | Default: [2, 3]
max_iters = 1000
delay = 0.2                  # seconds between frames
wrap = True                  # toroidal boundaries if True


# -------------------------
# Helper: preset patterns
# -------------------------
def add_glider(grid, top_left):
    x0, y0 = top_left
    coords = [(0,1), (1,2), (2,0), (2,1), (2,2)]
    for dx, dy in coords:
        grid[(x0+dx) % grid.shape[0], (y0+dy) % grid.shape[1]] = 1

def add_blinker(grid, top_left):
    x0, y0 = top_left
    coords = [(0,0), (0,1), (0,2)]
    for dx, dy in coords:
        grid[(x0+dx) % grid.shape[0], (y0+dy) % grid.shape[1]] = 1

# -------------------------
# CA core
# -------------------------
def parse_rule(B_list, S_list):
    """Return birth and survive sets from lists."""
    return set(B_list), set(S_list)

def count_neighbors(grid, x, y, wrap):
    """Count 8-neighbors (Moore)."""
    N = grid.shape[0]
    count = 0
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if wrap:
                nx %= N; ny %= N
                count += grid[nx, ny]
            else:
                if 0 <= nx < N and 0 <= ny < N:
                    count += grid[nx, ny]
    return count

def step(grid, Bset, Sset, wrap):
    N = grid.shape[0]
    new = np.zeros_like(grid)
    # vectorized-ish neighbor count via convolution would be faster,
    # but we keep explicit loops for clarity and flexibility
    for x in range(N):
        for y in range(N):
            n = 0
            # count neighbors
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if wrap:
                        nx %= N; ny %= N
                        n += grid[nx, ny]
                    else:
                        if 0 <= nx < N and 0 <= ny < N:
                            n += grid[nx, ny]
            if grid[x,y] == 0:
                # birth rule
                if n in Bset:
                    new[x,y] = 1
            else:
                # survival rule
                if n in Sset:
                    new[x,y] = 1
    return new

# -------------------------
# Initialization
# -------------------------
def initialize_grid(mode, N, density):
    grid = np.zeros((N, N), dtype=int)
    if mode == "random":
        mask = np.random.rand(N, N) < density
        grid[mask] = 1
    elif mode == "glider":
        add_glider(grid, (1, 1))
    elif mode == "blinker":
        add_blinker(grid, (N//2, N//2))
    elif mode == "custom_1":
        # place some gliders and blinkers for demo
        add_glider(grid, (2, 2))
        add_glider(grid, (20, 10))
        add_blinker(grid, (50, 50))
    else:
        raise ValueError("unknown init mode")
    return grid

# -------------------------
# Visualization + Run
# -------------------------
def run_ca(grid, Bset, Sset, max_iters=200, delay=0.1, wrap=True):
    cmap = mcolors.ListedColormap(["white", "black"])
    bounds = [0, 0.5, 1]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    plt.ion()
    fig, ax = plt.subplots(figsize=(6,6))
    img = ax.imshow(grid, cmap=cmap, norm=norm)
    ax.set_title(f"CA — B{sorted(Bset)}/S{sorted(Sset)}")
    ax.axis("off")

    for t in range(max_iters):
        grid = step(grid, Bset, Sset, wrap)
        img.set_data(grid)
        ax.set_title(f"CA — B{sorted(Bset)}/S{sorted(Sset)} — step {t+1}")
        plt.draw()
        plt.pause(delay)

        # optional frame saving
        # if save_frames:
        #     fname = f"{frame_folder}/frame_{t:04d}.png"
        #     fig.savefig(fname, dpi=150)

    plt.ioff()
    plt.show()

# -------------------------
# Run
# -------------------------
if __name__ == "__main__":
    Bset, Sset = parse_rule(rule_b, rule_s)
    grid = initialize_grid(init_mode, grid_size, init_density)
    run_ca(grid, Bset, Sset, max_iters=max_iters, delay=delay, wrap=wrap)
