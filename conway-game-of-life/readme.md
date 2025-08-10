# Conway's Game of Life (A Cellular Automaton Simulator)

In the 1970s a two-state, two-dimensional cellular automaton named **Game of Life** became widely known, particularly among the early computing community. It was invented by John Conway and popularized by Martin Gardner in a Scientific American article.

Here is a flexible and extensible Python implementation of life-like cellular automata, featuring real-time visualization and customizable rules.


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

### Classic Conway's Game of Life Rules:

- Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
- Any live cell with two or three live neighbours lives on to the next generation.
- Any live cell with more than three live neighbours dies, as if by overpopulation.
- Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.

You can tweak the rules and boundary conditions to explore different variations of the game.
Several predefined configurations are available in [`interesting_configs.py`](./interesting_configs.py) for quick experimentation.


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
