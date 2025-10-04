import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.colors as mcolors
import random

"""
Cultural Evolution Simulation

This simulation models how cultural traits evolve in human populations through:
- Individual agents with cultural characteristics (cooperation, innovation, tradition)
- Environmental challenges that favor certain cultural adaptations
- Cultural transmission through social interaction
- Innovation and adaptation based on environmental feedback

Key Concepts:
- Agents have cultural trait vectors that define their behavior
- Cultural traits influence survival and reproduction success
- Agents learn from successful neighbors (cultural transmission)
- Environmental pressures create selection for adaptive traits
- Innovation introduces new cultural variations
"""

# ==== Parameters ====
grid_size = 40                     # Size of the simulation grid
population_density = 0.6           # Fraction of cells initially occupied
max_iterations = 500               # Maximum simulation steps

# Cultural trait parameters (each trait ranges from 0.0 to 1.0)
cooperation_weight = 0.4           # Importance of cooperation for survival
innovation_weight = 0.3            # Importance of innovation for survival  
tradition_weight = 0.3             # Importance of tradition for survival

# Environmental parameters
environmental_pressure = 0.7       # Strength of environmental selection
learning_rate = 0.1               # How much agents learn from neighbors
innovation_rate = 0.05            # Probability of trait mutation
reproduction_threshold = 0.6       # Minimum fitness for reproduction
death_threshold = 0.3             # Maximum fitness for survival

# Visualization parameters
update_interval = 200             # Milliseconds between animation frames

# ==== Constants ====
EMPTY = 0
OCCUPIED = 1

class CulturalAgent:
    """Represents an individual agent with cultural traits"""
    
    def __init__(self, cooperation=None, innovation=None, tradition=None):
        # Initialize cultural traits randomly if not specified
        self.cooperation = cooperation if cooperation is not None else random.random()
        self.innovation = innovation if innovation is not None else random.random()
        self.tradition = tradition if tradition is not None else random.random()
        
        # Normalize traits to ensure they sum to a reasonable range
        total = self.cooperation + self.innovation + self.tradition
        if total > 2.0:  # Allow some flexibility but prevent extreme values
            factor = 2.0 / total
            self.cooperation *= factor
            self.innovation *= factor
            self.tradition *= factor
            
        self.fitness = 0.0
        self.age = 0
    
    def calculate_fitness(self, environment_type=1.0):
        """Calculate agent fitness based on cultural traits and environment"""
        # Environment type affects which traits are more valuable
        # environment_type ranges from 0 (stable) to 1 (changing)
        
        coop_benefit = self.cooperation * cooperation_weight
        innov_benefit = self.innovation * innovation_weight * environment_type
        trad_benefit = self.tradition * tradition_weight * (1 - environment_type)
        
        # Fitness is combination of traits weighted by environmental conditions
        base_fitness = coop_benefit + innov_benefit + trad_benefit
        
        # Add some noise to prevent deterministic outcomes
        noise = random.uniform(-0.1, 0.1)
        self.fitness = max(0.0, min(1.0, base_fitness + noise))
        
        return self.fitness
    
    def learn_from_neighbor(self, neighbor, learning_rate):
        """Learn cultural traits from a successful neighbor"""
        if neighbor.fitness > self.fitness:
            # Learn more successful traits
            self.cooperation += (neighbor.cooperation - self.cooperation) * learning_rate
            self.innovation += (neighbor.innovation - self.innovation) * learning_rate
            self.tradition += (neighbor.tradition - self.tradition) * learning_rate
            
            # Keep traits in valid range
            self.cooperation = max(0.0, min(1.0, self.cooperation))
            self.innovation = max(0.0, min(1.0, self.innovation))
            self.tradition = max(0.0, min(1.0, self.tradition))
    
    def innovate(self, innovation_rate):
        """Randomly modify cultural traits (innovation/mutation)"""
        if random.random() < innovation_rate:
            trait_to_change = random.choice(['cooperation', 'innovation', 'tradition'])
            change = random.uniform(-0.1, 0.1)
            
            if trait_to_change == 'cooperation':
                self.cooperation = max(0.0, min(1.0, self.cooperation + change))
            elif trait_to_change == 'innovation':
                self.innovation = max(0.0, min(1.0, self.innovation + change))
            else:
                self.tradition = max(0.0, min(1.0, self.tradition + change))
    
    def reproduce(self):
        """Create offspring with slightly modified traits"""
        child = CulturalAgent(
            cooperation=self.cooperation + random.uniform(-0.05, 0.05),
            innovation=self.innovation + random.uniform(-0.05, 0.05),
            tradition=self.tradition + random.uniform(-0.05, 0.05)
        )
        return child
    
    def get_dominant_trait(self):
        """Return which cultural trait is strongest"""
        traits = [self.cooperation, self.innovation, self.tradition]
        max_trait = max(traits)
        if self.cooperation == max_trait:
            return 'cooperation'
        elif self.innovation == max_trait:
            return 'innovation'
        else:
            return 'tradition'

