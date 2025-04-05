# Iterated Local Search for Book Scanning Problem

This repository contains an implementation of Iterated Local Search (ILS) algorithm applied to the Google Hash Code Book Scanning problem. The implementation combines ILS with GRASP (Greedy Randomized Adaptive Search Procedure) for initial solution generation and various perturbation strategies.

## Algorithm Overview

### Iterated Local Search (ILS)
The ILS implementation (`iterated_local_search` method) is based on Algorithm 16 "Iterated Local Search (ILS) with Random Restarts" from "Essentials of Metaheuristics" (Luke, 2014, p. 29). The implementation works as follows:

1. **Initial Solution**: Generated using GRASP with a quick local search improvement
2. **Main Loop**: Iterates until reaching time limit or maximum iterations
3. **Local Search Phase**: Variable time limit (5-60 seconds) for each local search phase
4. **Acceptance Criterion**: Uses a history-based acceptance criterion with 10% probability of accepting worse solutions

Key parameters:
- `time_limit`: Maximum running time (default: 300s)
- `max_iterations`: Maximum number of iterations (default: 1000)

### Quick Local Search (Hill Climbing)

The quick local search implementation (`local_search` method) uses a hill climbing approach with multiple neighborhood structures. It runs for a short time (default: 1 second) and applies the following tweak methods with different probabilities:

1. **Swap Signed-Unsigned Libraries** (50% probability):
   - Exchanges a signed library with an unsigned one
   - Maintains solution feasibility by recalculating book assignments
   - Can be biased to favor first or second half of signed libraries

2. **Swap Same Books** (10% probability):
   - Exchanges positions of two libraries while preserving their book assignments
   - Useful for improving library ordering without changing book assignments

3. **Crossover** (20% probability):
   - Shuffles library order and reassigns books accordingly
   - Creates a new solution by preserving book assignments where possible
   - Helps escape local optima by introducing more diversity

4. **Swap Last Book** (10% probability):
   - Replaces the last book in a library with a better unassigned book
   - Fine-grained optimization at the book level
   - Particularly effective when high-value books are available

5. **Swap Signed Libraries** (10% probability):
   - Exchanges positions of two signed libraries
   - Maintains solution feasibility by recalculating book assignments
   - Helps optimize library ordering

The hill climbing process:
1. Starts with an initial solution
2. Randomly selects a tweak method based on the defined probabilities
3. Applies the selected tweak to create a neighbor solution
4. Accepts the neighbor if it improves the fitness score
5. Repeats until the time limit is reached

This approach balances exploration of different neighborhood structures with exploitation of promising solutions.

### Perturbation Strategy

The perturbation mechanism (`perturb_solution` method) uses a destroy-and-rebuild strategy:

1. **Destroy Phase**:
   - Randomly selects a subset of signed libraries (1 to 1/3 of total)
   - Removes these libraries from the solution
   - Destroy size is randomly chosen between 1% and ~33.33% of signed libraries

2. **Rebuild Phase**:
   - Calculates scores for unsigned libraries based on:
     - Average book score
     - Books per day
     - Signup time
   - Greedily reinserts libraries based on these scores
   - Maintains solution feasibility regarding time constraints

### Initial Solution Generation (GRASP)

The initial solution is generated using a GRASP approach (`generate_initial_solution_grasp` method) based on Algorithm 108 "Greedy Randomized Adaptive Search Procedures (GRASP)" from "Essentials of Metaheuristics" (Luke, 2014, p. 151). The implementation includes:

1. **Construction Phase**:
   - Sorts libraries by signup days (ascending) and total score (descending)
   - Iteratively builds Restricted Candidate List (RCL)
   - Randomly selects libraries from RCL
   - Maintains feasibility regarding time constraints

2. **Local Search Improvement**:
   - Applies quick local search (1 second)
   - Uses multiple neighborhood structures:
     - Swap signed libraries
     - Swap signed with unsigned libraries
     - Crossover operations
     - Book-level tweaks

Parameters:
- `p`: RCL size as percentage (default: 0.05)
- `max_time`: Time limit for GRASP iterations (default: 60s)

## Usage

The solver can be used by creating an instance of the `Solver` class and calling the `iterated_local_search` method:

```python
solver = Solver()
best_score, best_solution = solver.iterated_local_search(
    data,
    time_limit=300,    # 5 minutes
    max_iterations=1000
)
```

## Implementation Details

The implementation uses several neighborhood structures for local search:

1. **Swap Signed**: Exchanges positions of two signed libraries
2. **Swap Signed-Unsigned**: Exchanges a signed library with an unsigned one
3. **Crossover**: Shuffles library order and reassigns books
4. **Book-level Tweaks**: Fine-grained adjustments to book assignments

The algorithm maintains solution feasibility throughout all operations and uses efficient data structures (sets, dictionaries) for book tracking and score calculations.

## Performance Considerations

- Uses adaptive time limits for local search phases
- Implements efficient book tracking using sets
- Maintains solution feasibility during all operations
- Combines multiple neighborhood structures
- Uses history-based acceptance criteria to escape local optima

The implementation balances exploration (through perturbation and acceptance criteria) with exploitation (through local search and greedy components) to effectively search the solution space.

## References

Luke, S. (2014). Essentials of Metaheuristics (2nd ed., Version 2.1). George Mason University. Retrieved from https://cs.gmu.edu/~sean/book/metaheuristics/
- Algorithm 16: Iterated Local Search (ILS) with Random Restarts (p. 29)
- Algorithm 108: Greedy Randomized Adaptive Search Procedures (GRASP) (p. 151)
