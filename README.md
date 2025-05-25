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


### Instance-Aware Adaptations

The algorithm adaptively adjusts its behavior based on instance characteristics:

1. **Small vs. Large Instances**:
   - Small instances: More intensive local search (longer time, more iterations)
   - Large instances: Faster, less intensive local search but more iterations

2. **Stagnation-Responsive Perturbation**:
   - Low stagnation: Balanced perturbation strategies
   - High stagnation: More disruptive perturbations

3. **Dynamic Perturbation Sizing**:
   - Size of perturbation increases with stagnation level
   - Small instances: 5-20% of libraries perturbed
   - Large instances: 10-33% of libraries perturbed

### Quick Local Search (Hill Climbing)

The quick local search implementation (`local_search` method) uses a hill climbing approach with multiple neighborhood structures. It runs for a random time and applies the following tweak methods with different probabilities:

1. **Swap Signed-Unsigned Libraries** (30% probability):
   - Exchanges a signed library with an unsigned one
   - Maintains solution feasibility by recalculating book assignments
   - Can be biased to favor first or second half of signed libraries

2. **Swap Same Books** (10% probability):
   - Exchanges positions of two libraries while preserving their book assignments
   - Useful for improving library ordering without changing book assignments

3. **Crossover** (10% probability):
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

6. **Insert Library** (20% probability):
   - Moves a library to a different position in the signed libraries list
   - Entirely rebuilds the solution from that point
   - Powerful operator for restructuring solutions

7. **Swap Neighbor Libraries** (10% probability):
   - Swaps adjacent libraries in the signed libraries list
   - Less disruptive than random swaps
   - Fine-tunes the library ordering

The hill climbing process:
1. Starts with an initial solution
2. Randomly selects a tweak method based on the defined probabilities
3. Applies the selected tweak to create a neighbor solution
4. Accepts the neighbor if it improves the fitness score
5. Repeats until the time limit is reached

This approach balances exploration of different neighborhood structures with exploitation of promising solutions.

### Perturbation Strategy

The perturbation mechanism (`perturb_solution` method) uses three main strategies:

1. **Remove-Insert Strategy** (40-60% probability):
   - Randomly selects a subset of signed libraries
   - Removes these libraries from the solution
   - Calculates scores for unsigned libraries based on efficiency metrics
   - Greedily reinserts libraries based on these scores

2. **Reorder Strategy** (30-40% probability):
   - Reorders libraries based on different criteria:
     - Random reordering
     - Efficiency-based reordering
     - Partial reordering of specific segments

3. **Shuffle Strategy** (10-20% probability):
   - Completely shuffles the signed libraries list
   - More disruptive perturbation for escaping deep local optima
   - Used more frequently when stagnation is detected

The strategy selection adapts to the search progress:
- Early stages: More balanced strategy distribution
- Stagnation phases: More disruptive strategies (remove-insert, shuffle)
- Small instances: More focused perturbations

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

Additional initial solution methods are implemented for comparison:
1. **Sorted** - Simple greedy approach based on signup days and total score
2. **Greedy** - Priority queue based on library efficiency
3. **Weighted Efficiency** - Parameterized approach with tunable alpha and beta values

### Additional Methods for Initial Solution Generation

In addition to GRASP, the implementation includes several other methods for generating initial solutions. Below are the explanations and formulas for each:

#### 1. Sorted (Greedy by Sorting)

**Idea:**
- Libraries are simply sorted by signup days (ascending) and total book scores (descending).
- Libraries are selected one by one, ensuring that the day limit is not exceeded and no books are scanned twice.

**Sorting Formula:**

```text
sorting = (signup_days, -sum(score_b for each b in lib.books))
```

**Steps:**
1. Sort libraries according to the formula above.
2. For each library, if there is enough time for signup, select the most valuable books that have not been scanned yet.
3. Update the list of scanned books and the remaining time.

**Advantages:**
- Very fast and simple.
- Yields good results for small instances.

