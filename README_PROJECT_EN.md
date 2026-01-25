# Project README – Route Optimization (AMS → JFK)

This repository contains a **route-optimization project** for a flight from **Schiphol (AMS)** to **JFK (New York)**.  
High-level flow:

1. **Build a grid/graph** (waypoints + edges).
2. Compute **edge costs** (wind → ground speed → time → fuel burn → € costs + ANSP).
3. Compute **trajectory costs** (sum of edge costs + penalties).
4. Run optimization algorithms:
   - **Dynamic Dijkstra** (state = node + time + weight)
   - **Artificial Bee Colony (ABC)** (candidate routes → evaluate trajectory cost)
5. Compare against a **Great Circle** baseline route.
6. **Visualize** and (optionally) run **validation/statistics**.

> Tip: Many files contain detailed comments. If you want to understand exactly “what does what”, follow the comments in the order suggested below.

---

## Project structure – where to look

### Core components
- `src/`
  - `grid.py` – **grid/waypoint generation** (cigar-shaped grid around the great-circle) + adjacency list.
  - `solver_1.py` – **dynamic Dijkstra** implementation (with Pareto-pruning per time bin).
  - `ansp.py` – simplified **ANSP fees** per edge (region + distance based).
  - `vinc.py` – Vincenty/geodesy utilities (distance + bearing).

- `Trajectory/`
  - `edge_cost_aircraft1.py` – **edge cost model** (wind, GS, time, fuel burn, fuel/time cost + ANSP).
  - `trajectory_cost_ac1.py` – **trajectory cost** (sum of edges + penalties/constraints).

- `graph_build_for_bee/`
  - `build_graph_function.py` – builds nodes/coords/graph for ABC (ABC often uses dummy edge-costs and evaluates full trajectory cost afterwards).

### Optimization algorithms
- `Dijkstra/`
  - `main_dijkstra.py` – run script for **dynamic Dijkstra** (uses the physics adapter via `get_edge_cost`).
- `Bee_Colony/`
  - `base_bee_colony_aircraft1.py` – **single ABC run** + (optional) animation.
  - `run_bee_ac1_for_multiple_scenarios.py` – **batch**: 31 start times (t=0..30), multiple runs per start time, exports CSV.
  - `random_or_mutate_trajectory_and_roulette_wheel.py` – random trajectories, mutation, roulette-wheel selection.

### Great Circle baseline & visualization
- `great_circle/`
  - `great_circle_costs.py` – cost computation for the **fixed great-circle trajectory** for 31 start times.
- `Visualization_base_scenario/`
  - `visualization_base_scenario.py` – generates a **Folium** map (`compare_routes.html`) comparing ABC vs Dijkstra vs Great Circle.

### Data prep (typically one-off / already provided)
- `dataframe_filtering/`
  - `aircraft_df_filtering.py` – filters the aircraft performance DB (altitude=34000, Mach≈0.82) → `Aircraft_1_filtered.csv`.
  - `determining_ff.py` – interpolation/extrapolation of fuel flow as a function of weight.
- `weather/`
  - `wind_for_coordinates.csv` – **wind per waypoint per hour** (0..39h). Used by the cost model.
  - `weather_model.py` – time interpolation + projection onto heading → head/tailwind (km/h).
  - `grib_to_csv.py` – (optional) regenerate `wind_for_coordinates.csv` from GRIB2 (extra dependencies).

### Misc / older work
- `Edge_calculation/` – early/prototype calculations (useful as reference, not the final pipeline).
- `OLD/`, `homework/`, `statistics/`, `omer_files/` – older/loose scripts.

---

## Quickstart (running the project)

### 1) Python environment
A `.venv/` exists in the zip, but it’s usually **machine/OS-specific**. Recommended: create your own venv.

```bash
cd Optimization
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -U pip
pip install numpy pandas matplotlib folium
```

**Only needed if you want to regenerate wind from GRIB:**
```bash
pip install xarray cfgrib
# Note: cfgrib often also requires ecCodes (platform dependent).
```

### 2) Important: run from the project root
Many imports look like `from Trajectory...` or `from Bee_Colony...`.  
So it’s most reliable to run scripts with **`Optimization/` as your working directory**.

---

## Step-by-step pipeline

### A) Build the graph / grid
**Where:** `src/grid.py` and `graph_build_for_bee/build_graph_function.py`

