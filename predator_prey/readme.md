# Predator-Prey Simulation with Agent-Based Modeling

This repository contains a modular, object-oriented predator-prey simulation implemented in Python. It models the interactions of two species—predators and prey—on a 2D toroidal grid using agent-based modeling (ABM) principles. The simulation provides real-time visualization of complex emergent behaviors such as population dynamics, hunting, reproduction, and starvation.


## Overview

Agent-Based Modeling (ABM) is a powerful computational approach to simulate complex systems composed of interacting autonomous agents. This predator-prey simulation demonstrates how simple local behaviors of individual agents can give rise to complex population-level dynamics over time.

### Key Features

- **Modular, Object-Oriented Design:** Separate classes for `Agent`, `Prey`, `Predator`, and `Environment` ensure code clarity, extensibility, and maintainability.
- **Toroidal Grid:** The 2D grid "wraps around" edges, modeling an unbounded continuous space.
- **Predator Hunting:** Predators search for prey within a configurable Manhattan radius and consume prey to survive.
- **Reproduction:** Both prey and predators can reproduce with user-configurable probabilities.
- **Starvation:** Predators have limited hunger capacity and die if they fail to eat within a given time.
- **Real-Time Visualization:** The simulation displays the grid dynamically using `matplotlib`, with distinct colors representing empty cells, prey, and predators.


## Simulation Components

### Agents

- **Prey:** Move randomly to adjacent empty cells; reproduce probabilistically.
- **Predators:** Hunt prey within a configurable radius; move, reproduce, and starve if unsuccessful at hunting.


### Environment

- Manages the grid state and agent positions.
- Provides neighbor queries for movement and hunting.
- Handles agent placement, removal, and movements, ensuring no conflicting updates.

### Simulation

- Coordinates the simulation loop.
- Updates agents in randomized order to avoid bias.
- Visualizes the system state at each timestep.


## How it works:
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

Updates:
* Predators move directly onto prey cells to eat.
* If multiple prey are in range, predator picks one randomly.


### Prerequisites

- Python 3.7+
- Required packages: numpy, matplotlib


### How to Run

Clone this repository:

```bash
git clone https://github.com/FarshadAmiri/complex-systems_simulations/
cd predator_prey
python run.py
