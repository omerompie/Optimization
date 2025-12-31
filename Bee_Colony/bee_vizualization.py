import folium
from main_tryout import build_graph

# -------- jouw hardcoded best trajectory --------
best_solution = [0, 6, 27, 48, 68, 90, 111, 132, 153, 173, 194, 215, 236, 257, 278, 299, 320, 342, 364, 386, 408, 430, 452, 473, 495, 516, 537, 558, 579, 599, 610]


def plot_trajectory(best_solution, node_coords, out_html="best_trajectory.html"):
    # Zet node ids om naar (lat, lon)
    route = [node_coords[nid] for nid in best_solution]

    # Kaart (dark theme zoals je foto)
    m = folium.Map(location=route[0], zoom_start=4, tiles="CartoDB dark_matter")

    # 1) Alle grid nodes als grijze puntjes (zoals je foto)
    for _, (lat, lon) in node_coords.items():
        folium.CircleMarker(
            location=(lat, lon),
            radius=2,          # maak 1-2 als je het subtieler wilt
            color="#bfbfbf",
            fill=True,
            fill_color="#bfbfbf",
            fill_opacity=0.6,
            opacity=0.6,
            weight=0
        ).add_to(m)

    # 2) Route lijn (rood/oranje)
    folium.PolyLine(
        locations=route,
        color="#ff3b30",   # rood (zoals foto). alternatief: "#ff9500" voor oranje
        weight=4,
        opacity=0.95
    ).add_to(m)

    # 3) Start / End markers
    folium.Marker(
        location=route[0],
        popup=f"Start (node {best_solution[0]})",
        icon=folium.Icon(color="green", icon="play")
    ).add_to(m)

    folium.Marker(
        location=route[-1],
        popup=f"End (node {best_solution[-1]})",
        icon=folium.Icon(color="red", icon="flag")
    ).add_to(m)

    # 4) Zoom zodat alles in beeld past
    m.fit_bounds(route)

    # Opslaan
    m.save(out_html)
    print("Saved map to:", out_html)


def main():
    # Alleen grid bouwen (geen ABC run)
    nodes, node_coords, graph, N_RINGS, N_ANGLES = build_graph()

    plot_trajectory(best_solution, node_coords, out_html="best_trajectory.html")


if __name__ == "__main__":
    main()
