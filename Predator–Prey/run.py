import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import time
import random

"""
Predator–Prey dynamic complex system simulation

- How it works:

* Prey move randomly and reproduce with a set probability.
* Predators seek prey in adjacent cells.
* If they find prey → they eat it, reset hunger, and may reproduce.
* If they don’t eat → hunger decreases until they starve.
* Toroidal grid — edges wrap around so agents reappear on the opposite side.
* Visualization updates every iteration so you can watch the dynamics unfold.

Colors mapping in the visualization:
- White ("white") — Empty cells (no agent)
- Green ("green") — Prey agents
- Red ("red") — Predator agents

This is an agent-based simulation, so you’ll see predators and prey moving, eating, and reproducing step-by-step.
"""

# future work:
# - add a random prey/predator genration at each step



# Parameters
grid_size = 50
num_prey = 50
num_predators = 200
prey_reproduce_prob = 0.1      # chance prey reproduces each step
predator_reproduce_prob = 0.05 # chance predator reproduces after eating
predator_starve_time = 5       # steps before predator dies without food
max_iters = 300
delay = 0.1  # seconds between iterations

# States
EMPTY = 0
PREY = 1
PREDATOR = 2

# Initialize grid
grid = np.zeros((grid_size, grid_size), dtype=int)

# Track predator hunger (parallel array)
hunger = np.zeros((grid_size, grid_size), dtype=int)

# Randomly place prey
for _ in range(num_prey):
    x, y = np.random.randint(0, grid_size, 2)
    grid[x, y] = PREY

# Randomly place predators
for _ in range(num_predators):
    x, y = np.random.randint(0, grid_size, 2)
    grid[x, y] = PREDATOR
    hunger[x, y] = predator_starve_time

# Color map
cmap = mcolors.ListedColormap(["white", "green", "red"])
bounds = [EMPTY, PREY, PREDATOR, PREDATOR + 1]
norm = mcolors.BoundaryNorm(bounds, cmap.N)

# Movement offsets
moves = [(-1,0), (1,0), (0,-1), (0,1)]

plt.ion()
fig, ax = plt.subplots()

for step in range(max_iters):
    new_grid = grid.copy()
    new_hunger = hunger.copy()

    # Shuffle coordinates to avoid directional bias
    coords = [(x, y) for x in range(grid_size) for y in range(grid_size)]
    random.shuffle(coords)

    for x, y in coords:
        if grid[x, y] == PREY:
            # Move prey randomly if empty space
            dx, dy = random.choice(moves)
            nx, ny = (x + dx) % grid_size, (y + dy) % grid_size
            if grid[nx, ny] == EMPTY:
                new_grid[nx, ny] = PREY
                new_grid[x, y] = EMPTY
                # Reproduce
                if random.random() < prey_reproduce_prob:
                    new_grid[x, y] = PREY

        elif grid[x, y] == PREDATOR:
            # Predator tries to move to prey first
            ate = False
            for dx, dy in moves:
                nx, ny = (x + dx) % grid_size, (y + dy) % grid_size
                if grid[nx, ny] == PREY:
                    new_grid[nx, ny] = PREDATOR
                    new_hunger[nx, ny] = predator_starve_time
                    new_grid[x, y] = EMPTY
                    ate = True
                    # Reproduce after eating
                    if random.random() < predator_reproduce_prob:
                        new_grid[x, y] = PREDATOR
                        new_hunger[x, y] = predator_starve_time
                    break

            if not ate:
                # Move to empty space
                dx, dy = random.choice(moves)
                nx, ny = (x + dx) % grid_size, (y + dy) % grid_size
                if grid[nx, ny] == EMPTY:
                    new_grid[nx, ny] = PREDATOR
                    new_hunger[nx, ny] = hunger[x, y] - 1
                    new_grid[x, y] = EMPTY
                else:
                    new_hunger[x, y] -= 1

                # Starvation check
                if new_hunger[nx, ny] <= 0:
                    new_grid[nx, ny] = EMPTY
                    new_hunger[nx, ny] = 0

    grid = new_grid
    hunger = new_hunger

    # Visualization
    ax.clear()
    ax.imshow(grid, cmap=cmap, norm=norm)
    ax.set_title(f"Predator–Prey Simulation (Step {step})")
    ax.axis("off")
    plt.draw()
    plt.pause(delay)

plt.ioff()
plt.show()
