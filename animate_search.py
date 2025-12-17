import matplotlib

matplotlib.use('TkAgg')  # Forces a separate interactive window
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# --- CONFIGURATION ---
ANIMATION_DURATION_SEC = 5.0  # Time spent searching (Green dots)
PAUSE_AT_END_SEC = 5.0  # Time to hold the final result (Red line)
FPS = 60  # Frames per second


def animate_optimization():
    # 1. LOAD DATA
    node_coords = {}
    x_coords, y_coords = [], []
    try:
        with open("grid_waypoints_lonlat.txt", "r") as f:
            for idx, line in enumerate(f):
                lat, lon = map(float, line.strip().split(','))
                node_coords[idx] = (lon, lat)
                x_coords.append(lon)
                y_coords.append(lat)
    except FileNotFoundError:
        print("Error: grid_waypoints_lonlat.txt not found.")
        return

    history = []
    try:
        with open("search_history.txt", "r") as f:
            for line in f:
                history.append(int(line.strip()))
    except FileNotFoundError:
        print("Error: search_history.txt not found. Run the solver first!")
        return

    final_path = []
    try:
        with open("solution_path.txt", "r") as f:
            for line in f:
                lat, lon = map(float, line.strip().split(','))
                final_path.append((lon, lat))
    except FileNotFoundError:
        print("Error: solution_path.txt not found.")
        return

    # 2. CALCULATE TIMING
    total_steps = len(history)
    search_frames = int(ANIMATION_DURATION_SEC * FPS)
    pause_frames = int(PAUSE_AT_END_SEC * FPS)
    total_frames = search_frames + pause_frames

    # Speed Factor: How many steps to process per frame
    speed_factor = int(total_steps / search_frames)
    if speed_factor < 1: speed_factor = 1

    print(f"Plan: Search for {ANIMATION_DURATION_SEC}s, then Hold for {PAUSE_AT_END_SEC}s.")

    # 3. SETUP PLOT
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_facecolor('#1a1a1a')
    fig.patch.set_facecolor('#1a1a1a')

    # Static Grid
    ax.scatter(x_coords, y_coords, c='#333333', s=10, alpha=0.5)
    ax.set_title("Dijkstra Optimization Replay", color='white', fontsize=14)

    # Dynamic Elements
    scat = ax.scatter([], [], c='cyan', s=30, marker='o', label='Active Front')
    scat_history = ax.scatter([], [], c='green', s=10, alpha=0.3, label='Visited')

    # Text Counters
    status_text = ax.text(0.02, 0.95, '', transform=ax.transAxes, color='white', fontsize=10)

    # The Big "Victory" Text (Hidden initially)
    victory_text = ax.text(0.5, 0.5, 'OPTIMIZATION COMPLETE',
                           transform=ax.transAxes, color='#00ff00', fontsize=20,
                           ha='center', va='center', weight='bold', alpha=0.0)

    # The Winning Path Line (Hidden initially)
    path_line, = ax.plot([], [], c='red', linewidth=3, alpha=0.8)

    # 4. ANIMATION LOOP
    def update(frame):
        # A. SEARCH PHASE
        if frame < search_frames:
            # Calculate how much history to show
            end_idx = min((frame + 1) * speed_factor, total_steps)
            current_batch = history[:end_idx]

            # Update Green Cloud (Visited)
            if current_batch:
                visited_x = [node_coords[nid][0] for nid in current_batch]
                visited_y = [node_coords[nid][1] for nid in current_batch]
                scat_history.set_offsets(np.c_[visited_x, visited_y])

            # Update Cyan Dot (Active Front)
            if end_idx > 0:
                start_front = max(0, end_idx - speed_factor)
                front_batch = history[start_front:end_idx]
                if front_batch:
                    front_x = [node_coords[nid][0] for nid in front_batch]
                    front_y = [node_coords[nid][1] for nid in front_batch]
                    scat.set_offsets(np.c_[front_x, front_y])

            status_text.set_text(f"Searching... Checked: {end_idx} / {total_steps}")

        # B. VICTORY PHASE (Hold the result)
        else:
            # Ensure full history is shown
            visited_x = [node_coords[nid][0] for nid in history]
            visited_y = [node_coords[nid][1] for nid in history]
            scat_history.set_offsets(np.c_[visited_x, visited_y])

            # Hide the "Active Front" dot
            scat.set_offsets(np.empty((0, 2)))

            # Draw Red Path
            path_x, path_y = zip(*final_path)
            path_line.set_data(path_x, path_y)

            # Show Victory Text
            victory_text.set_alpha(1.0)
            status_text.set_text(f"FINISHED. Optimal Cost Found.")

        return scat, scat_history, status_text, path_line, victory_text

    # 5. RUN
    ani = animation.FuncAnimation(
        fig, update,
        frames=total_frames,
        interval=1000 / FPS,
        blit=True,
        repeat=False
    )

    plt.show()


if __name__ == "__main__":
    animate_optimization()