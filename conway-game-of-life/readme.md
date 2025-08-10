# Conway's Game of Life (A Cellular Automaton Simulator)

A flexible and extensible Python implementation of life-like cellular automata, featuring real-time visualization and customizable rules.


## Overview

Cellular automata (CA) are discrete, abstract computational systems that have found application in modeling complex systems, biological processes, and emergent phenomena. This project implements a life-like CA framework capable of simulating a wide range of CA rules, including the classic Conway’s Game of Life.

The simulator supports:

- Custom birth/survival rules defined via **B/S notation** (e.g., B3/S23 for Conway’s Game of Life)
- Toroidal (wrap-around) or bounded grid topologies
- Multiple initialization modes: random, predefined patterns (glider, blinker), and custom setups
- Real-time interactive visualization using Matplotlib
- Configurable grid size, simulation steps, and visualization speed

## How It Works

The cellular automaton evolves over discrete time steps based on local rules applied uniformly to each cell in the grid:

1. **Grid Structure:**  
   The simulation runs on a two-dimensional square grid where each cell is either *alive* (populated) or *dead* (empty).

2. **Neighborhood:**  
   Each cell’s fate depends on its 8 neighboring cells (Moore neighborhood), including diagonals.

3. **Rule Application (Life-like rules in B/S format):**  
   - **Birth (B):** A dead cell becomes alive if the number of alive neighbors matches any number in the birth list.  
   - **Survival (S):** A living cell remains alive if the number of alive neighbors matches any number in the survival list. Otherwise, it dies.

4. **Boundary Conditions:**  
   The grid can be configured to *wrap around* edges (toroidal), making the top and bottom, left and right edges adjacent. Alternatively, boundaries can be treated as fixed (cells outside the grid are considered dead).

5. **Iteration:**  
   At each simulation step:  
   - The entire grid is evaluated simultaneously to compute the next generation.  
   - Updates are applied to produce a new grid state.

6. **Visualization:**  
   The current state of the grid is rendered in real-time using Matplotlib, with alive cells shown in black and dead cells in white (configurable).


### Features

- **Rule Flexibility:** Easily specify birth and survival conditions to simulate various life-like cellular automata.
- **Pattern Initialization:** Quickly start simulations with common patterns like gliders or oscillators, or with randomized initial states.
- **Toroidal Grid:** The simulation grid “wraps around” edges to emulate infinite plane behavior.
- **Real-Time Visualization:** Watch the system evolve over time with smooth, step-by-step rendering.
- **Extensible Design:** The codebase is clear and modular, making it straightforward to extend with new features or patterns.

## Usage

### Prerequisites

- Python 3.7+
- Required packages: numpy, matplotlib


### How to Run

Clone this repository:

```bash
git clone https://github.com/FarshadAmiri/complex-systems_simulations/
cd conway-game-of-life
python run.py
