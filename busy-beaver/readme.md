# Busy Beaver Random Search

This notebook (`bb.ipynb`) performs a Monte Carlo search over small 2‑symbol Turing machines to find candidates that maximize either (a) number of 1s written on halt (Σ-like) or (b) steps executed before halting (S-like).

Problem summary:
Given n states and alphabet {0,1}, each (state, read_symbol) transition maps to (write_symbol, move ∈ {l,r}, next_state | halt). Σ(n) and S(n) grow faster than any computable function; exact values are known only for small n, so we resort to stochastic sampling.

### Implementation outline:
- States are named a, b, c, ...
- Every (state, symbol) pair receives a random action triple.
- One random transition is converted to a halting transition (next state replaced by literal `halt`).
- Each machine runs up to `max_steps_to_halt`; if it halts earlier we score it; otherwise we discard it.
- Two champions (max ones, max steps) are tracked independently, with full tape histories.

### Core parameters:
- `n`: number of states.
- `iters`: random rule sets sampled.
- `max_steps_to_halt`: per-machine step ceiling.
- `initial_tape`: starting tape (default `["0"]`).
- `initial_head_idx`, `initial_mode`: initial configuration.

Algorithm (per candidate):
1 Initialize tape, head, mode.
2 Loop until halt or step cap:
   a Read symbol.
   b Fetch transition.
   c Write, move (extend tape with 0 if out of bounds).
   d Update mode; record snapshot.
   e Break if mode == `halt`.
3 Update champion metrics if improved.

### Outputs:
- Incremental messages when a new champion appears.
- Final rule set + tape history for max-steps champion.
- Final rule set + tape history for max-ones champion.

### Limitations:
- Random sampling gives no optimality guarantee.
- Forced halt transition may be unreachable.
- No cycle detection; some time lost on periodic non-halting behavior inside the cap.

### Potential extensions (future works):
- Cycle detection (hash of (mode, head, tape_tuple)).
- Persist champions (JSON) + metadata; add seeding CLI.
- Parallel sampling + symmetry/canonical pruning.
- Exhaustive mode for very small n to validate correctness.
