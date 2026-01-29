# ABC ONLOOKER PHASE - COMPLETE LINE-BY-LINE DEEP DIVE

## Purpose of This Document
This document provides an **exhaustive, line-by-line** explanation of the Onlooker Bee Phase in the Artificial Bee Colony algorithm. Every single line of code is analyzed for both **conceptual reasoning** (why it exists) and **syntactic details** (how Python executes it).

---

## TABLE OF CONTENTS
1. [High-Level Concept: What Are Onlooker Bees?](#high-level-concept)
2. [Phase 1: Ranking Solutions (Lines 1-6)](#phase-1-ranking)
3. [Phase 2: Converting Ranks to Probabilities (Lines 8-13)](#phase-2-probabilities)
4. [Phase 3: Probabilistic Selection and Mutation (Lines 15-30)](#phase-3-selection)
5. [Complete Worked Example](#worked-example)
6. [Exam-Style Questions and Answers](#exam-questions)

---

## HIGH-LEVEL CONCEPT

### What Are Onlooker Bees?

In the biological metaphor:
- **Employed bees** = Bees that have a food source and exploit it
- **Onlooker bees** = Bees that watch the employed bees' "waggle dance" and decide which food source to visit based on quality
- **Scout bees** = Bees that search for entirely new food sources

### Why Do We Need Onlooker Bees?

**Problem**: If we only have employed bees, each solution gets equal attention regardless of quality.
- Bad solutions waste computational effort
- Good solutions don't get exploited enough

**Solution**: Onlooker bees allocate effort proportionally to solution quality.
- Better solutions → more onlookers → faster improvement
- Worse solutions → fewer onlookers → less wasted effort

### What Happens in the Onlooker Phase?

**Three steps**:
1. **Rank** all solutions (how good is each one?)
2. **Calculate probabilities** (how likely should each be selected?)
3. **Select and mutate** (choose solutions probabilistically, try to improve them)

**Key difference from Employed Phase**:
- Employed: Each solution gets exactly 1 mutation attempt
- Onlooker: Good solutions may get multiple attempts, bad solutions may get zero

---

## PHASE 1: RANKING

### Complete Code Block

```python
a = [0] * NP
for i in range(NP):
    for j in range(NP):
        if Costs[i] <= Costs[j]:
            a[i] += 1
```

---

### LINE 1: `a = [0] * NP`

#### Syntax Analysis

**What it does**: Creates a list of length `NP` where every element is `0`.

**Breakdown**:
- `[0]`: A list containing one element (the integer 0)
- `* NP`: List repetition operator
- Result: `[0, 0, 0, ..., 0]` with `NP` elements

**Example** (`NP = 3`):
```python
a = [0] * 3
# Result: a = [0, 0, 0]
```

**Why not `a = []` and append?**
- Pre-allocation is faster (Python knows final size)
- Indexing is cleaner (`a[i] += 1` vs `a.append()`)

---

#### Conceptual Justification

**Purpose**: Initialize ranking scores for all solutions.

**What does `a[i]` represent?**
- The "dominance score" of solution `i`
- Higher score = better solution
- Specifically: "How many solutions does solution i beat or tie?"

**Why initialize to 0?**
- We're about to count victories via `+=`
- Starting from 0 ensures accurate counting

**Exam question**: "Why create a separate list `a` instead of modifying `Costs`?"
**Answer**: "We need both the raw costs (for comparisons) and the derived ranks (for probabilities). Keeping them separate maintains clarity and prevents accidental overwriting of cost data."

---

### LINE 2: `for i in range(NP):`

#### Syntax Analysis

**What it does**: Loop over indices 0, 1, 2, ..., NP-1.

**Breakdown**:
- `range(NP)`: Generator producing integers from 0 to NP-1 (exclusive of NP)
- `for i in ...`: Assigns each value to variable `i` sequentially
- Colon `:` starts indented block

**Example** (`NP = 3`):
```python
for i in range(3):
    print(i)
# Prints: 0, 1, 2
```

**Why `range(NP)` instead of `range(len(Solutions))`?**
- They're equivalent (`NP = len(Solutions)`)
- Using `NP` is cleaner (fewer function calls)

---

#### Conceptual Justification

**Purpose**: Iterate through each solution to calculate its rank.

**What does `i` represent?**
- The index of the solution being ranked
- Example: When `i=0`, we're calculating the rank of `Solutions[0]`

**Why loop through all solutions?**
- Each solution needs a rank
- Rank is relative (depends on comparing with all others)

**Exam question**: "Could we use `for solution in Solutions:` instead?"
**Answer**: "No, because we need the index `i` to store the rank in `a[i]`. Using enumerate like `for i, solution in enumerate(Solutions):` would work, but using `range(NP)` is simpler since we already have indexed lists."

---

### LINE 3: `for j in range(NP):`

#### Syntax Analysis

**What it does**: Nested loop over indices 0, 1, 2, ..., NP-1.

**Breakdown**:
- This is a **nested loop** (loop inside a loop)
- `j` is a separate loop variable from `i`
- For each value of `i`, this loop runs completely

**Example** (`NP = 3`):
```python
for i in range(3):
    for j in range(3):
        print(f"i={i}, j={j}")
# Prints: (0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)
```

**Execution flow**:
```
i=0: j loops through 0, 1, 2
i=1: j loops through 0, 1, 2
i=2: j loops through 0, 1, 2
```

**Total iterations**: `NP × NP = NP²`

---

#### Conceptual Justification

**Purpose**: Compare solution `i` against every solution (including itself).

**What does `j` represent?**
- The index of the solution being compared against
- Example: When `i=0, j=2`, we're comparing `Solutions[0]` vs `Solutions[2]`

**Why nested loop?**
- To calculate rank, we must compare solution `i` against ALL other solutions
- Each comparison is independent
- Nested structure ensures all pairs are compared

**Why compare against itself (`i == j`)?**
- Ensures every solution gets at least score 1
- A solution always "beats or ties" itself
- Prevents zero ranks (which would cause division issues later)

**Exam question**: "This is O(N²) complexity. Could we optimize it?"
**Answer**: "Yes, sorting would be O(N log N), but for small populations (NP=10-20), the simplicity of pairwise comparison outweighs the overhead of sorting. Additionally, this rank-based approach (counting victories) is more intuitive than index-based approaches and handles ties naturally."

---

### LINE 4: `if Costs[i] <= Costs[j]:`

#### Syntax Analysis

**What it does**: Check if cost of solution `i` is less than or equal to cost of solution `j`.

**Breakdown**:
- `Costs[i]`: Cost (in euros) of solution `i`
- `<=`: Less than or equal comparison operator
- `Costs[j]`: Cost (in euros) of solution `j`
- Returns `True` or `False`

**Example**:
```python
Costs = [1200, 1100, 1250]
i = 1
j = 0

if Costs[i] <= Costs[j]:  # 1100 <= 1200 → True
    print("Solution i is better or equal")
```

**Why `<=` instead of `<`?**
- `<=` includes ties (solutions with equal cost)
- Both solutions get credit for the tie
- `<` would only count strict victories

---

#### Conceptual Justification

**Purpose**: Determine if solution `i` beats or ties solution `j`.

**Remember**: Lower cost = better solution
- `Costs[i] <= Costs[j]` means "i is at least as good as j"
- If true → solution `i` gets a point

**Why this direction?**
- We're minimizing cost (not maximizing)
- `<=` means "i is better or equal to j"
- Each victory/tie adds 1 to `a[i]`

**What happens with ties?**
- If `Costs[i] == Costs[j]`, condition is true
- Both solutions get credit (when it's their turn as `i`)
- Fair: tied solutions should have equal ranks

**Exam question**: "What if we used `Costs[i] < Costs[j]` (strict inequality)?"
**Answer**: "Solutions would only get points for strict victories, not ties. A solution equal to all others would get rank 0 (only from self-comparison at i==j... wait, that would also be false!). Actually, with `<`, a solution only gets credit when `i==j` is false and `Costs[i] < Costs[j]`, so it would never count the self-comparison. The minimum score would be 0 (worst solution) instead of 1. We use `<=` to ensure every solution scores at least 1 (from self-comparison), which prevents probability calculation issues."

---

### LINE 5: `a[i] += 1`

#### Syntax Analysis

**What it does**: Increment the rank score of solution `i` by 1.

**Breakdown**:
- `a[i]`: Current rank score of solution `i`
- `+=`: In-place addition operator
- `1`: The increment value
- Equivalent to: `a[i] = a[i] + 1`

**Example**:
```python
a = [0, 0, 0]
i = 1

a[i] += 1  # a[1] = a[1] + 1 = 0 + 1 = 1
# Result: a = [0, 1, 0]
```

**Why `+=` instead of `= a[i] + 1`?**
- More concise
- Standard Python idiom for increment
- Slightly more efficient (one less lookup)

---

#### Conceptual Justification

**Purpose**: Award solution `i` one point for beating/tying solution `j`.

**What does this build?**
- After all comparisons, `a[i]` = number of solutions that `i` beats or ties
- Range: 1 (worst, only beats itself) to NP (best, beats all)

**Example** (`NP=3`, `Costs=[1200, 1100, 1250]`):

**For i=0 (Cost=1200)**:
- j=0: 1200 ≤ 1200 → True → a[0] += 1 (a[0]=1)
- j=1: 1200 ≤ 1100 → False → no increment
- j=2: 1200 ≤ 1250 → True → a[0] += 1 (a[0]=2)
- **Final: a[0] = 2**

**For i=1 (Cost=1100, best)**:
- j=0: 1100 ≤ 1200 → True → a[1] += 1 (a[1]=1)
- j=1: 1100 ≤ 1100 → True → a[1] += 1 (a[1]=2)
- j=2: 1100 ≤ 1250 → True → a[1] += 1 (a[1]=3)
- **Final: a[1] = 3** (beats all)

**For i=2 (Cost=1250, worst)**:
- j=0: 1250 ≤ 1200 → False → no increment
- j=1: 1250 ≤ 1100 → False → no increment
- j=2: 1250 ≤ 1250 → True → a[2] += 1 (a[2]=1)
- **Final: a[2] = 1** (only beats itself)

**Result**: `a = [2, 3, 1]`

**Exam question**: "Why count victories instead of just sorting by cost?"
**Answer**: "Counting victories naturally handles the ranking without needing to assign explicit rank numbers. It's also more robust: if we sorted and used indices, we'd need to maintain a mapping back to original solution indices. This pairwise counting approach keeps everything indexed consistently with the original `Solutions` and `Costs` lists."

---

### AFTER LINE 5: What Have We Accomplished?

**Output**: List `a` where `a[i]` = rank score of solution `i`

**Properties**:
- Sum of all `a[i]` = NP × NP (or something close, due to ties)
- Wait, let me recalculate...

**Careful Analysis**:
Actually, let's think about what `sum(a)` equals:
- Each of the `NP × NP` comparisons adds 1 to some `a[i]`
- But only half (roughly) add 1 (when condition is true)

**Actually, no. Let's trace carefully**:
For every pair (i, j):
- If `Costs[i] ≤ Costs[j]`, we increment `a[i]`
- If `Costs[j] ≤ Costs[i]`, we increment `a[j]` (in a different iteration)

**Key insight**: For any pair where costs differ:
- One solution gets a point (the better one)
- For ties, both get a point (when each is `i`)

**Sum analysis**:
```
sum(a) = sum over all i of (number of j where Costs[i] ≤ Costs[j])
```

Let me think differently:
- There are NP solutions
- Each solution compares against NP solutions (including itself)
- For each comparison where `Costs[i] ≤ Costs[j]`, `a[i]` increments

**Actually, the exact sum depends on the cost distribution**:
- If all costs are equal: Each solution beats all → `a[i] = NP` for all i → `sum(a) = NP²`
- If all costs are different: Winner beats NP, second beats NP-1, ..., loser beats 1 → `sum(a) = NP + (NP-1) + ... + 1 = NP(NP+1)/2`

**Example** (`NP=3`, `Costs=[1200, 1100, 1250]`):
- a = [2, 3, 1]
- sum(a) = 6 = 3(3+1)/2 ✓

**For probability calculation**: We normalize by `sum(a)`, so the exact value doesn't matter!

---

## PHASE 2: PROBABILITIES

### Complete Code Block

```python
SumA = sum(a)
if SumA == 0:
    Prob = [1.0 / NP] * NP
else:
    Prob = [ai / SumA for ai in a]
```

---

### LINE 8: `SumA = sum(a)`

#### Syntax Analysis

**What it does**: Calculate the sum of all elements in list `a`.

**Breakdown**:
- `sum()`: Built-in Python function
- `a`: List of integers (rank scores)
- Returns: Single integer (total of all ranks)

**Example**:
```python
a = [2, 3, 1]
SumA = sum(a)  # 2 + 3 + 1 = 6
```

**Equivalent code**:
```python
SumA = 0
for ai in a:
    SumA += ai
```

**Why use `sum()` instead of manual loop?**
- More readable
- Faster (implemented in C)
- Less error-prone

---

#### Conceptual Justification

**Purpose**: Get normalization constant for probability calculation.

**Why do we need the sum?**
- To convert raw ranks into probabilities (must sum to 1.0)
- Formula: `Prob[i] = a[i] / sum(a)`

**What does `SumA` represent?**
- Total "ranking points" distributed across all solutions
- Used as denominator to normalize

**Exam question**: "Could `SumA` ever be zero in normal operation?"
**Answer**: "No, because every solution gets at least 1 point from the self-comparison (when i==j, `Costs[i] ≤ Costs[i]` is always true). Minimum `SumA = NP × 1 = NP`. The zero-check is defensive programming for potential bugs."

---

### LINE 9: `if SumA == 0:`

#### Syntax Analysis

**What it does**: Check if `SumA` equals zero.

**Breakdown**:
- `if`: Conditional statement
- `SumA == 0`: Boolean expression using equality operator
- `:`: Starts conditional block

**Returns**: `True` or `False`

**Example**:
```python
SumA = 6
if SumA == 0:  # 6 == 0 → False
    print("This won't execute")
```

**Why `==` and not `=`?**
- `==`: Comparison (returns True/False)
- `=`: Assignment (stores value)
- Common mistake: `if SumA = 0:` is a syntax error

---

#### Conceptual Justification

**Purpose**: Handle edge case where ranking failed.

**When would this be true?**
- **Never in correct implementation** (as explained above)
- But could happen if:
  - Bug in ranking code
  - List `a` somehow got cleared
  - Floating-point error (if `a` had floats)

**Why handle this case?**
- **Defensive programming**: Prevent division by zero
- Better to have graceful degradation than crash
- Easy to debug: if probabilities are uniform, you know ranking failed

**Exam question**: "Is this check necessary?"
**Answer**: "Strictly speaking, no—it's impossible in correct code. However, it's good defensive programming. If someone modifies the ranking logic and introduces a bug, this prevents a catastrophic crash (division by zero) and instead falls back to uniform probabilities, making the bug obvious during testing."

---

### LINE 10: `Prob = [1.0 / NP] * NP`

#### Syntax Analysis

**What it does**: Create list of uniform probabilities.

**Breakdown**:
- `1.0 / NP`: Float division (each solution gets equal probability)
- `[...]`: Creates single-element list
- `* NP`: Repeats list NP times

**Example** (`NP=3`):
```python
Prob = [1.0 / 3] * 3
# Prob = [0.333...] * 3 = [0.333..., 0.333..., 0.333...]
```

**Why `1.0` instead of `1`?**
- `1.0`: Float literal
- `1 / NP`: In Python 3, this is float division (returns float)
- `1.0 / NP`: Explicit float division (clearer intent)
- Result is same, but `1.0` is more explicit about type

**Why `* NP` instead of loop?**
- Concise
- Same result as `[1.0/NP for _ in range(NP)]`
- Idiomatic Python

---

#### Conceptual Justification

**Purpose**: Fallback to uniform selection if ranking fails.

**What do uniform probabilities mean?**
- Every solution has equal chance of selection
- Equivalent to random search
- No exploitation of quality information

**Why `1/NP` specifically?**
- Probabilities must sum to 1.0
- `NP × (1/NP) = 1.0` ✓
- Each solution gets `1/NP` chance

**Example** (`NP=3`):
- `Prob = [0.333, 0.333, 0.333]`
- Sum = 1.0
- Each solution: 33.3% selection chance

**Exam question**: "Why fallback to uniform instead of, say, raising an error?"
**Answer**: "Uniform selection degrades gracefully—the algorithm continues running, just without quality-based selection bias. This is better than crashing. Additionally, uniform selection is equivalent to random search, which, while inefficient, can still find solutions. Raising an error would halt the optimization entirely."

---

### LINE 11: `else:`

#### Syntax Analysis

**What it does**: Alternate branch if `SumA != 0`.

**Breakdown**:
- `else`: Python keyword for fallback branch
- `:`: Starts alternate block
- Executes only if `if` condition was `False`

**Control flow**:
```
if SumA == 0:
    # Execute this block
else:
    # OR execute this block (never both)
```

---

#### Conceptual Justification

**Purpose**: Normal case (ranking succeeded).

**When does this execute?**
- Always in correct implementation
- When `SumA > 0` (ranking worked)

---

### LINE 12: `Prob = [ai / SumA for ai in a]`

#### Syntax Analysis

**What it does**: Create list of normalized probabilities using list comprehension.

**Breakdown**:
- `[... for ai in a]`: List comprehension (loops over `a`)
- `ai`: Each element of `a` (current rank score)
- `ai / SumA`: Divide each rank by total (normalize)
- Result: List of floats (probabilities)

**Example** (`a=[2,3,1]`, `SumA=6`):
```python
Prob = [ai / SumA for ai in a]
# Iteration 1: ai=2 → 2/6 = 0.333
# Iteration 2: ai=3 → 3/6 = 0.500
# Iteration 3: ai=1 → 1/6 = 0.167
# Result: Prob = [0.333, 0.500, 0.167]
```

**Equivalent loop**:
```python
Prob = []
for ai in a:
    Prob.append(ai / SumA)
```

**Why list comprehension?**
- More Pythonic
- Faster (optimized internally)
- Clearer intent (transform each element)

---

#### Conceptual Justification

**Purpose**: Convert raw ranks into valid probabilities.

**What does normalization achieve?**
- Raw ranks: Arbitrary scale (e.g., [2, 3, 1])
- Probabilities: Standard scale (sum to 1.0)
- Formula: `P(i) = rank(i) / sum(ranks)`

**Why divide by sum?**
- Makes probabilities sum to 1.0 (required for probability distribution)
- Preserves relative ratios
- Example: rank 3 is 3× better than rank 1 → 3× higher probability

**Verification** (`Prob=[0.333, 0.500, 0.167]`):
- Sum: 0.333 + 0.500 + 0.167 = 1.0 ✓
- Ratio: 0.500 / 0.167 ≈ 3.0 = 3/1 ✓ (preserves rank ratio)

**What does `Prob[i]` represent?**
- Probability that solution `i` will be selected by an onlooker bee
- Higher cost → lower rank → lower probability
- Lower cost → higher rank → higher probability

**Example interpretation**:
- `Prob[1] = 0.500`: Solution 1 has 50% chance of selection
- `Prob[2] = 0.167`: Solution 2 has 16.7% chance of selection
- Solution 1 is 3× more likely to be selected

**Exam question**: "Why use rank-based probabilities instead of cost-based?"
**Answer**: "Rank-based is more robust: (1) Cost magnitude doesn't matter (€10k vs €11k has same effect as €1k vs €1.1k), (2) Outliers don't dominate (one super-cheap solution doesn't monopolize selection), (3) Works for any cost scale (no tuning needed). Cost-based like `1/Cost[i]` would require careful scaling and has issues with very small costs approaching infinity."

---

### AFTER LINE 12: What Have We Accomplished?

**Output**: List `Prob` where `Prob[i]` = selection probability of solution `i`

**Properties**:
- All values are positive: `0 < Prob[i] ≤ 1`
- Sum equals 1.0: `sum(Prob) = 1.0`
- Better solutions have higher probabilities
- Worst solution still has non-zero chance (maintains diversity)

**Example** (`NP=3`, `a=[2,3,1]`, `SumA=6`):
```python
Prob = [2/6, 3/6, 1/6] = [0.333, 0.500, 0.167]
```

**Ready for**: Roulette wheel selection

---

## PHASE 3: SELECTION

### Complete Code Block

```python
for onlooker in range(NP):
    k = select_index_by_probability(Prob, rng=rng)
    
    base_solution = Solutions[k]
    base_cost = Costs[k]
    
    candidate_solution = MutateSolution(base_solution, graph, n_rings=N_RINGS, rng=rng)
    candidate_cost, _, _, _ = get_trajectory_cost(candidate_solution, Node_coordinates, t_start=T_START)
    
    if candidate_cost < base_cost:
        Solutions[k] = candidate_solution
        Costs[k] = candidate_cost
        Trials[k] = 0
    else:
        Trials[k] += 1
```

---

### LINE 15: `for onlooker in range(NP):`

#### Syntax Analysis

**What it does**: Loop NP times (once per onlooker bee).

**Breakdown**:
- `for`: Loop keyword
- `onlooker`: Loop variable (counts iterations)
- `range(NP)`: Generates 0, 1, 2, ..., NP-1

**Example** (`NP=3`):
```python
for onlooker in range(3):
    print(f"Onlooker {onlooker}")
# Prints: Onlooker 0, Onlooker 1, Onlooker 2
```

**Why variable name `onlooker`?**
- Semantic: Represents an onlooker bee
- Could be `i`, but `onlooker` is more descriptive
- Not used in loop body (just for counting)

---

#### Conceptual Justification

**Purpose**: Simulate NP onlooker bees choosing and exploiting food sources.

**Why NP onlookers?**
- Standard ABC: Number of onlookers = Number of employed bees = Population size
- Balances computational effort (same as employed phase)
- Each onlooker represents one mutation attempt

**Key difference from employed phase**:
- Employed: Each solution gets exactly 1 attempt
- Onlooker: Selection is probabilistic
  - Good solutions may get multiple attempts
  - Bad solutions may get zero attempts
  - Total attempts = NP (same as employed)

**Example** (`NP=3`):
- Employed phase: Solutions 0, 1, 2 each get 1 mutation
- Onlooker phase: 3 mutations distributed probabilistically
  - Possible: Solution 1 gets 2 attempts, solution 0 gets 1, solution 2 gets 0
  - Distribution depends on `Prob`

**Exam question**: "Why not have more/fewer onlookers than employed bees?"
**Answer**: "It's a design choice. Standard ABC uses equal numbers for balance. More onlookers = more exploitation (focuses on good solutions). Fewer onlookers = less exploitation. The 1:1 ratio is a reasonable default, but could be tuned. Research shows 1:1 works well for most problems."

---

### LINE 16: `k = select_index_by_probability(Prob, rng=rng)`

#### Syntax Analysis

**What it does**: Select a random solution index using roulette wheel.

**Breakdown**:
- `select_index_by_probability`: Function name
- `(Prob, rng=rng)`: Function arguments
  - `Prob`: List of probabilities (positional argument)
  - `rng=rng`: Random number generator (keyword argument)
- Returns: Integer (index of selected solution)
- Assigns result to variable `k`

**Example**:
```python
Prob = [0.333, 0.500, 0.167]
k = select_index_by_probability(Prob, rng=rng)
# Possible results:
# k = 0 (33.3% chance)
# k = 1 (50.0% chance)
# k = 2 (16.7% chance)
```

**Why `rng=rng` syntax?**
- `rng=`: Keyword argument name (in function definition)
- `rng`: Variable being passed (module-level random generator)
- Passes our seeded RNG to function (ensures reproducibility)

---

#### Conceptual Justification

**Purpose**: Probabilistically select a solution for exploitation.

**How does roulette wheel work?**
1. Generate random number `r` in [0, 1)
2. Map `r` to solution based on cumulative probabilities
3. Higher probability → wider segment → more likely selection

**Visual representation**:
```
Prob = [0.333, 0.500, 0.167]

Wheel:
|████████████|████████████████████|██████|
|  Solution 0 |    Solution 1      | Sol 2|
0.0          0.333               0.833  1.0

Random r = 0.6 → Falls in Solution 1 → k = 1
```

**Algorithm** (inside `select_index_by_probability`):
```python
r = rng.random()  # e.g., 0.6
cumulative = 0.0

# Index 0: cumulative = 0 + 0.333 = 0.333
#          r=0.6 > 0.333 → continue

# Index 1: cumulative = 0.333 + 0.500 = 0.833
#          r=0.6 <= 0.833 → return 1

k = 1  # Selected solution
```

**Why probabilistic selection?**
- Focuses effort on promising solutions
- But maintains diversity (bad solutions can still be selected)
- Prevents premature convergence (always a chance to explore)

**Expected selection counts** (over many iterations):
- Solution 0: 33.3% of onlookers
- Solution 1: 50.0% of onlookers
- Solution 2: 16.7% of onlookers

**Exam question**: "What if we always selected the best solution (k = argmin(Costs))?"
**Answer**: "That's 100% exploitation, 0% exploration. Problems: (1) Best solution might be local optimum, (2) No diversity—all onlookers work on same solution (redundant), (3) Other solutions never improve (wasted). Probabilistic selection balances focus (best solution gets most attention) with diversity (others still explored)."

---

### LINE 18: `base_solution = Solutions[k]`

#### Syntax Analysis

**What it does**: Retrieve the selected solution from the population.

**Breakdown**:
- `Solutions[k]`: List indexing (access element at index `k`)
- `Solutions`: List of trajectories (each is a list of node IDs)
- `k`: Index (integer from 0 to NP-1)
- Assigns result to `base_solution`

**Example**:
```python
Solutions = [
    [0, 15, 36, ..., 610],  # Solution 0
    [0, 12, 33, ..., 610],  # Solution 1
    [0, 18, 40, ..., 610]   # Solution 2
]
k = 1
base_solution = Solutions[k]  # [0, 12, 33, ..., 610]
```

**Type of `base_solution`**: List of integers (node IDs)

**Why not modify `Solutions[k]` directly?**
- Clarity: `base_solution` is more readable
- Safety: Prevents accidental modification of original
- Convention: Use temporary variables for intermediate steps

---

#### Conceptual Justification

**Purpose**: Get the trajectory that the onlooker bee will work on.

**What is `base_solution`?**
- The "food source" the onlooker bee chose
- A complete flight path from AMS to JFK
- Will be mutated to try to find improvement

**Why call it "base"?**
- It's the starting point for mutation
- We'll create a `candidate_solution` (mutated version)
- Then compare candidate vs. base

**Exam question**: "Is this assignment by reference or by value?"
**Answer**: "Reference in Python. `base_solution` points to the same list object as `Solutions[k]`. However, we don't modify `base_solution` directly—we create a new list via `MutateSolution()`. This is important: if we did `base_solution.append(x)`, it would modify `Solutions[k]`. But we do `candidate_solution = MutateSolution(base_solution, ...)`, which creates a new list, so no issue."

---

### LINE 19: `base_cost = Costs[k]`

#### Syntax Analysis

**What it does**: Retrieve the cost of the selected solution.

**Breakdown**:
- `Costs[k]`: List indexing (access cost at index `k`)
- `Costs`: List of floats (costs in euros)
- `k`: Same index as previous line
- Assigns result to `base_cost`

**Example**:
```python
Costs = [12000.0, 11500.0, 12200.0]
k = 1
base_cost = Costs[k]  # 11500.0
```

**Type of `base_cost`**: Float (euros)

---

#### Conceptual Justification

**Purpose**: Store the current quality of the selected solution.

**Why do we need this?**
- To compare against mutated solution
- Decision: Accept mutation if `candidate_cost < base_cost`
- Without this, we'd have to use `Costs[k]` in comparison (less clear)

**Why not just use `Costs[k]` directly?**
- Readability: `base_cost` is more semantic
- Performance: Avoids repeated list lookup
- Maintainability: If comparison logic changes, single variable to update

**Exam question**: "Could we compute base_cost from base_solution instead of looking it up?"
**Answer**: "Technically yes—we could call `get_trajectory_cost(base_solution, ...)` again. But that's wasteful: we already computed it in the initialization phase and stored it in `Costs[k]`. Recomputing would involve full physics simulation (wind, fuel, time) for the entire trajectory—expensive! Looking up from `Costs` is O(1) and effectively free."

---

### LINE 21: `candidate_solution = MutateSolution(base_solution, graph, n_rings=N_RINGS, rng=rng)`

#### Syntax Analysis

**What it does**: Create a mutated version of the selected solution.

**Breakdown**:
- `MutateSolution`: Function name (imported from another module)
- Arguments:
  - `base_solution`: Trajectory to mutate (positional)
  - `graph`: Adjacency list (positional)
  - `n_rings=N_RINGS`: Number of rings (keyword, = 29)
  - `rng=rng`: Random generator (keyword, for reproducibility)
- Returns: New list of node IDs (mutated trajectory) or `None` (if mutation failed)
- Assigns result to `candidate_solution`

**Example**:
```python
base_solution = [0, 15, 36, 57, 78, ..., 610]
candidate_solution = MutateSolution(base_solution, graph, n_rings=29, rng=rng)
# Possible result: [0, 15, 42, 63, 84, ..., 610]
#                        ^^  ^^  ^^ (mutated ring + regenerated rest)
```

**Type of `candidate_solution`**: List of integers (or `None`)

---

#### Conceptual Justification

**Purpose**: Generate a neighboring solution to explore.

**What does `MutateSolution` do?** (High-level):
1. Select random ring position in trajectory
2. Replace waypoint at that position with random alternative
3. Regenerate path from mutation point to destination
4. Validate result (correct length, start/end nodes)
5. Return new trajectory (or `None` if failed)

**Why mutate?**
- Pure exploitation: Keep exact same trajectory → No improvement possible
- Mutation: Small change → Explore neighborhood
- If change is improvement → Accept (progress)
- If change is worse → Reject (stay put)

**What makes a good mutation strategy?**
- Small changes (one ring) → Local search
- Random element → Avoids getting stuck
- Validates feasibility → Only returns valid trajectories

**Why might mutation return `None`?**
- Previous node only connects to current waypoint (no alternatives)
- Random path generation gets stuck
- Validation fails (wrong length, etc.)

**Exam question**: "What happens if `MutateSolution` returns `None`?"
**Answer**: "The next line calls `get_trajectory_cost(candidate_solution, ...)`, which would crash if `candidate_solution` is `None`. Looking at the actual code (not shown here), `MutateSolution` is designed to rarely fail—it retries internally. But if it does fail, we'd get an error. Production code should check: `if candidate_solution is None: continue`. This is a weakness in the current implementation—assumes mutation always succeeds."

---

### LINE 22: `candidate_cost, _, _, _ = get_trajectory_cost(candidate_solution, Node_coordinates, t_start=T_START)`

#### Syntax Analysis

**What it does**: Evaluate the cost of the mutated trajectory.

**Breakdown**:
- `get_trajectory_cost`: Function name (imported from another module)
- Arguments:
  - `candidate_solution`: Mutated trajectory (list of node IDs)
  - `Node_coordinates`: Dict mapping node_id → (lat, lon)
  - `t_start=T_START`: Starting time (hours, = 0.0)
- Returns: Tuple of 4 values `(cost_euro, fuel_burn_kg, time_hours, final_weight_kg)`
- **Unpacking**: Assigns first value to `candidate_cost`, ignores others with `_`

**Example**:
```python
result = get_trajectory_cost([0, 15, 36, ..., 610], Node_coordinates, t_start=0.0)
# result = (11450.0, 58200.0, 7.25, 199543.0)

candidate_cost, _, _, _ = result
# candidate_cost = 11450.0
# Other values are discarded
```

**Why four underscores `_, _, _,_`?**
- Function returns 4 values (tuple)
- We only need the first (cost)
- `_` is Python convention for "ignored variable"
- Must have exactly 4 variables on left side to unpack

**Alternative syntax**:
```python
candidate_cost = get_trajectory_cost(...)[0]  # Only take first element
```
But unpacking is more standard.

---

#### Conceptual Justification

**Purpose**: Determine if mutation improved the solution.

**What does `get_trajectory_cost` do?** (High-level):
1. Loop through trajectory edges (node i → node j)
2. For each edge:
   - Calculate distance (Vincenty)
   - Look up wind (weather model)
   - Compute ground speed (TAS + wind)
   - Calculate time (distance / speed)
   - Look up fuel flow (interpolate by weight)
   - Calculate fuel burn (flow × time)
   - Update weight (subtract fuel burn)
   - Calculate costs (fuel cost + time cost + ANSP)
3. Sum all edge costs
4. Apply penalties (if fuel exceeds max or time violates window)
5. Return: (total_cost, total_fuel, total_time, final_weight)

**Why do we need to evaluate?**
- Mutation is random → Could be better or worse
- Need actual cost to decide acceptance
- Can't predict cost without full physics simulation

**Why ignore fuel, time, weight?**
- Decision only needs cost
- Greedy selection: Accept if cheaper
- Other values are used elsewhere (e.g., final reporting, constraint checking in trajectory_cost function)

**How expensive is this?**
- Full physics simulation: ~30 edges × (distance + wind + fuel calculations)
- Most expensive operation in the algorithm
- Why ABC is slower than Dijkstra: Evaluates many candidate solutions

**Exam question**: "Why not cache costs to avoid recomputation?"
**Answer**: "Costs ARE cached—that's what the `Costs` list is! We only recompute for NEW candidate solutions (mutations). The base solution cost is already in `Costs[k]`, which we retrieved as `base_cost`. This function call only evaluates the mutated trajectory, which is new and hasn't been seen before. Caching mutations would require a hash table mapping trajectory → cost, but trajectories are lists (unhashable) and there are too many possibilities to cache effectively."

---

### LINE 24: `if candidate_cost < base_cost:`

#### Syntax Analysis

**What it does**: Check if mutation improved the solution.

**Breakdown**:
- `if`: Conditional keyword
- `candidate_cost < base_cost`: Boolean comparison
- `<`: Less than operator (strict inequality)
- `:`: Starts conditional block

**Example**:
```python
candidate_cost = 11450.0
base_cost = 11500.0

if candidate_cost < base_cost:  # 11450 < 11500 → True
    print("Improvement!")
```

**Why `<` instead of `<=`?**
- Strict improvement required
- Equal cost → Keep original (no benefit to switching)
- Tie-breaking: Prefer established solution

---

#### Conceptual Justification

**Purpose**: Greedy selection—accept only improvements.

**Decision rule**:
- `candidate_cost < base_cost` → Accept mutation
- `candidate_cost >= base_cost` → Reject mutation

**Why greedy?**
- ABC already has exploration (random mutations, scout phase)
- Onlooker phase focuses on exploitation
- Always accepting improvements ensures progress

**What about worse solutions (exploration)?**
- Not accepted in onlooker phase
- Handled by scout phase (replaces abandoned solutions)
- Balance: Onlooker exploits, scout explores

**Why not accept slightly worse solutions (simulated annealing style)?**
- Could help escape local minima
- But adds complexity (need temperature schedule)
- ABC design: Use scouts for exploration instead
- Simpler and equally effective for most problems

**Exam question**: "What if we used `<=` (accept ties)?"
**Answer**: "It wouldn't change much. With ties, we'd update to a different trajectory with same cost. Pros: More diversity (different path, same cost might lead to different neighborhoods). Cons: Extra work (update Solutions[k]) for no benefit. Using `<` is more efficient—only update when there's actual improvement."

---

### LINE 25: `Solutions[k] = candidate_solution`

#### Syntax Analysis

**What it does**: Replace old solution with improved mutation.

**Breakdown**:
- `Solutions[k]`: List element at index `k`
- `=`: Assignment operator
- `candidate_solution`: New trajectory (mutated version)
- Overwrites `Solutions[k]` with new value

**Example**:
```python
Solutions = [
    [0, 15, 36, ..., 610],  # Solution 0
    [0, 12, 33, ..., 610],  # Solution 1 (old)
    [0, 18, 40, ..., 610]   # Solution 2
]
k = 1
candidate_solution = [0, 12, 42, ..., 610]  # Mutated version

Solutions[k] = candidate_solution

# Result:
Solutions = [
    [0, 15, 36, ..., 610],  # Solution 0 (unchanged)
    [0, 12, 42, ..., 610],  # Solution 1 (updated!)
    [0, 18, 40, ..., 610]   # Solution 2 (unchanged)
]
```

---

#### Conceptual Justification

**Purpose**: Update population with improved solution.

**Why update the population?**
- Keeps best solutions available for future iterations
- Other onlookers can now select improved version
- Progress accumulates over iterations

**What happens to old solution?**
- Lost (overwritten)
- No longer accessible
- Garbage collected by Python

**Is this safe?**
- Yes: We already confirmed improvement (`candidate_cost < base_cost`)
- Won't lose progress (old cost was worse)

**What if multiple onlookers select same solution?**
- Possible! (Probabilistic selection can pick same index)
- First onlooker improves it
- Second onlooker sees improved version (updated `Solutions[k]`)
- Both work on best available version
- This is a FEATURE: Best solutions get most attention

**Exam question**: "Should we make a copy: `Solutions[k] = candidate_solution.copy()`?"
**Answer**: "Not necessary. `candidate_solution` is already a new list (created by `MutateSolution`). There's no aliasing issue—we're not sharing references. Copying would be wasteful (extra memory, no benefit). The assignment here transfers ownership of the new list to `Solutions[k]`."

---

### LINE 26: `Costs[k] = candidate_cost`

#### Syntax Analysis

**What it does**: Update stored cost to match new solution.

**Breakdown**:
- `Costs[k]`: Cost list element at index `k`
- `=`: Assignment
- `candidate_cost`: New cost (already computed)
- Keeps `Costs` synchronized with `Solutions`

**Example**:
```python
Costs = [12000.0, 11500.0, 12200.0]
k = 1
candidate_cost = 11450.0

Costs[k] = candidate_cost

# Result:
Costs = [12000.0, 11450.0, 12200.0]
#                   ^^^^^^^ Updated!
```

---

#### Conceptual Justification

**Purpose**: Maintain consistency between solution and cost lists.

**Why is this critical?**
- `Solutions[k]` and `Costs[k]` must stay synchronized
- If we update solution but not cost, rankings would be wrong
- Future comparisons would use stale cost (BUG!)

**What would happen without this line?**
```python
# BUG SCENARIO:
Solutions[k] = candidate_solution  # New trajectory (cost 11450)
# Costs[k] = 11500  (OLD COST - not updated!)

# Next iteration:
# Rankings use Costs[k] = 11500 (wrong!)
# Selection probabilities are incorrect
# Worse: If we select this solution again, base_cost = 11500
# But solution actually costs 11450
# Comparison is meaningless!
```

**Exam question**: "Could we avoid storing costs and just recompute on demand?"
**Answer**: "Theoretically yes, but terrible for performance. Computing trajectory cost is expensive (full physics simulation). We do it once per mutation, then cache in `Costs[k]`. Without caching, we'd recompute: (1) For ranking (N² comparisons = N² cost calls!), (2) For comparison in accept/reject, (3) For final reporting. That's 1000s of redundant calculations. The memory cost of storing N floats is trivial compared to computation savings."

---

### LINE 27: `Trials[k] = 0`

#### Syntax Analysis

**What it does**: Reset failure counter for this solution.

**Breakdown**:
- `Trials[k]`: Trial counter for solution `k`
- `=`: Assignment
- `0`: Reset to zero (integer literal)

**Example**:
```python
Trials = [5, 12, 3]  # Solution 1 has failed 12 times
k = 1

Trials[k] = 0

# Result:
Trials = [5, 0, 3]
#            ^  Reset!
```

---

#### Conceptual Justification

**Purpose**: Reward success—solution just improved, so reset abandonment counter.

**What is `Trials[k]`?**
- Counter of consecutive failed improvement attempts
- Increments when mutation is rejected
- Resets when mutation is accepted
- Used in scout phase: If `Trials[k] > LIMIT`, abandon solution

**Why reset on success?**
- Solution just improved → Still promising
- Give it more chances to improve further
- Don't abandon solutions that are making progress

**What's the scout mechanism?**
- Solutions stuck in local optima accumulate high trial counts
- When `Trials[k] > LIMIT` (e.g., 20), scout replaces it with random solution
- Restarting search elsewhere

**Why is this important?**
- Without reset: Even successful solutions eventually get abandoned (trial count keeps growing)
- With reset: Only stagnant solutions get abandoned
- This is the key to balancing exploitation and exploration

**Example scenario**:
```
Iteration 10: Solution 1 at cost 11500, Trials[1] = 8
  - Mutation improves to 11450
  - Accept: Trials[1] = 0  (reset!)

Iteration 11-15: 5 mutations fail
  - Trials[1] increments to 5

Iteration 16: Mutation improves to 11400
  - Accept: Trials[1] = 0  (reset again!)

Without reset:
  - Trials[1] would be 8 + 5 + 1 = 14
  - Close to LIMIT = 20, even though solution is improving

With reset:
  - Trials[1] = 0 after each success
  - Only abandoned if truly stuck
```

**Exam question**: "What if we didn't reset trials on success?"
**Answer**: "All solutions would eventually hit LIMIT and get abandoned, even ones that are improving. The population would be constantly reset to random solutions, losing all learned information. The algorithm would effectively become random search (no learning, no progress). Resetting trials is essential for the algorithm to accumulate improvements over time."

---

### LINE 28: `else:`

#### Syntax Analysis

**What it does**: Alternate branch when mutation didn't improve.

**Breakdown**:
- `else`: Python keyword
- `:`: Starts alternate block
- Executes when `if` condition was `False`

**Control flow**:
```
if candidate_cost < base_cost:
    # Accept mutation (executed if improved)
else:
    # Reject mutation (executed if not improved)
```

---

#### Conceptual Justification

**Purpose**: Handle case where mutation was worse.

**When does this execute?**
- `candidate_cost >= base_cost`
- Mutation didn't improve (equal or worse)
- Keep old solution, penalize with trial increment

---

### LINE 29: `Trials[k] += 1`

#### Syntax Analysis

**What it does**: Increment failure counter.

**Breakdown**:
- `Trials[k]`: Current trial count
- `+=`: In-place addition
- `1`: Increment by one
- Equivalent to: `Trials[k] = Trials[k] + 1`

**Example**:
```python
Trials = [5, 12, 3]
k = 1

Trials[k] += 1

# Result:
Trials = [5, 13, 3]
#            ^^  Incremented!
```

---

#### Conceptual Justification

**Purpose**: Track consecutive failures—if too many, solution will be abandoned.

**What does incrementing do?**
- Records one more failed improvement attempt
- Moves solution closer to abandonment threshold
- Signals solution might be stuck

**Why increment only on rejection?**
- Accept → Solution improved → Reset to 0
- Reject → Solution didn't improve → Increment
- Counts CONSECUTIVE failures (reset breaks the streak)

**What happens when `Trials[k] > LIMIT`?**
- Scout phase (next phase) replaces solution with random trajectory
- Restarts search in unexplored region
- Prevents wasting effort on stuck solutions

**Balance**:
- LIMIT too low (e.g., 5): Frequent abandonment → Not enough local search
- LIMIT too high (e.g., 100): Rare abandonment → Stuck in local optima
- LIMIT = 20: Reasonable balance (used in this code)

**Example scenario**:
```
Initial: Trials[1] = 0

Iteration 1: Mutation rejected → Trials[1] = 1
Iteration 2: Mutation rejected → Trials[1] = 2
Iteration 3: Mutation rejected → Trials[1] = 3
...
Iteration 20: Mutation rejected → Trials[1] = 20
Iteration 21: Mutation rejected → Trials[1] = 21

Scout phase: Trials[1] = 21 > LIMIT = 20
  → Replace Solutions[1] with random trajectory
  → Reset Trials[1] = 0
```

**Exam question**: "Why not abandon immediately after one failure?"
**Answer**: "Random mutations often make things worse before finding improvements. This is exploration—we're searching the neighborhood. One failure doesn't mean the solution is stuck; it just means this particular mutation was bad. LIMIT = 20 gives 20 chances to find an improvement. Only after 20 consecutive failures do we conclude the solution is likely in a local optimum and needs restart."

---

## WORKED EXAMPLE

### Scenario Setup

**Population**: `NP = 3`

**After Employed Phase**:
```python
Solutions = [
    [0, 15, 36, 57, 78, 99, ..., 610],   # Solution 0
    [0, 12, 33, 54, 75, 96, ..., 610],   # Solution 1
    [0, 18, 39, 60, 81, 102, ..., 610]   # Solution 2
]

Costs = [12000.0, 11500.0, 12500.0]
Trials = [2, 0, 5]
```

---

### PHASE 1: RANKING (DETAILED TRACE)

#### Line 1: `a = [0] * NP`
```python
a = [0] * 3
# Result: a = [0, 0, 0]
```

---

#### Lines 2-5: Nested Loop

**i = 0 (Solution 0, Cost = 12000)**:

```python
# j = 0:
if Costs[0] <= Costs[0]:  # 12000 <= 12000 → True
    a[0] += 1  # a = [1, 0, 0]

# j = 1:
if Costs[0] <= Costs[1]:  # 12000 <= 11500 → False
    # (no increment)  # a = [1, 0, 0]

# j = 2:
if Costs[0] <= Costs[2]:  # 12000 <= 12500 → True
    a[0] += 1  # a = [2, 0, 0]
```

**After i=0**: `a = [2, 0, 0]`

---

**i = 1 (Solution 1, Cost = 11500, BEST)**:

```python
# j = 0:
if Costs[1] <= Costs[0]:  # 11500 <= 12000 → True
    a[1] += 1  # a = [2, 1, 0]

# j = 1:
if Costs[1] <= Costs[1]:  # 11500 <= 11500 → True
    a[1] += 1  # a = [2, 2, 0]

# j = 2:
if Costs[1] <= Costs[2]:  # 11500 <= 12500 → True
    a[1] += 1  # a = [2, 3, 0]
```

**After i=1**: `a = [2, 3, 0]`

---

**i = 2 (Solution 2, Cost = 12500, WORST)**:

```python
# j = 0:
if Costs[2] <= Costs[0]:  # 12500 <= 12000 → False
    # (no increment)  # a = [2, 3, 0]

# j = 1:
if Costs[2] <= Costs[1]:  # 12500 <= 11500 → False
    # (no increment)  # a = [2, 3, 0]

# j = 2:
if Costs[2] <= Costs[2]:  # 12500 <= 12500 → True
    a[2] += 1  # a = [2, 3, 1]
```

**After i=2**: `a = [2, 3, 1]`

---

**Final Ranking**:
```python
a = [2, 3, 1]
# Solution 0: Rank 2 (beats 2 solutions: itself and solution 2)
# Solution 1: Rank 3 (beats all 3 solutions) ← BEST
# Solution 2: Rank 1 (beats only itself) ← WORST
```

---

### PHASE 2: PROBABILITIES (DETAILED TRACE)

#### Line 8: `SumA = sum(a)`
```python
SumA = sum([2, 3, 1])
# 2 + 3 + 1 = 6
SumA = 6
```

---

#### Line 9-10: Check for Zero (Defensive)
```python
if SumA == 0:  # 6 == 0 → False
    # (this block skipped)
```

---

#### Line 12: Calculate Probabilities
```python
Prob = [ai / SumA for ai in a]
# Expansion:
# ai = 2: 2/6 = 0.333...
# ai = 3: 3/6 = 0.500
# ai = 1: 1/6 = 0.167...

Prob = [0.333, 0.500, 0.167]
```

**Verification**:
- Sum: 0.333 + 0.500 + 0.167 = 1.000 ✓
- Best solution (1): Highest probability (0.500) ✓
- Worst solution (2): Lowest probability (0.167) ✓

---

### PHASE 3: SELECTION (DETAILED TRACE)

We'll trace **one onlooker iteration** in detail.

---

#### Onlooker 0 (First of 3)

**Line 15**: `for onlooker in range(3):` → `onlooker = 0`

---

**Line 16**: `k = select_index_by_probability(Prob, rng=rng)`

**Inside the function** (conceptual trace):
```python
r = rng.random()  # Say: 0.6 (random between 0 and 1)
cumulative = 0.0

# Index 0:
cumulative += Prob[0]  # 0.0 + 0.333 = 0.333
if r <= cumulative:    # 0.6 <= 0.333 → False
    # Continue

# Index 1:
cumulative += Prob[1]  # 0.333 + 0.500 = 0.833
if r <= cumulative:    # 0.6 <= 0.833 → True
    return 1           # ← Selected!

k = 1  # Solution 1 chosen (the best one, 50% chance)
```

---

**Line 18**: `base_solution = Solutions[k]`
```python
base_solution = Solutions[1]
# [0, 12, 33, 54, 75, 96, ..., 610]
```

---

**Line 19**: `base_cost = Costs[k]`
```python
base_cost = Costs[1]
# 11500.0
```

---

**Line 21**: `candidate_solution = MutateSolution(base_solution, graph, n_rings=29, rng=rng)`

**Inside MutateSolution** (conceptual):
```python
# 1. Choose random ring
ring_mutation = rng.integers(0, 29)  # Say: 5

# 2. Get nodes
position = 5 + 1 = 6
prev_node = base_solution[5]  # Node 75
old_node = base_solution[6]   # Node 96

# 3. Find alternatives
prev_edges = graph.get(75, [])  # Say: [(94, 0), (95, 0), (96, 0), (97, 0)]
feasible_options = [94, 95, 97]  # Exclude old_node = 96

# 4. Select new waypoint
new_node = rng.choice([94, 95, 97])  # Say: 95

# 5. Build new trajectory
new_solution = base_solution[:6] + [95]
# [0, 12, 33, 54, 75, 95]

# 6. Regenerate rest (random walk to goal)
# (details omitted, assume succeeds)
new_solution = [0, 12, 33, 54, 75, 95, 117, ..., 610]

# 7. Validate and return
return new_solution
```

```python
candidate_solution = [0, 12, 33, 54, 75, 95, 117, ..., 610]
#                                       ^^  ^^^  (changed)
```

---

**Line 22**: `candidate_cost, _, _, _ = get_trajectory_cost(candidate_solution, Node_coordinates, t_start=0.0)`

**Inside get_trajectory_cost** (conceptual):
```python
# Loop through edges: (0→12), (12→33), ..., (117→...→610)
# For each edge:
#   - Calculate distance, wind, ground speed, time, fuel
#   - Sum costs

# Say result:
total_cost = 11400.0  # Cheaper! (was 11500)
total_fuel = 58000.0
total_time = 7.2
final_weight = 199743.0

return (11400.0, 58000.0, 7.2, 199743.0)
```

```python
candidate_cost = 11400.0  # (others ignored)
```

---

**Line 24**: `if candidate_cost < base_cost:`
```python
if 11400.0 < 11500.0:  # True! Improvement of €100
```

---

**Line 25**: `Solutions[k] = candidate_solution`
```python
Solutions[1] = [0, 12, 33, 54, 75, 95, 117, ..., 610]

# Updated population:
Solutions = [
    [0, 15, 36, 57, 78, 99, ..., 610],        # Solution 0 (unchanged)
    [0, 12, 33, 54, 75, 95, 117, ..., 610],   # Solution 1 (UPDATED!)
    [0, 18, 39, 60, 81, 102, ..., 610]        # Solution 2 (unchanged)
]
```

---

**Line 26**: `Costs[k] = candidate_cost`
```python
Costs[1] = 11400.0

# Updated costs:
Costs = [12000.0, 11400.0, 12500.0]
#                 ^^^^^^^^  (improved!)
```

---

**Line 27**: `Trials[k] = 0`
```python
Trials[1] = 0

# Updated trials:
Trials = [2, 0, 5]
#            ^  (reset because improved)
```

---

**Summary of Onlooker 0**:
- Selected solution 1 (probabilistically, 50% chance)
- Mutated it (changed ring 5)
- Evaluated mutation: €11,400 (improvement!)
- Accepted: Updated solution, cost, reset trials

---

#### Onlooker 1 & 2

Would continue similarly:
- Each onlooker: Select → Mutate → Evaluate → Accept/Reject
- Could select same solution multiple times (probabilistic)
- Could select different solutions
- Total: 3 mutation attempts distributed probabilistically

---

### AFTER ONLOOKER PHASE

**Possible result** (after all 3 onlookers):
```python
Solutions = [
    [0, 15, 36, 57, 78, 99, ..., 610],        # Solution 0 (unchanged this phase)
    [0, 12, 33, 54, 75, 95, 117, ..., 610],   # Solution 1 (improved by onlooker 0)
    [0, 18, 39, 60, 81, 102, ..., 610]        # Solution 2 (unchanged this phase)
]

Costs = [12000.0, 11400.0, 12500.0]
Trials = [2, 0, 5]
```

**Key observations**:
- Solution 1 improved (was €11,500, now €11,400)
- Solution 1 had highest selection probability → Got most attention
- Solution 2 (worst) might not have been selected at all (low probability)
- This is the power of probabilistic selection: Effort focuses on promising solutions

---

## EXAM QUESTIONS

### Conceptual Understanding

**Q1**: "Explain the purpose of the onlooker phase in one sentence."
**A**: "The onlooker phase probabilistically selects and exploits promising solutions, allocating more computational effort to better solutions while maintaining diversity."

---

**Q2**: "Why do we rank solutions before calculating probabilities?"
**A**: "Ranking converts arbitrary costs into a relative quality measure. This makes selection robust to cost magnitude (€10k vs €11k has same effect as €100k vs €110k) and prevents outliers from dominating selection."

---

**Q3**: "What's the difference between employed and onlooker phases?"
**A**: 
- **Employed**: Each solution gets exactly 1 mutation attempt (democratic)
- **Onlooker**: Solutions selected probabilistically; good solutions get multiple attempts, bad solutions may get zero (meritocratic)
- **Effect**: Onlooker accelerates convergence by focusing on promising regions

---

**Q4**: "What role does the `Trials` counter play?"
**A**: "Trials tracks consecutive failed improvements. When `Trials[k] > LIMIT`, solution k is stuck in a local optimum and will be abandoned (replaced with random solution) in scout phase. Successful improvements reset the counter, giving improving solutions more chances."

---

### Implementation Details

**Q5**: "Walk through the ranking algorithm for `Costs = [100, 80, 120]`."
**A**:
```
i=0 (Cost=100):
  j=0: 100≤100 → a[0]=1
  j=1: 100≤80  → No
  j=2: 100≤120 → a[0]=2

i=1 (Cost=80, best):
  j=0: 80≤100 → a[1]=1
  j=1: 80≤80  → a[1]=2
  j=2: 80≤120 → a[1]=3

i=2 (Cost=120, worst):
  j=0: 120≤100 → No
  j=1: 120≤80  → No
  j=2: 120≤120 → a[2]=1

Result: a = [2, 3, 1]
Probabilities: [2/6, 3/6, 1/6] = [33%, 50%, 17%]
```

---

**Q6**: "Explain `Prob = [ai / SumA for ai in a]` in detail."
**A**: "This is list comprehension that normalizes ranks into probabilities. It iterates through each element `ai` in list `a`, divides by `SumA` (total of all ranks), and creates a new list. Result: probabilities that sum to 1.0, proportional to ranks."

---

**Q7**: "Why do we check `if SumA == 0:` when it's impossible?"
**A**: "Defensive programming. While logically impossible (every solution beats itself → minimum SumA = NP), bugs could cause it. Checking prevents division by zero crash. Fallback to uniform probabilities (equal selection chance) allows algorithm to continue rather than crash."

---

**Q8**: "Trace `select_index_by_probability([0.2, 0.5, 0.3], r=0.6)`."
**A**:
```
r = 0.6
cumulative = 0.0

Index 0: cumulative = 0.0 + 0.2 = 0.2
         0.6 <= 0.2? No

Index 1: cumulative = 0.2 + 0.5 = 0.7
         0.6 <= 0.7? Yes → Return 1
```

---

**Q9**: "Why might `MutateSolution` return `None`?"
**A**: "Three reasons: (1) Previous node has only one outgoing edge (no alternatives to mutate to), (2) Random path generation from mutation point to goal fails (gets stuck), (3) Validation fails (wrong length, missing start/end). In production, should retry or skip iteration."

---

**Q10**: "What does the line `candidate_cost, _, _, _ = get_trajectory_cost(...)` do?"
**A**: "Unpacks 4-tuple returned by function: (cost, fuel, time, weight). We only need cost for accept/reject decision, so assign it to `candidate_cost` and ignore others with `_` (Python convention for unused variables)."

---

### Debugging & What-If

**Q11**: "What happens if we forget to reset `Trials[k] = 0` on success?"
**A**: "All solutions eventually hit LIMIT and get abandoned, even improving ones. Population constantly resets to random, losing learned info. Algorithm becomes random search with no progress accumulation."

---

**Q12**: "What if we forget `Costs[k] = candidate_cost` after accepting mutation?"
**A**: "Costs list becomes inconsistent with Solutions list. Future rankings use stale costs → wrong probabilities → poor selection. Worse: if we select same solution again, comparison uses old cost → meaningless accept/reject decision."

---

**Q13**: "What if we used `if Costs[i] < Costs[j]:` (no equals) in ranking?"
**A**: "Solutions only get points for strict victories, not ties. Crucially, self-comparison `Costs[i] < Costs[i]` is false, so solutions don't even beat themselves! Minimum rank becomes 0 (not 1), causing issues in probability calculation (solutions with rank 0 never selected)."

---

**Q14**: "Suppose `NP=10`, `LIMIT=20`, and solution 5 has `Trials[5]=19`. An onlooker selects it and the mutation fails. What happens?"
**A**: "Line 29: `Trials[5] += 1` → `Trials[5] = 20`. In next scout phase, `if Trials[5] > LIMIT:` → `20 > 20` is False (not greater). Solution survives this iteration. Must fail once more (Trials=21) to be abandoned."

---

### Performance & Tuning

**Q15**: "How many `get_trajectory_cost` calls happen in onlooker phase?"
**A**: "Exactly NP calls (one per onlooker). With NP=10, that's 10 trajectory evaluations. This is the most expensive operation (full physics simulation per call). Total ABC iteration: NP employed + NP onlooker = 2×NP evaluations."

---

**Q16**: "How would you tune the population size NP?"
**A**: 
- **NP too small** (e.g., 3): Not enough diversity, premature convergence, few solutions to select from
- **NP too large** (e.g., 100): Slow (2×NP evaluations per iteration), wastes effort on bad solutions
- **Sweet spot**: 10-30 for most problems (balance diversity and computation)
- **Rule of thumb**: NP ≈ 2 × problem_dimension (here, 29 rings → NP≈20-30 reasonable)

---

**Q17**: "What if we changed onlooker count to 2×NP instead of NP?"
**A**: "More exploitation (good solutions get even more attention). Pros: Faster refinement of best solutions. Cons: Slower per iteration, less diversity, risk of over-exploitation. Trade-off between convergence speed and exploration. Standard ABC uses 1:1 ratio as reasonable balance."

---

### Code Improvements

**Q18**: "How would you handle `MutateSolution` returning `None`?"
**A**:
```python
candidate_solution = MutateSolution(base_solution, graph, n_rings=N_RINGS, rng=rng)

if candidate_solution is None:
    # Mutation failed, skip this onlooker
    Trials[k] += 1  # Still penalize (failed to improve)
    continue  # Skip to next onlooker

# Otherwise, proceed with evaluation...
```

---

**Q19**: "Could we optimize by avoiding mutation evaluation if candidate equals base?"
**A**: "Theoretically yes, but nearly impossible: trajectories are lists of 31 integers, chance of exact duplicate after mutation is astronomically small (graph has ~10²⁰ possible paths). Cost of comparison (O(n)) similar to avoiding one cost check. Not worth complexity."

---

**Q20**: "How would you parallelize the onlooker phase?"
**A**: "Each onlooker iteration is independent (selecting and mutating doesn't affect others until update). Could parallelize across onlookers:
```python
from multiprocessing import Pool

def onlooker_task(onlooker_id):
    k = select_index_by_probability(Prob, rng=rng)
    # ... rest of logic
    return (k, candidate_solution, candidate_cost, improved)

with Pool(processes=4) as pool:
    results = pool.map(onlooker_task, range(NP))

# Then update Solutions, Costs, Trials based on results
```
Challenge: Need to merge updates (multiple onlookers might improve same solution). Performance gain: ~2-4× on multi-core CPU."

---

## FINAL SUMMARY

### The Onlooker Phase in Three Steps

1. **RANK** solutions by counting victories (`a[i]` = how many solutions i beats)
2. **CONVERT** ranks to probabilities (`Prob[i] = a[i] / sum(a)`)
3. **SELECT** solutions probabilistically, mutate, accept if improved

### Key Concepts

- **Probabilistic selection**: Better solutions get more attempts (but all have a chance)
- **Greedy acceptance**: Only accept improvements (exploitation)
- **Trial tracking**: Count failures to identify stuck solutions
- **Synchronization**: Keep Solutions/Costs/Trials consistent

### Critical Lines

- `a[i] += 1`: Builds rank scores
- `Prob = [ai / SumA for ai in a]`: Normalizes to probabilities
- `k = select_index_by_probability(Prob, rng=rng)`: Roulette wheel
- `if candidate_cost < base_cost:`: Greedy selection
- `Solutions[k] = candidate_solution`: Update population
- `Trials[k] = 0` or `+= 1`: Track progress

### Why This Design?

- **Efficiency**: Focuses effort on promising solutions
- **Balance**: Exploitation (onlooker) + Exploration (scout)
- **Robustness**: Rank-based (not cost-based) probabilities
- **Simplicity**: No complex parameters or schedules

You now have **complete mastery** of the onlooker phase! 🐝
