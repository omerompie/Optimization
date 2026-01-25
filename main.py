import sys
import os
from pathlib import Path

# --- 1. SETUP PROJECT PATHS ---
# This ensures that whether we run Dijkstra or ABC, they can find the 'src'
# and 'Trajectory' folders relative to this root file.
root_dir = Path(__file__).resolve().parent
sys.path.append(str(root_dir))


def run_dijkstra():
    print("Dijkstra")
    from Dijkstra.main_dijkstra import main as dijkstra_main
    dijkstra_main()


def run_bee_colony():
    print("ABC")
    import Bee_Colony.base_bee_colony_aircraft1


if __name__ == "__main__":
    print("Starting optimizations")

    # 1. Run Dijkstra
    run_dijkstra()

    # 2. Run ABC
    run_bee_colony()

    print("\nDone.")