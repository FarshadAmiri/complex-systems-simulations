import random

n = 2
iters = 50000
max_steps_to_halt = 100

initial_tape = ["0"]
initial_head_idx = 0
initial_mode = "a"

write_set = ["0", "1"]
move_set = ["l", "r"]
next_mode_set = [chr(97+i) for i in range(n)]

state_set = []
for i in next_mode_set:
    for j in write_set:
        state_set.append((i, j))
        

def generate_rules(state_set, write_set, move_set, next_mode_set):
    rules_set = dict()
    halt_state = random.choice(state_set)
    for state in state_set:
        write_act = random.choice(write_set)
        move_act = random.choice(move_set)
        next_mode_act = random.choice(next_mode_set)
        rules_set[state] = [write_act, move_act, next_mode_act]
    rules_set[halt_state][-1] = "halt"  # Define halt state
    return rules_set

def simulate_turing_machine(rules_set, tape, head_idx, mode):
    current_symbol = tape[head_idx]
    
    write_symbol, move_direction, mode = rules_set[(mode, current_symbol)]
    tape[head_idx] = write_symbol

    if move_direction == "r":
        head_idx += 1
    elif move_direction == "l":
        head_idx -= 1

    if head_idx < 0:
        tape.insert(0, "0")
        head_idx = 0
    if head_idx >= len(tape):
        tape.insert(len(tape), "0")
        head_idx = len(tape) - 1

    return (tape, head_idx, mode)


max_score = 0
max_shifts = 0

tape = initial_tape.copy()
head_idx = initial_head_idx
mode = initial_mode
score = 0
shifts = 0
tape_history = []

rules_set = {
        ('a', '0'): ['1', 'l', 'b'],
        ('a', '1'): ['0', 'r', 'b'],
        ('b', '0'): ['1', 'r', 'a'],
        ('b', '1'): ['0', 'l', 'halt']
 }

for i in range(max_steps_to_halt):
    new_tape = tape.copy()
    tape_history.append(new_tape)
    tape, head_idx, mode = simulate_turing_machine(rules_set, tape, head_idx, mode)
    
    score = tape.count("1")
    shifts = i+1

    if mode == "halt":
        if score > max_score:
            max_score = score
            print(f"score: {score}")

        if shifts > max_shifts:
            max_shifts = shifts
            best_rules = rules_set
            best_tape = tape_history
            print(f"shift: {shifts}")
        
        break

tape_history