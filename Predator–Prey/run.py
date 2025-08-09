import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random

"""
Predator–Prey dynamic complex system simulation

Colors mapping in the visualization:
- White ("white") — Empty cells (no agent)
- Green ("green") — Prey agents
- Red ("red") — Predator agents

- How it works:

* Prey move randomly and reproduce with a set probability.
* Predators seek prey in adjacent cells.
* If they find prey → they eat it, reset hunger, and may reproduce.
* If they don’t eat → hunger decreases until they starve.
* If predator eats prey in a step: hunger resets to max (starve time), because it just fed.
* If predator does NOT eat in a step: hunger decreases by 1 (getting hungrier).
* When hunger reaches zero → predator dies.
* Toroidal grid — edges wrap around so agents reappear on the opposite side.
* Visualization updates every iteration so you can watch the dynamics unfold.

- Updates:
* Predators hunt prey within a Manhattan distance (radius) of 2 instead of just adjacent cells.
* Predators move directly onto prey cells to eat.
* If multiple prey are in range, predator picks one randomly.
* Predators move only once per step.

* Starvation kills predator correctly.
* Prey still move randomly and reproduce.



This is an agent-based simulation, so you’ll see predators and prey moving, eating, and reproducing step-by-step.
"""

# future work:
# - add a random prey/predator genration at each step



# Constants for cell states
EMPTY = 0
PREY = 1
PREDATOR = 2

class Agent:
    def __init__(self, x, y, env):
        self.x = x
        self.y = y
        self.env = env
    
    def step(self):
        raise NotImplementedError()

class Prey(Agent):
    reproduce_prob = 0.1

    def step(self):
        # Move to random empty adjacent cell if possible
        empty_neighbors = self.env.get_adjacent_cells(self.x, self.y, state=EMPTY)
        if empty_neighbors:
            nx, ny = random.choice(empty_neighbors)
            self.env.move_agent(self, nx, ny)
        # Reproduce with some probability in adjacent empty cell
        if random.random() < Prey.reproduce_prob:
            empty_neighbors = self.env.get_adjacent_cells(self.x, self.y, state=EMPTY)
            if empty_neighbors:
                rx, ry = random.choice(empty_neighbors)
                self.env.add_agent(Prey(rx, ry, self.env))

class Predator(Agent):
    reproduce_prob = 0.05
    starve_time = 20
    hunting_radius = 8

    def __init__(self, x, y, env):
        super().__init__(x, y, env)
        self.hunger = Predator.starve_time
        self.ate_this_turn = False

    def step(self):
        self.ate_this_turn = False
        # Look for prey within hunting radius
        prey_cells = self.env.get_cells_in_radius(self.x, self.y, Predator.hunting_radius, state=PREY)
        if prey_cells:
            # Hunt random prey
            target = random.choice(prey_cells)
            self.env.remove_agent_at(*target)  # Eat prey
            self.env.move_agent(self, *target)
            self.hunger = Predator.starve_time
            self.ate_this_turn = True
            # Reproduce in old position with probability
            if random.random() < Predator.reproduce_prob:
                self.env.add_agent(Predator(self.x, self.y, self.env))
        else:
            # Move to empty adjacent cell if possible
            empty_neighbors = self.env.get_adjacent_cells(self.x, self.y, state=EMPTY)
            if empty_neighbors:
                nx, ny = random.choice(empty_neighbors)
                self.env.move_agent(self, nx, ny)
            # Lose hunger if did not eat
            self.hunger -= 1
            if self.hunger <= 0:
                self.env.remove_agent(self)

class Environment:
    def __init__(self, size, initial_prey, initial_predators):
        self.size = size
        self.grid = np.zeros((size, size), dtype=int)
        self.agents = []
        self.agent_map = {}  # (x,y) -> agent for quick lookup

        # Place initial prey
        self.populate_agents(Prey, initial_prey)
        # Place initial predators
        self.populate_agents(Predator, initial_predators)

    def populate_agents(self, agent_cls, count):
        placed = 0
        while placed < count:
            x, y = np.random.randint(0, self.size, 2)
            if self.grid[x, y] == EMPTY:
                agent = agent_cls(x, y, self)
                self.add_agent(agent)
                placed += 1

    def add_agent(self, agent):
        self.agents.append(agent)
        self.grid[agent.x, agent.y] = PREY if isinstance(agent, Prey) else PREDATOR
        self.agent_map[(agent.x, agent.y)] = agent

    def remove_agent(self, agent):
        self.grid[agent.x, agent.y] = EMPTY
        self.agent_map.pop((agent.x, agent.y), None)
        if agent in self.agents:
            self.agents.remove(agent)

    def remove_agent_at(self, x, y):
        agent = self.agent_map.get((x, y))
        if agent:
            self.remove_agent(agent)

    def move_agent(self, agent, new_x, new_y):
        # Remove old position
        self.grid[agent.x, agent.y] = EMPTY
        self.agent_map.pop((agent.x, agent.y), None)

        # Update agent coords
        agent.x, agent.y = new_x, new_y

        # Update grid and map
        self.grid[new_x, new_y] = PREY if isinstance(agent, Prey) else PREDATOR
        self.agent_map[(new_x, new_y)] = agent

    def get_adjacent_cells(self, x, y, state=None):
        candidates = []
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = (x + dx) % self.size, (y + dy) % self.size
            if state is None or self.grid[nx, ny] == state:
                candidates.append((nx, ny))
        return candidates

    def get_cells_in_radius(self, x, y, radius, state=None):
        positions = []
        for dx in range(-radius, radius+1):
            for dy in range(-radius, radius+1):
                if abs(dx) + abs(dy) <= radius:
                    nx, ny = (x + dx) % self.size, (y + dy) % self.size
                    if (dx !=0 or dy !=0):
                        if state is None or self.grid[nx, ny] == state:
                            positions.append((nx, ny))
        return positions

    def step(self):
        # Shuffle agents to randomize action order
        random.shuffle(self.agents)
        # Use a copy since agents can be removed during iteration
        for agent in self.agents[:]:
            agent.step()

class Simulation:
    def __init__(self, grid_size=50, num_prey=400, num_predators=50, max_iters=200, delay=0.1):
        self.env = Environment(grid_size, num_prey, num_predators)
        self.max_iters = max_iters
        self.delay = delay
        self.cmap = mcolors.ListedColormap(["white", "green", "red"])
        self.bounds = [EMPTY, PREY, PREDATOR, PREDATOR+1]
        self.norm = mcolors.BoundaryNorm(self.bounds, self.cmap.N)

    def run(self):
        plt.ion()
        fig, ax = plt.subplots(figsize=(6,6))

        for step in range(self.max_iters):
            self.env.step()
            ax.clear()
            ax.imshow(self.env.grid, cmap=self.cmap, norm=self.norm)
            ax.set_title(f"Predator–Prey Simulation (Step {step+1})")
            ax.axis('off')
            plt.draw()
            plt.pause(self.delay)

        plt.ioff()
        plt.show()

if __name__ == "__main__":
    sim = Simulation()
    sim.run()
