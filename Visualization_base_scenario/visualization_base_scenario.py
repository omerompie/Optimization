"""
This file makes a visualization of the two algorithm outcomes and includes the great circle trajectory.
If you run this file, a file named compare_routes.html should pop up in this directory.
"""


import folium
from graph_build_for_bee.build_graph_function import build_graph


base_solution_bee_scenario_0 = [0, 18, 40, 60, 80, 101, 122, 142, 163, 184, 205, 226, 247, 268, 289, 311, 332, 353, 374, 395, 416, 437, 457, 478, 499, 520, 541, 562, 583, 603, 610]

best_solution_dijkstra = [
0,
21,
41,
61,
81,
101,
121,
142,
163,
184,
206,
227,
248,
269,
290,
311,
332,
353,
374,
395,
416,
437,
457,
477,
498,
519,
540,
561,
582,
604,
610
]

great_circle_trajectory = [0, 11, 32, 53, 74, 95, 116, 137, 158, 179, 200, 221, 242, 263, 284, 305, 326, 347, 368, 389, 410, 431, 452, 473, 494, 515, 536, 557, 578, 610]

"""
please refer to the AI disclosure. 
We made the inputs for the visualization and chat GPT made the visualization 
To make a good and clear visualization with the map, we had to use folium 
and write html
we could not figure out how. 
"""

def add_legend(m):
    legend_html = """
    <div style="
        position: fixed;
        bottom: 30px;
        left: 30px;
        z-index: 9999;
        background-color: rgba(255,255,255,0.9);
        padding: 10px 12px;
        border-radius: 8px;
        font-size: 14px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    ">
      <div style="font-weight: 600; margin-bottom: 6px;">Legend</div>

      <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
        <div style="width:26px; height:4px; background:#ff3b30;"></div>
        <div>ABC's solution</div>
      </div>

      <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
        <div style="width:26px; height:4px; background:#34c759;"></div>
        <div>Dijkstra's solution</div>
      </div>

      <div style="display:flex; align-items:center; gap:8px;">
        <div style="width:26px; height:0; border-top:4px dashed #007aff;"></div>
        <div>Great circle trajectory</div>
      </div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))


def plot_trajectories(best_bee, best_dijkstra, great_circle, node_coords, out_html="compare_routes.html"):
    # ids -> (lat,lon)
    route_bee = [node_coords[nid] for nid in best_bee]
    route_dij = [node_coords[nid] for nid in best_dijkstra]
    route_gc = [node_coords[nid] for nid in great_circle]

    # map
    m = folium.Map(location=route_bee[0], zoom_start=4, tiles="CartoDB dark_matter")

    # grid nodes (grey dots)
    for _, (lat, lon) in node_coords.items():
        folium.CircleMarker(
            location=(lat, lon),
            radius=2,
            color="#bfbfbf",
            fill=True,
            fill_color="#bfbfbf",
            fill_opacity=0.55,
            opacity=0.55,
            weight=0
        ).add_to(m)

    # Great circle line (blue dashed)
    folium.PolyLine(
        locations=route_gc,
        color="#007aff",
        weight=4,
        opacity=0.95,
        dash_array="6,6"
    ).add_to(m)

    # Dijkstra line (green)
    folium.PolyLine(
        locations=route_dij,
        color="#34c759",
        weight=4,
        opacity=0.95
    ).add_to(m)

    # Bee best line (red) - teken als laatste zodat hij "bovenop" ligt
    folium.PolyLine(
        locations=route_bee,
        color="#ff3b30",
        weight=4,
        opacity=0.95
    ).add_to(m)

    # Start/End markers (gebruik start/eind van bee)
    folium.Marker(
        location=route_bee[0],
        popup=f"Start (node {best_bee[0]})",
        icon=folium.Icon(color="green", icon="play")
    ).add_to(m)

    folium.Marker(
        location=route_bee[-1],
        popup=f"End (node {best_bee[-1]})",
        icon=folium.Icon(color="red", icon="flag")
    ).add_to(m)

    # legend
    add_legend(m)

    # fit bounds zodat alles goed in beeld is (combineer alle routes)
    all_points = route_bee + route_dij + route_gc
    m.fit_bounds(all_points)

    m.save(out_html)
    print("Saved map to:", out_html)


def main():
    nodes, node_coords, graph, N_RINGS, N_ANGLES = build_graph()
    plot_trajectories(base_solution_bee_scenario_0, best_solution_dijkstra, great_circle_trajectory, node_coords)


if __name__ == "__main__":
    main()