def initialize_population(grid_size, density):
    """Initialize the population grid with random agents"""
    grid = np.empty((grid_size, grid_size), dtype=object)
    
    for i in range(grid_size):
        for j in range(grid_size):
            if random.random() < density:
                grid[i, j] = CulturalAgent()
            else:
                grid[i, j] = None
    
    return grid

def get_neighbors(grid, x, y):
    """Get all neighboring agents (Moore neighborhood)"""
    neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = (x + dx) % grid.shape[0], (y + dy) % grid.shape[1]
            if grid[nx, ny] is not None:
                neighbors.append(grid[nx, ny])
    return neighbors

def get_empty_neighbors(grid, x, y):
    """Get coordinates of empty neighboring cells"""
    empty_neighbors = []
    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            if dx == 0 and dy == 0:
                continue
            nx, ny = (x + dx) % grid.shape[0], (y + dy) % grid.shape[1]
            if grid[nx, ny] is None:
                empty_neighbors.append((nx, ny))
    return empty_neighbors

def update_population(grid, iteration):
    """Update the population for one time step"""
    # Calculate environmental type based on iteration (cyclical environment)
    environment_type = 0.5 + 0.5 * np.sin(iteration * 0.1)
    
    # Calculate fitness for all agents
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] is not None:
                grid[i, j].calculate_fitness(environment_type)
                grid[i, j].age += 1
    
    # Cultural learning phase
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] is not None:
                neighbors = get_neighbors(grid, i, j)
                if neighbors:
                    # Learn from a random successful neighbor
                    teacher = random.choice(neighbors)
                    grid[i, j].learn_from_neighbor(teacher, learning_rate)
                
                # Innovation
                grid[i, j].innovate(innovation_rate)
    
    # Reproduction and death phase
    new_births = []
    deaths = []
    
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] is not None:
                agent = grid[i, j]
                
                # Death based on low fitness or old age
                if agent.fitness < death_threshold or agent.age > 100:
                    deaths.append((i, j))
                
                # Reproduction based on high fitness
                elif agent.fitness > reproduction_threshold and random.random() < 0.1:
                    empty_neighbors = get_empty_neighbors(grid, i, j)
                    if empty_neighbors:
                        birth_location = random.choice(empty_neighbors)
                        child = agent.reproduce()
                        new_births.append((birth_location, child))
    
    # Apply deaths
    for i, j in deaths:
        grid[i, j] = None
    
    # Apply births
    for (i, j), child in new_births:
        if grid[i, j] is None:  # Make sure cell is still empty
            grid[i, j] = child
    
    return grid

def create_visualization_grid(population_grid):
    """Convert population grid to visualization grid based on dominant traits"""
    vis_grid = np.zeros(population_grid.shape)
    
    for i in range(population_grid.shape[0]):
        for j in range(population_grid.shape[1]):
            if population_grid[i, j] is not None:
                agent = population_grid[i, j]
                dominant_trait = agent.get_dominant_trait()
                
                if dominant_trait == 'cooperation':
                    vis_grid[i, j] = 1  # Blue
                elif dominant_trait == 'innovation':
                    vis_grid[i, j] = 2  # Red
                else:  # tradition
                    vis_grid[i, j] = 3  # Green
            else:
                vis_grid[i, j] = 0  # Empty (white)
    
    return vis_grid

