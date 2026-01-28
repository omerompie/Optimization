# BEE COLONY ALGORITHM - COMPLETE EXAM PREPARATION GUIDE

## Document Purpose
This document provides a line-by-line explanation of the Artificial Bee Colony (ABC) implementation and all supporting modules (random trajectories, edge costs, weather processing, aircraft filtering). Use this to prepare for programming questions about your teammate's work.

---

## TABLE OF CONTENTS
1. [High-Level Overview](#high-level-overview)
2. [Random Trajectory & Mutation](#random-trajectory-mutation)
3. [Edge Cost Calculation](#edge-cost-calculation)
4. [Weather Processing](#weather-processing)
5. [Aircraft Data Filtering](#aircraft-filtering)
6. [Main ABC Algorithm](#abc-algorithm)
7. [Key Concepts & Justifications](#key-concepts)
8. [Exam Questions You Should Be Ready For](#exam-questions)

---

## HIGH-LEVEL OVERVIEW

### What is Artificial Bee Colony (ABC)?
**Nature-inspired optimization algorithm** that mimics honey bee foraging behavior:
- **Employed bees**: Exploit known food sources (improve existing solutions)
- **Onlooker bees**: Choose promising sources probabilistically (exploit good solutions)
- **Scout bees**: Abandon poor sources and search randomly (exploration)

### Why ABC for Route Optimization?
**Advantages**:
1. **Global search capability**: Avoids local minima (unlike gradient methods)
2. **No gradient needed**: Works with complex cost functions (wind, fuel, ANSP)
3. **Population-based**: Maintains diverse solutions simultaneously
4. **Simple implementation**: Few parameters to tune

**Disadvantages**:
1. **No optimality guarantee**: Heuristic, not exact
2. **Slower than Dijkstra**: More function evaluations
3. **Parameter sensitive**: POPULATION_SIZE, LIMIT, etc. affect performance

### Key Difference from Dijkstra
| Aspect | Dijkstra | ABC |
|--------|----------|-----|
| Type | Exact algorithm | Metaheuristic |
| Guarantee | Optimal (if found) | Near-optimal |
| Search | Systematic (state-space) | Stochastic (population) |
| Speed | Fast (with pruning) | Slower (many evaluations) |
| Flexibility | Requires graph structure | Works with any evaluation function |

---

## RANDOM TRAJECTORY & MUTATION

### File: `Bee_Colony/random_or_mutate_trajectory_and_roulette_wheel.py`

### FUNCTION: `RandomTrajectory()`

```python
def RandomTrajectory(start_node, goal_node, graph, n_rings=29, rng=None):
```

**Purpose**: Generate a random feasible trajectory from AMS to JFK.

**Why needed?** 
- Initialize ABC population
- Scout bee phase (replace abandoned solutions)

#### Line-by-Line Breakdown

```python
if rng is None:
    rng = np.random.default_rng()
```
**Justification**: 
- Create random number generator if not provided
- `rng=None` → non-reproducible (for testing)
- `rng=np.random.default_rng(seed)` → reproducible (for experiments)

**Exam tip**: "Why use `rng` parameter instead of `random.randint()`?"
**Answer**: "Allows reproducibility via seeds for scientific experiments. Same seed → same random sequence → reproducible results."

---

```python
trajectory = [start_node]
current = start_node
```
**Justification**: 
- Initialize trajectory with origin (node 0)
- Track current position in graph traversal

---

```python
max_edges = n_rings + 1
edges_taken = 0
```
**Justification**: Safety check for infinite loops.

**Why `n_rings + 1`?**
- Expected path length: origin → 29 rings → destination = 31 nodes = 30 edges
- `+1` for tolerance (should never exceed, but prevents crashes)

---

```python
while current != goal_node:
```
**Justification**: Continue until we reach JFK (node 610).

---

```python
    edges = graph.get(current, [])
    
    if not edges:
        raise ValueError(
            f"Node {current} does not have outgoing edges, cannot reach {goal_node}."
        )
```
**Justification**: 
- Get neighbors from adjacency list
- If no neighbors → graph is broken → raise error

**Why `graph.get(current, [])`?** 
- Safe dictionary access (returns `[]` if key missing)
- Prevents `KeyError` exceptions

---

```python
    neighbors = [neighbor_id for (neighbor_id, _) in edges]
```
**Justification**: Extract neighbor IDs from edge tuples.

**Why `_` (underscore)?**
- Graph stores edges as `(neighbor_id, cost)` tuples
- We don't need cost (dummy value = 0)
- `_` = Python convention for "ignored variable"

**Example**: 
```python
edges = [(22, 0), (23, 0), (24, 0)]
neighbors = [22, 23, 24]
```

---

```python
    next = int(rng.choice(neighbors))
```
**Justification**: Randomly select next waypoint.

**Why `int()`?**
- `rng.choice()` returns `numpy.int64` type
- Causes issues later (e.g., `np.int64(17)` instead of `17`)
- `int()` converts to Python native integer

**Random selection**: Each neighbor has equal probability (uniform distribution).

---

```python
    trajectory.append(next)
    current = next
```
**Justification**: 
- Add selected node to path
- Update current position

---

```python
    edges_taken += 1
    if edges_taken > max_edges:
        raise RuntimeError(
            "Trajectory is longer than expected. Bug in the graph"
        )
```
**Justification**: Detect infinite loops.

**When would this trigger?**
- Graph has cycles (shouldn't happen with our DAG)
- Incorrect connectivity
- Bug in graph construction

**Why raise error?** Better to crash immediately than loop forever.

---

```python
return trajectory
```
**Justification**: Return complete path as list of node IDs.

**Example output**: `[0, 15, 36, 57, ..., 610]`

---

### FUNCTION: `MutateSolution()`

```python
def MutateSolution(solution, graph, n_rings=29, rng=None, max_tries=200):
```

**Purpose**: Create a modified version of an existing trajectory.

**Why needed?** Core of ABC exploration:
- Employed bees: Try to improve current solution
- Onlooker bees: Exploit promising solutions

**Strategy**: Change one waypoint, regenerate rest of path.

#### Line-by-Line Breakdown

```python
expected_len = n_rings + 2
if len(solution) != expected_len:
    raise ValueError(f"Solution length {len(solution)} != expected {expected_len}.")
```
**Justification**: Validate input trajectory.

**Why `n_rings + 2`?**
- 1 origin + 29 rings + 1 destination = 31 nodes
- If length wrong → input is corrupted → raise error

---

```python
start_node = solution[0]
goal_node = solution[-1]
```
**Justification**: 
- Extract origin and destination
- `solution[0]` should always be 0 (Schiphol)
- `solution[-1]` should always be 610 (JFK)

---

```python
ring_mutation = int(rng.integers(0, n_rings))
position = ring_mutation + 1
```
**Justification**: Choose random ring to mutate.

**Why `rng.integers(0, n_rings)`?**
- Returns integer in `[0, 29)` → 29 possible rings
- **Does NOT include `n_rings`** (exclusive upper bound)

**Why `position = ring_mutation + 1`?**
- Ring 0 is at index 1 in trajectory (index 0 is origin)
- Ring 1 is at index 2
- Ring r is at index r+1

**Example**: 
- Trajectory: `[0, 15, 36, 57, ..., 610]`
- Indices:    `[0,  1,  2,  3, ...,  30]`
- `ring_mutation = 2` → `position = 3` → mutate node at index 3

---

```python
prev_node = solution[position - 1]
old_node  = solution[position]
```
**Justification**: 
- `prev_node`: Node we're coming from (needed for connectivity)
- `old_node`: Current node at mutation point (to avoid selecting same one)

---

```python
prev_edges = graph.get(prev_node, [])
if not prev_edges:
    return None
```
**Justification**: 
- Get edges from previous node
- If no edges → impossible to continue → return `None`

**Why return `None`?** Signals mutation failed (caller can retry).

---

```python
feasible_options = [nid for (nid, _) in prev_edges if nid != old_node]
if not feasible_options:
    return None
```
**Justification**: Find alternative waypoints.

**Filter logic**:
- Include all neighbors of `prev_node`
- EXCEPT the current `old_node` (otherwise mutation does nothing)

**Why might this be empty?**
- `prev_node` only connects to `old_node` (no alternatives)
- Rare, but possible near edges of grid

---

```python
new_node = int(rng.choice(feasible_options))
```
**Justification**: Randomly select replacement waypoint.
- `int()` for same reason as before (avoid `numpy.int64`)

---

```python
new_solution = solution[:position] + [new_node]
```
**Justification**: Build new trajectory up to mutation point.

**Slicing**: `solution[:position]` = all nodes before mutation
- `position = 3` → `solution[:3]` = `[0, 15, 36]`
- Then append `new_node`

---

```python
current = new_node
remaining_edges_max = n_rings - ring_mutation
steps = 0
```
**Justification**: Setup for regenerating rest of path.

**Why `n_rings - ring_mutation`?**
- We mutated ring `ring_mutation`
- Remaining rings: `n_rings - ring_mutation`
- Example: Mutated ring 2, remaining = 29 - 2 = 27 rings

---

```python
while current != goal_node:
    edges = graph.get(current, [])
    if not edges:
        break
    
    neighbors = [nid for (nid, _) in edges]
    next = int(rng.choice(neighbors))
    
    new_solution.append(next)
    current = next
    
    steps += 1
    if steps > remaining_edges_max:
        break
```
**Justification**: Regenerate path from mutation point to destination.
- Same logic as `RandomTrajectory()`
- Safety checks for stuck paths

---

```python
if len(new_solution) == expected_len and new_solution[0] == start_node and new_solution[-1] == goal_node:
    return new_solution

return None
```
**Justification**: Validate result before returning.

**Checks**:
1. **Length**: Must be exactly 31 nodes
2. **Start**: Must begin at origin (0)
3. **End**: Must end at destination (610)

**Return `None`** if any check fails → caller knows mutation failed.

---

### FUNCTION: `select_index_by_probability()`

```python
def select_index_by_probability(prob_list, rng=None):
```

**Purpose**: Roulette wheel selection for onlooker phase.

**Concept**: Select index with probability proportional to `prob_list[i]`.

#### How Roulette Wheel Works

```
Probabilities: [0.5, 0.3, 0.2]

Wheel:
|████████████████████████|████████████████|██████████|
|        Index 0          |    Index 1     | Index 2  |
0.0                      0.5              0.8        1.0
```

Spin (random number `r`):
- `r = 0.25` → falls in Index 0
- `r = 0.65` → falls in Index 1
- `r = 0.95` → falls in Index 2

#### Line-by-Line Breakdown

```python
r = rng.random()
cumulative = 0.0

for index in range(len(prob_list)):
    cumulative += prob_list[index]
    if r <= cumulative:
        return index

return len(prob_list) - 1
```
**Justification**: Find which interval `r` falls into.

**Algorithm**:
1. Add probability of index 0 to cumulative → check if `r ≤ cumulative`
2. If yes → return 0
3. If no → add probability of index 1 → check again
4. Repeat until `r ≤ cumulative`

**Fallback**: Return last index for floating-point rounding errors.

---

## EDGE COST CALCULATION

### File: `Trajectory/edge_cost_aircraft1.py`

**Purpose**: Calculate fuel burn, time, and cost for a single edge (waypoint i → waypoint j).

### Global Constants

```python
TEMPERATURE_HEIGHT = 288.15 - ((34000 * 0.3048) * 0.0065)
```
**Justification**: Calculate temperature at cruise altitude.

**Formula**: Standard atmosphere model
- Sea level: 288.15 K (15°C)
- Lapse rate: 0.0065 K/m
- Altitude: 34,000 ft = 10,363 m
- Temperature = 288.15 - (10,363 × 0.0065) ≈ 218.8 K (-54°C)

**Why needed?** Speed of sound depends on temperature → affects Mach to TAS conversion.

---

```python
COST_OF_TIME_INDEX = 35
```
**Justification**: Cost index (CI) in kg fuel/hour.

**What is CI?**
- Airline operating cost expressed as fuel equivalent
- Higher CI → fly faster (trade fuel for time)
- Value 35: Typical for long-haul flights

---

```python
MACH_AIRCRAFT_1 = 0.82
FUEL_COSTS_PER_KG = 0.683125
WEIGHT_START_CRUISE = 257743
FUEL_BURN_MAX = 62600
TIME_MAX = 7.5
TIME_MIN = 7.0
```
**Justification**: Aircraft parameters and constraints.
- Mach 0.82: Most efficient speed (determined by analysis)
- Weight: 257,743 kg at cruise start
- Time window: 7.0-7.5 hours

---

### Main Function: `get_edge_cost()`

```python
def get_edge_cost(
    waypoint_i,
    waypoint_j,
    waypoint_i_id,
    current_weight_kg,
    current_time,
):
```

**Purpose**: Compute all costs for one edge.

**Inputs**:
- `waypoint_i`, `waypoint_j`: Coordinates (lat, lon)
- `waypoint_i_id`: ID for weather lookup
- `current_weight_kg`: Aircraft weight at start of edge
- `current_time`: Time since departure (hours)

**Outputs**: `(fuel_burn_kg, time_h, total_cost_eur)`

#### Execution Flow

```python
distance_km = get_distance(waypoint_i, waypoint_j)
heading_deg = get_heading(waypoint_i, waypoint_j)
head_tail_kmh = get_wind_kmh(waypoint_i_id, current_time, heading_deg)
ground_speed_kmh = get_ground_speed(MACH_AIRCRAFT_1, TEMPERATURE_HEIGHT, head_tail_kmh)
time_h = get_time(distance_km, ground_speed_kmh)
fuel_flow_kg_per_h = get_fuel_flow(current_weight_kg, weight_table, ff_table)
fuel_burn_kg = get_fuel_burn(fuel_flow_kg_per_h, time_h)
fuel_cost = get_fuel_costs(fuel_burn_kg, FUEL_COSTS_PER_KG)
time_cost = get_cost_of_time(time_h, COST_OF_TIME_INDEX, FUEL_COSTS_PER_KG)
ansp_cost = get_ansp_cost_for_edge(waypoint_i, waypoint_j)
total_cost_edge = fuel_cost + time_cost + ansp_cost
return fuel_burn_kg, time_h, total_cost_edge
```

**Key Steps**:
1. Calculate distance (Vincenty)
2. Calculate heading
3. Get wind component (weather model)
4. Calculate ground speed (TAS + wind)
5. Calculate time (distance / speed)
6. Look up fuel flow (interpolation)
7. Calculate fuel burn (flow × time)
8. Calculate costs (fuel + time + ANSP)

---

## WEATHER PROCESSING

### File: `weather/grib_to_csv.py`

**Purpose**: Convert GRIB2 weather files to CSV format.

### Key Concepts

**GRIB2**: Standard weather data format
- Source: NOAA GFS
- Resolution: 0.25° lat/lon
- Time: Hourly forecasts (0-39 hours)
- Content: u/v wind components at FL340

### Processing Steps

```python
# 1. Get waypoint coordinates
nodes, node_coords, graph, N_RINGS, N_ANGLES = build_graph()
lat_list = [lat for (lat, lon) in points]
lon_list = [lon for (lat, lon) in points]
```

**Justification**: Extract coordinates for interpolation.

---

```python
# 2. Create xarray DataArrays
lats = xr.DataArray(lat_list, dims="point")
lons = xr.DataArray(lon_list, dims="point")
```

**Justification**: Prepare for bilinear interpolation.

---

```python
# 3. Open GRIB file
ds = xr.open_dataset(grib_path, engine='cfgrib', backend_kwargs={'indexpath': ''})
ds = ds.sortby('latitude').sortby('longitude')
```

**Justification**: 
- Load weather data
- Sort for interpolation (requires monotonic coordinates)

---

```python
# 4. Interpolate to waypoints
u_wp = u.interp(latitude=lats, longitude=lons, method='linear')
v_wp = v.interp(latitude=lats, longitude=lons, method='linear')
```

**Justification**: Bilinear interpolation from grid to waypoints.

**Why interpolate?**
- GRIB grid: 0.25° spacing (≈28 km)
- Waypoints: Arbitrary locations
- Interpolation gives smooth wind field

---

```python
# 5. Create DataFrame
df = pd.DataFrame({
    'waypoint_id': point_ids,
    'latitude': lat_list,
    'longitude': lon_list,
    'u_speed_ms': u_wp,
    'v_speed_ms': v_wp,
    'time': valid_time
})
```

**Justification**: Structure data for easy lookup.

---

```python
# 6. Process all GRIB files
files = ["gfs.t18z.pgrb2.0p25.f000", ..., "gfs.t18z.pgrb2.0p25.f039"]
dataframes = {}
for name in files:
    df_name = get_wind_from_grib(location / name)
    dataframes[name] = df_name

whole_dataframe = pd.concat(list(dataframes.values()), ignore_index=True)
```

**Justification**: 
- Process 40 hourly files
- Merge into single DataFrame
- 40 files × 611 waypoints = 24,440 rows

---

```python
# 7. Convert time to hours
t0 = whole_dataframe['time'].min()
whole_dataframe['time_hours'] = (whole_dataframe['time'] - t0) / pd.Timedelta(hours=1)
```

**Justification**: Convert timestamps to hours since departure.

**Why?** Edge cost function expects `current_time` in hours (0.0, 1.5, etc.)

---

### File: `weather/weather_model.py`

**Purpose**: Interpolate wind in time and project onto heading.

### Function: `get_wind_kmh()`

```python
def get_wind_kmh(waypoint_id, time, heading):
    t = float(time)
    if t > t_max:
        t = t_max
```

**Justification**: Clamp time to data range (0-39 hours).

---

```python
    if t in u_table.index:
        u = float(u_table.at[t, waypoint_id])
        v = float(v_table.at[t, waypoint_id])
    else:
        # Linear interpolation
        h0 = math.floor(t)
        h1 = h0 + 1.0
        u0 = float(u_table.at[float(h0), waypoint_id])
        v0 = float(v_table.at[float(h0), waypoint_id])
        u1 = float(u_table.at[float(h1), waypoint_id])
        v1 = float(v_table.at[float(h1), waypoint_id])
        u = u0 + (t-h0) * ((u1-u0)/(h1-h0))
        v = v0 + (t-h0) * ((v1-v0)/(h1-h0))
```

**Justification**: Interpolate wind between hourly data points.

**Formula**: `value = v0 + (t - t0) × (v1 - v0) / (t1 - t0)`

---

```python
    speed_ms = math.sqrt(u ** 2 + v ** 2)
    wind_to_deg = (90 - math.degrees(math.atan2(v, u))) % 360
```

**Justification**: Convert (u,v) to speed and direction.

**Direction conversion**:
- Mathematical: 0° = East, 90° = North
- Compass: 0° = North, 90° = East
- Formula: `90° - math_angle`

---

```python
    diff = (wind_to_deg - heading + 180) % 360 - 180
    head_tail_kmh = speed_ms * 3.6 * math.cos(math.radians(diff))
```

**Justification**: Project wind onto flight path.

**Vector projection**: `component = magnitude × cos(angle)`
- `diff = 0°` → tailwind (full effect)
- `diff = 90°` → crosswind (no effect)
- `diff = 180°` → headwind (full negative)

---

## AIRCRAFT FILTERING

### File: `dataframe_filtering/aircraft_df_filtering.py`

**Purpose**: Filter aircraft database to relevant conditions.

### Key Steps

```python
# 1. Load data
df = pd.read_csv('Aircraft_1.txt', sep=r'\s+', engine='python')
```

**Justification**: Read space-separated text file.

---

```python
# 2. Filter by altitude
df_340 = df[df["altitude"] == 34000]
```

**Justification**: Keep only FL340 data (cruise altitude).

---

```python
# 3. Find economic Mach
grouped = df_340.groupby("Mach")
avg_fuel_flow = grouped["fuel_flow"].mean()

economics = avg_fuel_flow.copy()
for M in avg_fuel_flow.index:
    TAS = tas_kmh(M)
    FF = avg_fuel_flow[M]
    economics[M] = TAS / FF  # km per kg fuel
```

**Justification**: Calculate efficiency metric (km/kg).
- Higher = more efficient
- Mach 0.82 typically wins

---

```python
# 4. Export filtered data
df_aircraft = df[(df["altitude"] == 34000) & (df["Mach"] == 0.82)]
df_aircraft.to_csv("Aircraft_1_filtered.csv", index=False)
```

**Justification**: Save only relevant rows for fuel flow interpolation.

---

### File: `dataframe_filtering/determining_ff.py`

**Purpose**: Interpolate fuel flow as function of weight.

### Function: `get_fuel_flow()`

```python
def get_fuel_flow(weight, weight_table, ff_table):
    # 1. Sort data
    pairs = sorted(zip(weight_table, ff_table))
    weight_table = [p[0] for p in pairs]
    ff_table = [p[1] for p in pairs]
```

**Justification**: Ensure monotonic x-values for interpolation.

---

```python
    # 2. Check exact match
    if weight in weight_table:
        return ff_table[weight_table.index(weight)]
```

**Justification**: No interpolation needed if exact match.

---

```python
    # 3. Handle extrapolation
    Wmin = weight_table[0]
    Wmax = weight_table[-1]
    
    if weight < Wmin:
        Wa, Wb = weight_table[0], weight_table[1]
        FFa, FFb = ff_table[0], ff_table[1]
    elif weight > Wmax:
        Wa, Wb = weight_table[-2], weight_table[-1]
        FFa, FFb = ff_table[-2], ff_table[-1]
```

**Justification**: Extrapolate if outside data range.
- Use first/last two points to define linear trend

---

```python
    # 4. Find bracketing interval
    else:
        for i in range(len(weight_table) - 1):
            Wa = weight_table[i]
            Wb = weight_table[i + 1]
            if Wa <= weight <= Wb:
                FFa = ff_table[i]
                FFb = ff_table[i + 1]
                break
```

**Justification**: Find interval containing weight.

---

```python
    # 5. Linear interpolation
    FF = ((weight - Wb) / (Wa - Wb)) * FFa + ((weight - Wa) / (Wb - Wa)) * FFb
    return FF
```

**Justification**: Standard linear interpolation formula.

**Simplified**: `FF = FFa + (weight - Wa) / (Wb - Wa) × (FFb - FFa)`

---

## ABC ALGORITHM

### File: `Bee_Colony/base_bee_colony_aircraft1.py`

**Purpose**: Main ABC optimization loop.

### Global Parameters

```python
POPULATION_SIZE = 10
MAX_ITERATIONS = 50
LIMIT = 20
```

**Justification**: ABC hyperparameters.
- **POPULATION_SIZE**: Number of solutions (10 = reasonable diversity)
- **MAX_ITERATIONS**: Number of cycles (50 = sufficient convergence)
- **LIMIT**: Abandonment threshold (20 = balanced exploration/exploitation)

---

### Initialization

```python
Solutions = [None] * NP
Costs = [None] * NP
Trials = [0] * NP
Prob = [0.0] * NP

for i in range(NP):
    Solutions[i] = RandomTrajectory(start_node, goal_node, graph, n_rings=N_RINGS, rng=rng)
    cost_euro, fuel_burn, time_s, weight = get_trajectory_cost(Solutions[i], Node_coordinates, t_start=T_START)
    Costs[i] = cost_euro

min_cost = min(Costs)
b = Costs.index(min_cost)
BestSolution = Solutions[b].copy()
BestCost = Costs[b]
```

**Justification**: 
- Create empty lists
- Generate random initial population
- Track global best

**`.copy()`**: Critical! Prevents reference issues.

---

### Main Loop Structure

```python
while iteration < NumIter:
    # EMPLOYED PHASE
    # ONLOOKER PHASE
    # SCOUT PHASE
    iteration += 1
```

---

### Employed Bee Phase

```python
for i in range(NP):
    current_solution = Solutions[i]
    current_costs = Costs[i]
    
    candidate_solution = MutateSolution(current_solution, graph, n_rings=N_RINGS, rng=rng)
    candidate_costs, _, _, _ = get_trajectory_cost(candidate_solution, Node_coordinates, t_start=T_START)
    
    if candidate_costs < current_costs:
        Solutions[i] = candidate_solution
        Costs[i] = candidate_costs
        Trials[i] = 0
    else:
        Trials[i] += 1
```

**Justification**: Local search with greedy acceptance.

**Process**:
1. Each bee works on assigned solution
2. Generate neighbor via mutation
3. Accept if better (greedy)
4. Reset trials if success, increment if failure

---

### Onlooker Bee Phase

```python
# 1. Rank solutions
a = [0] * NP
for i in range(NP):
    for j in range(NP):
        if Costs[i] <= Costs[j]:
            a[i] += 1

# 2. Convert to probabilities
SumA = sum(a)
if SumA == 0:
    Prob = [1.0 / NP] * NP
else:
    Prob = [ai / SumA for ai in a]

# 3. Select and mutate
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

**Justification**: Probabilistic selection favoring good solutions.

**Ranking**: Count how many solutions each beats
**Selection**: Roulette wheel (better solutions → higher probability)
**Effect**: Good solutions get more "attention"

---

### Scout Bee Phase

```python
best_index = Costs.index(min(Costs))
for i in range(NP):
    if i == best_index:
        continue  # Protect best solution
    
    if Trials[i] > LIMIT:
        Solutions[i] = RandomTrajectory(start_node, goal_node, graph, n_rings=N_RINGS, rng=rng)
        new_costs, _, _, _ = get_trajectory_cost(Solutions[i], Node_coordinates, t_start=T_START)
        Costs[i] = new_costs
        Trials[i] = 0
```

**Justification**: Replace stagnant solutions.

**Condition**: `Trials[i] > LIMIT` (not improved for LIMIT iterations)
**Action**: Replace with random trajectory
**Exception**: Protect best solution (never abandon global best)

---

## KEY CONCEPTS

### 1. Metaheuristic vs. Exact Algorithms

| Feature | ABC (Metaheuristic) | Dijkstra (Exact) |
|---------|---------------------|------------------|
| Optimality | Near-optimal | Optimal |
| Speed | Slower | Faster (with pruning) |
| Flexibility | Any cost function | Requires graph decomposition |
| Tuning | Many parameters | Few parameters |

---

### 2. Exploration vs. Exploitation

**Employed**: Exploitation (local refinement)
**Onlooker**: Moderate exploitation (focus on promising areas)
**Scout**: Exploration (global jumps)

**Balance controlled by LIMIT**: Lower = more exploration, Higher = more exploitation

---

### 3. Trajectory Encoding

**Direct encoding**: List of node IDs
- Simple, intuitive
- Easy mutation
- Guarantees feasibility

---

### 4. Weather Integration

**Bilinear interpolation** (space) + **Linear interpolation** (time) + **Vector projection** (onto heading)

**Result**: Smooth, continuous wind field

---

### 5. Fuel Flow Modeling

**Linear interpolation** between weight data points
**Result**: Accurate fuel prediction as weight changes

---

## EXAM QUESTIONS

### Conceptual

**Q1**: "Why use ABC instead of Dijkstra?"
**A**: "ABC is more flexible for complex objectives that don't decompose into edge costs. However, for our problem, Dijkstra is actually better because costs do decompose nicely. ABC serves as a validation method and handles what-if scenarios easily."

**Q2**: "Explain ABC's three phases."
**A**: "Employed bees exploit current solutions via mutation. Onlooker bees focus on promising solutions probabilistically. Scout bees explore globally by replacing abandoned solutions. This balances local refinement with global search."

---

### Implementation

**Q3**: "Walk through RandomTrajectory()."
**A**: "Start at node 0. Get neighbors from graph. Randomly select one. Add to trajectory. Repeat until reaching node 610. Safety checks prevent infinite loops. Result: feasible random path from AMS to JFK."

**Q4**: "Explain mutation strategy."
**A**: "Select random ring position. Replace that waypoint with random alternative from previous node's neighbors. Regenerate rest of path randomly. This preserves good parts before mutation while exploring new options after."

---

### Calculations

**Q5**: "Trace edge cost calculation."
**A**: "Distance via Vincenty → Heading → Wind lookup → Ground speed (TAS + wind) → Time (distance/speed) → Fuel flow interpolation → Fuel burn (flow × time) → Costs (fuel + time + ANSP) → Total."

**Q6**: "Explain weather interpolation."
**A**: "Spatial: Bilinear between 4 grid points. Temporal: Linear between hour brackets. Direction: Project onto heading via dot product. Result: head/tail wind component in km/h."

---

## SUMMARY

### Components
1. **Random/Mutation**: Generate and modify trajectories
2. **Edge Costs**: Physics model (wind, fuel, time, ANSP)
3. **Weather**: GRIB → CSV → interpolation
4. **Aircraft**: Database filtering + interpolation
5. **ABC**: Population-based optimization

### Innovation
- Direct trajectory encoding (node IDs)
- Single-ring mutation
- Rank-based selection
- Decomposed cost model
- Spatiotemporal weather interpolation

You're fully prepared! 🐝✈️
