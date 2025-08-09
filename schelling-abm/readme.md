# Schelling's Segregation Model — Generative Agent-Based Modeling

## Overview

This project implements **Schelling's Segregation Model**, a classic example of **generative agent-based modeling (ABM)** that demonstrates how simple individual preferences can lead to emergent, large-scale patterns of residential segregation.

Agents of different groups (e.g., ethnicities) occupy a grid representing a neighborhood. Each agent prefers a minimum fraction of neighbors similar to itself. If this preference is not met, the agent relocates to an empty spot. Over time, these micro-level decisions generate macro-level segregation patterns without any centralized control.

---

## What is Generative Agent-Based Modeling?

Generative ABM refers to models where:

- Agents possess simple rules to **generate their own behaviors autonomously** based on local information.
- Complex system-wide patterns **emerge naturally** from these interactions.
- The modeler does not hard-code global outcomes; instead, agents’ micro-decisions **generate** the observed phenomena.

Schelling’s model is generative because each agent independently decides whether to move, and these individual choices collectively produce the emergent segregation patterns.

---

## Problem Statement

How do individual preferences regarding neighbors cause emergent segregation in urban environments?

- Agents want to live near similar agents.
- Even mild preferences can lead to significant clustering and segregation.
- The model shows segregation can arise without overt discrimination.

---

## Model Description

### Grid

- A 2D square grid represents the neighborhood.
- Each cell may be occupied by an agent from one of several groups or be empty.

### Agents

- Assigned to groups (e.g., Red, Blue, Green), identified by integers.
- Agents have no global view; they only observe their local neighbors.

### Key Variables & Parameters

| Variable / Parameter      | Description                                             |
|--------------------------|---------------------------------------------------------|
| `grid_size`              | Size of the square grid (e.g., 50x50 cells)             |
| `populations`            | List of fractions representing relative size of each agent group (e.g., `[0.3, 0.5, 0.2]`) |
| `EMPTY`                  | Integer representing empty cells (default 0)            |
| `tolerance`              | Minimum fraction of similar neighbors for agent to be happy (e.g., 0.3) |
| `max_iters`              | Maximum number of iterations/steps for simulation       |
| `GROUP_IDS`              | Internal IDs assigned to agent groups starting from 1   |

### Agent Behavior

- Agents inspect neighbors in a **Moore neighborhood** (adjacent 8 cells).
- Calculate fraction of neighbors belonging to the same group.
- If fraction < `tolerance`, agent is unhappy and moves to a random empty cell.
- Otherwise, agent stays put.

---

## How to Run

1. Clone this repository:

```bash
git clone https://github.com/FarshadAmiri/ComplexSystems_playground/
cd schelling-abm