def calculate_population_stats(grid):
    """Calculate population statistics"""
    total_agents = 0
    cooperation_sum = 0
    innovation_sum = 0
    tradition_sum = 0
    
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] is not None:
                agent = grid[i, j]
                total_agents += 1
                cooperation_sum += agent.cooperation
                innovation_sum += agent.innovation
                tradition_sum += agent.tradition
    
    if total_agents > 0:
        return {
            'population': total_agents,
            'avg_cooperation': cooperation_sum / total_agents,
            'avg_innovation': innovation_sum / total_agents,
            'avg_tradition': tradition_sum / total_agents
        }
    else:
        return {
            'population': 0,
            'avg_cooperation': 0,
            'avg_innovation': 0,
            'avg_tradition': 0
        }

# Global variables for animation
population_grid = None
stats_history = []

def update_simulation(frame):
    """Update function for animation"""
    global population_grid, stats_history
    
    # Update population
    population_grid = update_population(population_grid, frame)
    
    # Calculate and store statistics
    stats = calculate_population_stats(population_grid)
    stats_history.append(stats)
    
    # Create visualization
    vis_grid = create_visualization_grid(population_grid)
    
    # Update main plot
    im.set_data(vis_grid)
    
    # Update title with current statistics
    plt.suptitle(f'Cultural Evolution Simulation - Generation {frame}\n'
                f'Population: {stats["population"]}, '
                f'Cooperation: {stats["avg_cooperation"]:.2f}, '
                f'Innovation: {stats["avg_innovation"]:.2f}, '
                f'Tradition: {stats["avg_tradition"]:.2f}', 
                fontsize=12)
    
    # Update statistics plot if we have enough data
    if len(stats_history) > 1:
        ax2.clear()
        generations = range(len(stats_history))
        cooperation_vals = [s['avg_cooperation'] for s in stats_history]
        innovation_vals = [s['avg_innovation'] for s in stats_history]
        tradition_vals = [s['avg_tradition'] for s in stats_history]
        
        ax2.plot(generations, cooperation_vals, 'b-', label='Cooperation', linewidth=2)
        ax2.plot(generations, innovation_vals, 'r-', label='Innovation', linewidth=2)
        ax2.plot(generations, tradition_vals, 'g-', label='Tradition', linewidth=2)
        
        ax2.set_xlabel('Generation')
        ax2.set_ylabel('Average Trait Value')
        ax2.set_title('Cultural Trait Evolution')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_ylim(0, 1)
    
    return [im]

def main():
    """Main simulation function"""
    global population_grid, im, ax2
    
    # Initialize population
    population_grid = initialize_population(grid_size, population_density)
    
    # Create figure with subplots
    fig = plt.figure(figsize=(15, 6))
    
    # Main simulation plot
    ax1 = plt.subplot(1, 2, 1)
    
    # Create color map
    colors = ['white', 'blue', 'red', 'green']  # Empty, Cooperation, Innovation, Tradition
    cmap = mcolors.ListedColormap(colors)
    bounds = [0, 1, 2, 3, 4]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)
    
    # Initialize visualization
    vis_grid = create_visualization_grid(population_grid)
    im = ax1.imshow(vis_grid, cmap=cmap, norm=norm, interpolation='nearest')
    ax1.set_title('Cultural Evolution Simulation\nBlue: Cooperation, Red: Innovation, Green: Tradition')
    ax1.axis('off')
    
    # Statistics plot
    ax2 = plt.subplot(1, 2, 2)
    ax2.set_xlabel('Generation')
    ax2.set_ylabel('Average Trait Value')
    ax2.set_title('Cultural Trait Evolution')
    
    # Create animation
    ani = animation.FuncAnimation(fig, update_simulation, frames=max_iterations,
                                  interval=update_interval, repeat=False, blit=False)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()