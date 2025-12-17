import folium


def visualize_results():
    # 1. READ THE GRID NODES
    grid_coords = []
    try:
        with open("grid_waypoints_lonlat.txt", "r") as f:
            for line in f:
                lat, lon = map(float, line.strip().split(','))
                grid_coords.append((lat, lon))
    except FileNotFoundError:
        print("Error: grid_waypoints_lonlat.txt not found. Run main.py first!")
        return

    # 2. READ THE SOLUTION PATH
    path_coords = []
    try:
        with open("solution_path.txt", "r") as f:
            for line in f:
                lat, lon = map(float, line.strip().split(','))
                path_coords.append((lat, lon))
    except FileNotFoundError:
        print("Error: solution_path.txt not found. Run main.py first!")
        return

    # 3. CREATE MAP (Centered on Atlantic)
    # Using a dark theme to make points pop
    m = folium.Map(location=[50, -30], zoom_start=4, tiles='CartoDB dark_matter')

    # 4. PLOT GRID (Grey Dots)
    # We plot them as tiny circles
    for lat, lon in grid_coords:
        folium.CircleMarker(
            location=[lat, lon],
            radius=1,
            color='#888888',
            fill=True,
            fill_opacity=0.4
        ).add_to(m)

    # 5. PLOT START & END
    folium.Marker(grid_coords[0], popup="AMS", icon=folium.Icon(color='green')).add_to(m)
    folium.Marker(grid_coords[-1], popup="JFK", icon=folium.Icon(color='red')).add_to(m)

    # 6. PLOT OPTIMAL PATH (Red Line)
    folium.PolyLine(
        path_coords,
        color="red",
        weight=3,
        opacity=0.9,
        tooltip="Optimal Path"
    ).add_to(m)

    # 7. VISUALIZE THE "FAN OUT" (Optional Debug)
    # Show exactly where Node 0 connects to (Nodes 1-21)
    ams_lat, ams_lon = grid_coords[0]
    # Assuming first 21 nodes after AMS are the first ring
    for i in range(1, 22):
        if i < len(grid_coords):
            lat, lon = grid_coords[i]
            folium.PolyLine(
                [(ams_lat, ams_lon), (lat, lon)],
                color="blue",
                weight=1,
                opacity=0.3
            ).add_to(m)

    # 8. SAVE
    output_file = "optimization_map.html"
    m.save(output_file)
    print(f"Map created! Open '{output_file}' in your browser.")


if __name__ == "__main__":
    visualize_results()