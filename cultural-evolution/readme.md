# Cultural Evolution Simulation

## Overview

This repository contains a Python implementation of a **Cultural Evolution Simulation**, demonstrating how cultural traits evolve and spread through human populations via social learning, environmental adaptation, and innovation. The model illustrates how individual cultural characteristics collectively shape population-level cultural dynamics over time.

Agents representing individuals with distinct cultural profiles interact within a dynamic environment, learning from successful neighbors, innovating new behaviors, and adapting to changing environmental pressures. Through iterative cultural transmission and selection, distinct cultural patterns and trait distributions naturally emerge.

## Key Concepts

### Cultural Evolution Theory

- **Cultural Traits**: Characteristics that influence behavior and are transmitted through learning rather than genetics
- **Cultural Transmission**: The process by which cultural information spreads between individuals through social learning
- **Cultural Selection**: Environmental and social pressures that favor certain cultural traits over others
- **Innovation**: The introduction of new cultural variants through creativity and experimentation

### The Cultural Evolution Problem

- How do individual cultural traits influence survival and reproduction success?
- How does cultural learning shape population-level trait distributions?
- What role does environmental change play in cultural adaptation?
- How do innovation and tradition balance in evolving cultures?

## Model Description

### Environment

- **Grid**: A two-dimensional toroidal lattice representing the social space
- **Cells**: Each cell may be empty or occupied by an agent with cultural traits
- **Environmental Pressure**: Dynamic conditions that favor different cultural adaptations over time

### Agents

- **Cultural Traits**: Each agent has three key cultural characteristics:
  - **Cooperation**: Tendency to work with others and share resources
  - **Innovation**: Openness to new ideas and willingness to experiment
  - **Tradition**: Adherence to established practices and cultural norms

- **Fitness**: Agents' survival and reproduction success based on how well their cultural traits match environmental demands

- **Learning**: Agents observe and learn from more successful neighbors, gradually adopting beneficial cultural traits

- **Innovation**: Agents occasionally modify their cultural traits through experimentation and creativity

### Dynamics

1. **Fitness Calculation**: Each agent's fitness is determined by how well their cultural traits suit current environmental conditions
2. **Cultural Learning**: Agents learn from more successful neighbors, gradually adopting their beneficial traits
3. **Innovation**: Random cultural mutations introduce new trait variations
4. **Selection**: Agents with higher fitness are more likely to survive and reproduce
5. **Reproduction**: Successful agents create offspring with similar but slightly modified cultural traits

### Parameters

| Parameter | Description | Default Value |
|-----------|-------------|---------------|
| `grid_size` | Size of the simulation grid | 40 |
| `population_density` | Initial fraction of occupied cells | 0.6 |
| `cooperation_weight` | Importance of cooperation for fitness | 0.4 |
| `innovation_weight` | Importance of innovation for fitness | 0.3 |
| `tradition_weight` | Importance of tradition for fitness | 0.3 |
| `environmental_pressure` | Strength of environmental selection | 0.7 |
| `learning_rate` | Rate of cultural learning from neighbors | 0.1 |
| `innovation_rate` | Probability of cultural trait mutation | 0.05 |
| `reproduction_threshold` | Minimum fitness for reproduction | 0.6 |
| `death_threshold` | Maximum fitness for survival | 0.3 |

## Visualization

The simulation provides real-time visualization with two main components:

### Cultural Map
- **Blue cells**: Agents dominated by cooperation traits
- **Red cells**: Agents dominated by innovation traits  
- **Green cells**: Agents dominated by tradition traits
- **White cells**: Empty spaces

### Evolution Graph
- Real-time tracking of average cultural trait values across the population
- Shows how cultural characteristics change over generations
- Demonstrates the dynamic balance between cooperation, innovation, and tradition

## Installation and Usage

### Prerequisites

- Python 3.7+
- Required packages: numpy, matplotlib

### Installation

1. Clone this repository:
```bash
git clone https://github.com/FarshadAmiri/complex-systems-simulations/
cd complex-systems-simulations/cultural-evolution
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Simulation

Execute the main simulation:
```bash
python run.py
```

The simulation will open an interactive window showing:
- The cultural evolution map on the left
- Population statistics and trait evolution graphs on the right

### Customization

You can modify simulation parameters by editing the variables at the top of `run.py`:

```python
# Adjust these parameters to explore different scenarios
grid_size = 40                     # Size of simulation space
population_density = 0.6           # Initial population density
cooperation_weight = 0.4           # Importance of cooperation
innovation_weight = 0.3            # Importance of innovation
tradition_weight = 0.3             # Importance of tradition
learning_rate = 0.1               # Cultural learning speed
innovation_rate = 0.05            # Rate of cultural innovation
```

## Scientific Insights

This simulation demonstrates several important principles of cultural evolution:

1. **Cultural Clustering**: Similar cultural traits tend to cluster in space due to local learning
2. **Environmental Adaptation**: Populations adapt their cultural profiles to match environmental demands
3. **Innovation-Tradition Balance**: Successful cultures balance innovation with tradition
4. **Emergent Patterns**: Complex cultural dynamics emerge from simple individual behaviors

## Possible Extensions

- **Multi-level Selection**: Add group-level selection pressures
- **Cultural Complexity**: Introduce hierarchical cultural traits
- **Migration**: Allow agents to move between locations
- **Social Networks**: Implement more complex social learning networks
- **Historical Memory**: Add cultural memory and historical influence

## References

This simulation is inspired by research in:
- Cultural Evolution Theory (Boyd & Richerson, 1985)
- Agent-Based Models of Cultural Change (Henrich & McElreath, 2003)
- Social Learning and Cultural Evolution (Mesoudi, 2011)