**Limitations:**
- Does not account for library efficiency in relation to time.

---

#### 2. Greedy Heap (Efficiency via Heap)

**Idea:**
- Uses a heap (priority queue) to always select the library with the highest efficiency.
- Efficiency is calculated as the ratio of maximum possible scores to signup days.

**Efficiency Formula:**

```text
efficiency = sum(score_b for each b in top books) / signup_days
```

where "top books" are the most valuable books that can be scanned within the remaining time.

**Steps:**
1. For each library, calculate the efficiency according to the formula.
2. Add all libraries to the heap based on efficiency.
3. In each step, select the library with the highest efficiency, update scanned books and time.
4. Update the heap if necessary.

**Advantages:**
- Considers the ratio between scores and signup time.
- Yields good results for large instances.

**Limitations:**
- May overlook libraries with few signup days but many valuable books.

---

#### 3. Weighted Efficiency (Efficiency via Weights and Penalty)

**Idea:**
- Improves the greedy approach by penalizing libraries that are selected later or have many signup days.
- Uses two tunable parameters: α (alpha) and β (beta) to balance the penalty.

**Weighted Efficiency Formula:**

```text
weighted_efficiency = sum(score_b for each b in top books) / (signup_days^alpha * (1 + beta * used))
```

where:
- top books: the most valuable books that can be scanned within the remaining time
- alpha: controls how strongly signup days are penalized
- beta: penalizes libraries that are selected later (used is the number of libraries selected so far)

**Steps:**
1. For each library, calculate the weighted efficiency according to the formula.
2. Always select the library with the highest weighted_efficiency value.
3. Update scanned books, time, and the number of used libraries.
4. Parameters α and β can be automatically tuned for better results.

**Advantages:**
- High flexibility through parameters.
- Yields very good results across different instances.

**Limitations:**
- Requires parameter tuning for optimal performance.

---

These methods are used to generate different initial solutions, which are then improved with local search and perturbation. The choice of the best method depends on the instance characteristics and tuned parameters.

## Multiple Solution Handling

The system processes multiple problem instances in sequence:

1. **Batch Processing**:
   - Iterates through all input files in the `input` directory
   - Runs ILS on each instance with the same parameters
   - Exports solutions to the `output` directory

2. **Validation**:
   - Automatically validates all generated solutions
   - Checks for validity constraints (time limits, library capacities)
   - Provides a summary of valid and invalid solutions

3. **Results Summary**:
   - Generates a comprehensive summary of all instance results
   - Creates a `summary_results.txt` file with scores for each instance
   - Displays formatted results in the console

## Usage

The solver can be used by creating an instance of the `Solver` class and calling the `iterated_local_search` method:

```python
solver = Solver()
result = solver.iterated_local_search(
    data,
    time_limit=300,    # 5 minutes
    max_iterations=1000
)
result.export("output/solution.txt")
```

To run the entire pipeline on all input files:

```python
python app.py
```

## Implementation Details

The implementation uses several key data structures:

1. **Solution Representation**:
   - `signed_libraries`: List of scheduled library IDs in processing order
   - `unsigned_libraries`: List of unscheduled library IDs
   - `scanned_books_per_library`: Dictionary mapping library IDs to their scanned books
   - `scanned_books`: Set of all scanned book IDs

2. **Library Efficiency Calculation**:
   ```
   efficiency = (score_potential * 0.6 + unique_ratio * 0.2 + time_efficiency * 0.2)
   ```
   where:
   - `score_potential`: Sum of scores of unscanned books in the library
   - `unique_ratio`: Proportion of unique books in the library
   - `time_efficiency`: Books per day / signup days

3. **Adaptive Parameter Tuning**:
   - Local search time allocation adapts based on remaining time
   - Perturbation size increases with stagnation level
   - Strategy selection probabilities change during search

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

Algorithms inspired by nature 2025 class repository available on https://github.com/ArianitHalimi/AIN_25
- Tweak operators used from this repository
