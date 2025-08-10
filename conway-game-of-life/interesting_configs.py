# Classic Conway's Game of Life
classic_life = {
    "grid_size": 100,
    "init_mode": "random",
    "init_density": 0.15,
    "rule_b": [3],
    "rule_s": [2, 3],
    "max_iters": 1000,
    "delay": 0.2,
    "wrap": True
}

# Maze generation rules – converges to maze-like stable patterns
maze_like = {
    "grid_size": 50,
    "init_mode": "random",
    "init_density": 0.15,
    "rule_b": [2],
    "rule_s": [1, 2, 3],
    "max_iters": 1000,
    "delay": 0.2,
    "wrap": True
}

# HighLife – like Life but allows birth on 6 → creates replicators
# Famous for its "replicator" patterns
highlife = {
    "grid_size": 80,
    "init_mode": "random",
    "init_density": 0.15,
    "rule_b": [3, 6],
    "rule_s": [2, 3],
    "max_iters": 1000,
    "delay": 0.2,
    "wrap": True
}

# Day & Night – symmetric rule, patterns survive inverted
# Explores symmetry: replacing live with dead and vice versa still works
day_and_night = {
    "grid_size": 80,
    "init_mode": "random",
    "init_density": 0.3,
    "rule_b": [3, 6, 7, 8],
    "rule_s": [3, 4, 6, 7, 8],
    "max_iters": 1000,
    "delay": 0.2,
    "wrap": True
}

# Seeds – explosive chaos, no survival at all
# Famous for explosive growth from small seeds
seeds = {
    "grid_size": 80,
    "init_mode": "random",
    "init_density": 0.05,
    "rule_b": [2],
    "rule_s": [],
    "max_iters": 500,
    "delay": 0.2,
    "wrap": True
}

# Coral Growth – produces coral-like organic growth patterns
coral_growth = {
    "grid_size": 80,
    "init_mode": "random",
    "init_density": 0.2,
    "rule_b": [3],
    "rule_s": [4, 5, 6, 7, 8],
    "max_iters": 1000,
    "delay": 0.15,
    "wrap": True
}

# Amoeba – chaotic amoeba-like blobs
amoeba = {
    "grid_size": 80,
    "init_mode": "random",
    "init_density": 0.3,
    "rule_b": [3, 5, 7],
    "rule_s": [1, 3, 5, 8],
    "max_iters": 1000,
    "delay": 0.2,
    "wrap": True
}

# 2x2 – behaves like a block cellular automaton
two_by_two = {
    "grid_size": 80,
    "init_mode": "random",
    "init_density": 0.15,
    "rule_b": [3, 6],
    "rule_s": [1, 2, 5],
    "max_iters": 1000,
    "delay": 0.2,
    "wrap": True
}
