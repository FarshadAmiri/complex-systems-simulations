import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors

# Parameters
# ==================================================================
# Simulation Configuration

# Grid size
# The simulation grid is square: grid_size × grid_size cells.
grid_size = 50

# Relative population fractions for each agent group.
# - Each value is a fraction of the total grid (0.0 to 1.0).
# - Values must sum to ≤ 1.0. Remaining fraction will be empty cells.
# - You can define as many groups as you like by adding more values.
# Example: [0.3, 0.4, 0.2] → 30% Group 1, 40% Group 2, 20% Group 3, and 10% empty.
populations = [0.15, 0.45]

# Colors assigned to each category in the simulation.
# - The FIRST color is reserved for empty cells.
# - Remaining colors correspond to groups in the same order as in `populations`.
# - Must include at least len(populations) + 1 colors.
# Colors can be any Matplotlib-recognized name or hex code (e.g., "#FF0000").
colors = ['white', 'red', 'blue', 'green', 'yellow', 'purple', 'orange', 'cyan', 'magenta']

# Agent satisfaction tolerance.
# - Fraction of neighbors that must be of the same group for an agent to be "happy" and try not to relocate.
# - Range: 0.0 (very tolerant) to 1.0 (very intolerant).
# - Higher values → stronger segregation.
tolerance = 0.6

# Maximum number of simulation iterations before stopping.
max_iters = 500
# ==================================================================


EMPTY = 0
GROUP_IDS = list(range(1, len(populations) + 1))

def initialize_grid(size, populations):
    total_cells = size * size
    num_agents = int(total_cells * sum(populations))
    num_empty = total_cells - num_agents
    
    counts = [int(total_cells * p) for p in populations]
    diff = num_agents - sum(counts)
    counts[0] += diff
    
    cells = []
    for gid, count in zip(GROUP_IDS, counts):
        cells.extend([gid]*count)
    cells.extend([EMPTY]*num_empty)
    
    np.random.shuffle(cells)
    grid = np.array(cells).reshape((size, size))
    return grid

def get_neighbors(grid, x, y):
    neighbors = []
    for dx in [-1,0,1]:
        for dy in [-1,0,1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = x + dx, y + dy
            if 0 <= nx < grid.shape[0] and 0 <= ny < grid.shape[1]:
                neighbors.append(grid[nx, ny])
    return neighbors

def is_happy(grid, x, y, tolerance):
    agent = grid[x,y]
    if agent == EMPTY:
        return True
    neighbors = get_neighbors(grid, x, y)
    if len(neighbors) == 0:
        return True
    similar = sum(1 for n in neighbors if n == agent)
    similarity_ratio = similar / len(neighbors)
    return similarity_ratio >= tolerance

def find_unhappy_agents(grid, tolerance):
    unhappy_agents = []
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x,y] != EMPTY and not is_happy(grid, x, y, tolerance):
                unhappy_agents.append((x,y))
    return unhappy_agents

def find_empty_cells(grid):
    empties = []
    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if grid[x,y] == EMPTY:
                empties.append((x,y))
    return empties

def move_agents(grid, tolerance):
    unhappy_agents = find_unhappy_agents(grid, tolerance)
    empty_cells = find_empty_cells(grid)
    np.random.shuffle(unhappy_agents)
    np.random.shuffle(empty_cells)
    
    moved = 0
    for agent_pos in unhappy_agents:
        if not empty_cells:
            break
        agent_type = grid[agent_pos]
        new_pos = empty_cells.pop()
        
        grid[new_pos] = agent_type
        grid[agent_pos] = EMPTY
        moved += 1
    return moved

def update(frame_num, img, grid, tolerance):
    moved = move_agents(grid, tolerance)
    img.set_data(grid)
    plt.title(f'Schelling Model - Iteration {frame_num+1}, Agents moved: {moved}')
    if moved == 0:
        ani.event_source.stop()
    return img,

def main():
    global colors
    grid = initialize_grid(grid_size, populations)
    
    fig, ax = plt.subplots()
    
    num_colors = len(populations) + 1
    if num_colors > len(colors):
        import matplotlib.cm as cm
        cmap_ = cm.get_cmap('tab20', num_colors)
        colors = [cmap_(i) for i in range(num_colors)]
    else:
        colors = colors[:num_colors]
    
    cmap = mcolors.ListedColormap(colors)
    bounds = list(range(num_colors+1))
    norm = mcolors.BoundaryNorm(bounds, cmap.N)
    
    img = ax.imshow(grid, cmap=cmap, norm=norm)
    ax.axis('off')
    
    global ani
    ani = animation.FuncAnimation(fig, update, fargs=(img, grid, tolerance),
                                  frames=max_iters, interval=500, repeat=False)
    
    plt.show()

if __name__ == "__main__":
    main()