- Grid parameters: `N_RINGS`, `N_ANGLES`, `RING_SPACING_KM`, `MAX_WIDTH_KM`, `BASE_WIDTH_M`.
- Adjacency: each node connects to “straight/left/right” in the next ring + last ring connects to the destination.

**Quick test:**
- `main.py` writes `grid_waypoints_lonlat.txt` (useful for plotting).

```bash
python main.py
```

---

### B) Edge costs (the main “physics/economics” part)
**Where:** `Trajectory/edge_cost_aircraft1.py`

Key function:

```python
fuel_burn_kg, time_h, total_cost_edge = get_edge_cost(
    waypoint_i, waypoint_j, waypoint_i_id,
    current_weight_kg, current_time
)
```

What happens (high level):
- distance + heading (Vincenty)
- head/tailwind from `weather/weather_model.py`
- ground speed → segment time
- fuel flow from `dataframe_filtering/determining_ff.py` (interpolation vs weight)
- fuel burn + costs (fuel + cost-of-time) + ANSP costs

> This file also contains commented “sample calls” at the bottom, which are very useful for debugging.

---

### C) Trajectory costs (sum of edges + constraints)
**Where:** `Trajectory/trajectory_cost_ac1.py`

Key function:
```python
total_cost, total_fuel, total_time, final_weight = get_trajectory_cost(
    trajectory_node_ids,
    node_coordinates,
    t_start=0.0
)
```

**Constraints / penalties:**
- excessive fuel burn → large penalty
- arrival too early / too late (time window) → large penalty

---

### D) Run Dynamic Dijkstra
**Where:** `Dijkstra/main_dijkstra.py` + `src/solver_1.py`

Run:
```bash
python Dijkstra/main_dijkstra.py
```

What you can tweak in `main_dijkstra.py`:
- `ENABLE_TOA_CONSTRAINT` + `MIN_ARRIVAL_HOURS` / `MAX_ARRIVAL_HOURS`
- grid parameters (`N_RINGS`, `N_ANGLES`, …)
- `TIME_BIN_SEC` (pruning resolution)

Outputs (in the working directory):
- `solution_path.txt` (lat/lon per line)
- `solution_path_ids.txt` (node IDs)
- `grid_waypoints_lonlat.txt`

---

### E) Run Artificial Bee Colony (ABC)
**Where:** `Bee_Colony/`

**Single run + animation:**
```bash
python Bee_Colony/base_bee_colony_aircraft1.py
```

**Batch over multiple start times (t=0..30) + CSV export:**
```bash
python Bee_Colony/run_bee_ac1_for_multiple_scenarios.py
```

Main parameters (top of the scripts) to tune:
- `POPULATION_SIZE`, `MAX_ITERATIONS`, `LIMIT`
- `T_START` (scenario start time)

> ABC uses the graph mainly for “feasible moves”; the real objective value comes from `get_trajectory_cost()`.

---

### F) Compute the Great Circle baseline
**Where:** `great_circle/great_circle_costs.py`

Run:
```bash
python great_circle/great_circle_costs.py
```

This uses a hardcoded list of node IDs (the great-circle trajectory) and writes a CSV with cost/fuel/time per `t_start`.

---

### G) Visualize route comparison
**Where:** `Visualization_base_scenario/visualization_base_scenario.py`

Run:
```bash
python Visualization_base_scenario/visualization_base_scenario.py
```

Output:
- `compare_routes.html` (open in a browser)

---

## Where the “most important comments” are
If you want to read the repo in a logical order:

1. `src/grid.py` – how the grid and connectivity are constructed  
2. `weather/weather_model.py` – how wind is interpolated and projected onto heading  
3. `dataframe_filtering/determining_ff.py` – fuel-flow interpolation vs weight  
4. `Trajectory/edge_cost_aircraft1.py` – full edge-cost chain  
5. `Trajectory/trajectory_cost_ac1.py` – trajectory cost + penalties  
6. `src/solver_1.py` – dynamic Dijkstra + pruning  
7. `Bee_Colony/base_bee_colony_aircraft1.py` – ABC phases (employed/onlooker/scout)  

---

## Handy “starting points”
If you only want to run 3 things to see the full story:

1. **Dijkstra**: `python Dijkstra/main_dijkstra.py`  
2. **ABC (single run)**: `python Bee_Colony/base_bee_colony_aircraft1.py`  
3. **Visualization**: `python Visualization_base_scenario/visualization_base_scenario.py`  

Good luck — and definitely follow the comments in the code for the details.
