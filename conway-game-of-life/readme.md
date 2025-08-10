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

### Convay's Game of Life:

In the 1970s a two-state, two-dimensional cellular automaton named **Game of Life** became widely known, particularly among the early computing community. Invented by John Conway and popularized by Martin Gardner in a Scientific American article, its rules are as follows:

- Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
- Any live cell with two or three live neighbours lives on to the next generation.
- Any live cell with more than three live neighbours dies, as if by overpopulation.
- Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.


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
