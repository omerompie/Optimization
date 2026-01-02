import graphviz
import os

# Create the Directed Graph
dot = graphviz.Digraph(comment='Dynamic Dijkstra Flowchart', format='png')
dot.attr(rankdir='TB', size='8,12')

# --- Global Node Style ---
dot.attr(
    'node',
    shape='box',
    style='filled',
    fillcolor='#E3F2FD',
    fontname='Arial'
)

# --- 1. Start / Initialization ---
dot.node(
    'Start',
    'START\nInitialize Priority Queue\n(cost=0, start_node, start_time, initial_weight)',
    shape='oval',
    fillcolor='#C8E6C9'
)

# --- 2. Main Loop ---
dot.node(
    'QueueCheck',
    'Is Priority Queue Empty?',
    shape='diamond',
    fillcolor='#FFE0B2'
)

dot.node(
    'NoPath',
    'No Path Found\n(Return Failure)',
    shape='oval',
    fillcolor='#FFCDD2'
)

dot.node(
    'Pop',
    'Pop Lowest-Cost State\n(cost, u, time, weight)'
)

# --- 3. Goal Check ---
dot.node(
    'GoalCheck',
    'Is u == Destination?',
    shape='diamond',
    fillcolor='#FFE0B2'
)

dot.node(
    'End',
    'Reconstruct Path & Return\n(Final cost already includes\nToA penalty if enabled)',
    shape='oval',
    fillcolor='#A5D6A7'
)

# --- 4. Pareto Pruning ---
dot.node(
    'TimeBin',
    'Discretize Time\nCompute time_bin = floor(time / Δt)'
)

dot.node(
    'Pruning',
    'Is State Dominated?\n(Compare cost & remaining fuel\nat same node and time_bin)',
    shape='diamond',
    fillcolor='#FFCDD2'
)

dot.node(
    'DiscardDominated',
    'Discard State\n(Dominated)',
    shape='oval',
    fillcolor='#EF9A9A'
)

dot.node(
    'UpdatePareto',
    'Update Pareto Frontier\nRemove states dominated\nby current state'
)

# --- 5. Neighbor Expansion ---
dot.node(
    'Expand',
    'For Each Neighbor v\nin Adjacency List'
)

dot.node(
    'Physics',
    'Physics Engine\n• Compute wind at time\n• Calculate fuel burn\n• Calculate segment time\n• Calculate segment cost'
)

dot.node(
    'CalcNewState',
    'Compute New State\nnew_cost = cost + segment_cost\nnew_weight = weight − fuel_burn\nnew_time = time + segment_time'
)

dot.node(
    'Feasible',
    'Is new_weight ≥ 0?',
    shape='diamond',
    fillcolor='#FFCDD2'
)

dot.node(
    'SkipNeighbor',
    'Skip Neighbor\n(Infeasible)',
    shape='oval',
    fillcolor='#EF9A9A'
)

dot.node(
    'ApplyPenalty',
    'If v == Destination AND\nTarget Time Exists:\nApply ToA Penalty to cost'
)

dot.node(
    'Push',
    'Push New State to Queue\n(new_cost, v, new_time, new_weight)\nUpdate came_from'
)

dot.node(
    'NextNeighbor',
    'More Neighbors?',
    shape='diamond',
    fillcolor='#FFE0B2'
)

# --- Edges ---

dot.edge('Start', 'QueueCheck')

# Queue handling
dot.edge('QueueCheck', 'Pop', label='No')
dot.edge('QueueCheck', 'NoPath', label='Yes')

# Pop and goal check
dot.edge('Pop', 'GoalCheck')
dot.edge('GoalCheck', 'End', label='Yes')
dot.edge('GoalCheck', 'TimeBin', label='No')

# Pareto pruning
dot.edge('TimeBin', 'Pruning')
dot.edge('Pruning', 'DiscardDominated', label='Yes')
dot.edge('DiscardDominated', 'QueueCheck', style='dashed', label='Loop Back')
dot.edge('Pruning', 'UpdatePareto', label='No')
dot.edge('UpdatePareto', 'Expand')

# Neighbor expansion
dot.edge('Expand', 'Physics')
dot.edge('Physics', 'CalcNewState')
dot.edge('CalcNewState', 'Feasible')

dot.edge('Feasible', 'SkipNeighbor', label='No')
dot.edge('Feasible', 'ApplyPenalty', label='Yes')

dot.edge('ApplyPenalty', 'Push')
dot.edge('Push', 'NextNeighbor')

# Neighbor loop
dot.edge('SkipNeighbor', 'NextNeighbor', style='dashed')
dot.edge('NextNeighbor', 'Expand', label='Yes', style='dashed')
dot.edge('NextNeighbor', 'QueueCheck', label='No', style='dashed')

# --- Render ---
output_path = 'dynamic_dijkstra_flowchart'
dot.render(output_path, view=True)

print(f"Flowchart saved to: {os.path.abspath(output_path + '.png')}")
