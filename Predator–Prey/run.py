import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import random

"""
Predator–Prey dynamic complex system simulation
This is an agent-based simulation, so you’ll see predators and prey moving, eating, and reproducing step-by-step.


Colors mapping in the visualization:
- White ("white") — Empty cells (no agent)
- Green ("green") — Prey agents
- Red ("red") — Predator agents


How it works:
* Prey move randomly and reproduce with a set probability.
* Predators seek prey in adjacent cells.
* If they find prey (within a specific radius of adjacent cells) → they eat it, reset hunger, and may reproduce.
* If they don’t eat → hunger decreases until they starve and die.
* If predator eats prey in a step: hunger resets to max (starve time), because it just fed.
* If predator does NOT eat in a step: hunger decreases by 1 (getting hungrier).
* When hunger reaches zero → predator dies.
* Predators move only once per step.
* Toroidal grid — edges wrap around so agents reappear on the opposite side.
* Visualization updates every iteration so you can watch the dynamics unfold.

- Updates:
* Predators move directly onto prey cells to eat.
* If multiple prey are in range, predator picks one randomly.
"""

# future work:



# ==== Parameters ====
grid_size = 50   # 50
num_predators = 50   # 50
num_prey = 400    # 400
prey_reproduce_prob = 0.15     # 0.1
predator_reproduce_prob = 0.05     # 0.05
predator_starve_time = 20      # 20
predator_hunting_radius = 2    # 2
max_iters = 10000
delay = 0.08

# ==== Constants for cell states ====
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
    def __init__(self, x, y, env, reproduce_prob):
        super().__init__(x, y, env)
        self.reproduce_prob = reproduce_prob

    def step(self):
        empty_neighbors = self.env.get_adjacent_cells(self.x, self.y, state=EMPTY)
        if empty_neighbors:
            nx, ny = random.choice(empty_neighbors)
            self.env.move_agent(self, nx, ny)
        if random.random() < self.reproduce_prob:
            empty_neighbors = self.env.get_adjacent_cells(self.x, self.y, state=EMPTY)
            if empty_neighbors:
                rx, ry = random.choice(empty_neighbors)
                self.env.add_agent(Prey(rx, ry, self.env, self.reproduce_prob))


class Predator(Agent):
    def __init__(self, x, y, env, reproduce_prob, starve_time, hunting_radius):
        super().__init__(x, y, env)
        self.reproduce_prob = reproduce_prob
        self.starve_time = starve_time
        self.hunting_radius = hunting_radius
        self.hunger = starve_time
        self.ate_this_turn = False

    def step(self):
        self.ate_this_turn = False
        prey_cells = self.env.get_cells_in_radius(self.x, self.y, self.hunting_radius, state=PREY)
        if prey_cells:
            target = random.choice(prey_cells)
            self.env.remove_agent_at(*target)
            self.env.move_agent(self, *target)
            self.hunger = self.starve_time
            self.ate_this_turn = True
            if random.random() < self.reproduce_prob:
                self.env.add_agent(Predator(self.x, self.y, self.env,
                                            self.reproduce_prob, self.starve_time, self.hunting_radius))
        else:
            empty_neighbors = self.env.get_adjacent_cells(self.x, self.y, state=EMPTY)
            if empty_neighbors:
                nx, ny = random.choice(empty_neighbors)
                self.env.move_agent(self, nx, ny)
            self.hunger -= 1
            if self.hunger <= 0:
                self.env.remove_agent(self)


class Environment:
    def __init__(self, size, initial_prey, initial_predators,
                 prey_reproduce_prob, predator_reproduce_prob,
                 predator_starve_time, predator_hunting_radius):
        self.size = size
        self.grid = np.zeros((size, size), dtype=int)
        self.agents = []
        self.agent_map = {}

        self.populate_agents(lambda x, y: Prey(x, y, self, prey_reproduce_prob), initial_prey)
        self.populate_agents(lambda x, y: Predator(x, y, self,
                                                   predator_reproduce_prob, predator_starve_time, predator_hunting_radius),
                             initial_predators)

    def populate_agents(self, agent_factory, count):
        placed = 0
        while placed < count:
            x, y = np.random.randint(0, self.size, 2)
            if self.grid[x, y] == EMPTY:
                agent = agent_factory(x, y)
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
        self.grid[agent.x, agent.y] = EMPTY
        self.agent_map.pop((agent.x, agent.y), None)
        agent.x, agent.y = new_x, new_y
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
                    if (dx != 0 or dy != 0):
                        if state is None or self.grid[nx, ny] == state:
                            positions.append((nx, ny))
        return positions

    def step(self):
        random.shuffle(self.agents)
        for agent in self.agents[:]:
            agent.step()


class Simulation:
    def __init__(self, grid_size, num_prey, num_predators, prey_reproduce_prob,
                 predator_reproduce_prob, predator_starve_time, predator_hunting_radius,
                 max_iters, delay):
        self.env = Environment(grid_size, num_prey, num_predators,
                               prey_reproduce_prob, predator_reproduce_prob,
                               predator_starve_time, predator_hunting_radius)
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

            prey_count = sum(isinstance(agent, Prey) for agent in self.env.agents)
            predator_count = sum(isinstance(agent, Predator) for agent in self.env.agents)

            if prey_count == 0 or predator_count == 0:
                print(f"Simulation ended at step {step+1} — Prey: {prey_count}, Predators: {predator_count}")
                plt.close()
                break

        plt.ioff()
        plt.show()


if __name__ == "__main__":
    sim = Simulation(grid_size, num_prey, num_predators,
                     prey_reproduce_prob, predator_reproduce_prob,
                     predator_starve_time, predator_hunting_radius,
                     max_iters, delay)
    sim.run()