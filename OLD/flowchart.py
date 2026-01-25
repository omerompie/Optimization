import graphviz
import os

# Create the Directed Graph
dot = graphviz.Digraph(comment='Dynamic Dijkstra Flowchart', format='png')
dot.attr(rankdir='TB', size='10,16')  # Top-Bottom direction, slightly larger

# --- Define Nodes ---
# Styles
dot.attr('node', shape='box', style='filled', fillcolor='#E3F2FD', fontname='Arial')

# 1. Initialization
dot.node('Start', 'Start\n(Init Queue: StartNode, Time, Weight)', shape='oval', fillcolor='#C8E6C9')

# 2. Main Loop
dot.node('QueueCheck', 'Is Queue Empty?', shape='diamond', fillcolor='#FFE0B2')
dot.node('NoPath', 'No Path Found\n(Return Failure)', shape='oval', fillcolor='#FFCDD2')
dot.node('Pop', 'Pop Lowest Cost State\n(cost, u, time, weight)')

# 3. Goal Logic (Updated to match code)
dot.node('GoalCheck', 'Is Node (u) == Destination?', shape='diamond', fillcolor='#FFE0B2')
dot.node('MinTimeCheck', 'Is Time < Min Arrival?\n(Too Early?)', shape='diamond', fillcolor='#FFCDD2')
dot.node('DiscardEarly', 'Discard Path\n(Too Early)', shape='oval', fillcolor='#EF9A9A')
dot.node('End', 'Success!\nReconstruct Path & Return', shape='oval', fillcolor='#A5D6A7')

# 4. Pruning Logic (Pareto)
dot.node('Pruning', 'Is State Dominated?\n(Check best_states[u, t_bin])', shape='diamond', fillcolor='#FFCDD2')
dot.node('DiscardDominated', 'Discard State\n(Dominated)', shape='oval', fillcolor='#EF9A9A')
dot.node('UpdatePareto', 'Update Pareto Frontier\n(Add new, remove worse)')

# 5. Expansion Logic
dot.node('Expand', 'For Each Neighbor (v)\nin Adjacency List')
dot.node('Physics', 'Physics Engine:\n1. Get Wind @ Time\n2. Calc Fuel Burn & Time\n3. Calc Segment Cost')
dot.node('CalcNewState', 'Calculate New State:\nnew_cost += segment_cost\nnew_weight -= fuel_burn\nnew_time += segment_time')

# 6. Constraint Checks (Fuel & Max Time)
dot.node('Constraints', 'Is Weight < Min Dry\nOR\nTime > Max Arrival?', shape='diamond', fillcolor='#FFCDD2')
dot.node('SkipNeighbor', 'Skip Neighbor\n(Invalid)', shape='oval', fillcolor='#EF9A9A')
dot.node('Push', 'Push New State to Queue\n(new_cost, v, new_time, new_weight)')
dot.node('NextNeighbor', 'More Neighbors?', shape='diamond', fillcolor='#FFE0B2')

# --- Define Edges ---

# Initialization -> Loop
dot.edge('Start', 'QueueCheck')

# Queue Loop
dot.edge('QueueCheck', 'NoPath', label='Yes (Empty)')
dot.edge('QueueCheck', 'Pop', label='No')

# Pop -> Goal Check
dot.edge('Pop', 'GoalCheck')

# Goal Check Logic
dot.edge('GoalCheck', 'Pruning', label='No')  # Not destination, continue to standard checks
dot.edge('GoalCheck', 'MinTimeCheck', label='Yes')  # Is destination, check time window

# Min Time Check (Specific to your code)
dot.edge('MinTimeCheck', 'DiscardEarly', label='Yes (< Min)')
dot.edge('DiscardEarly', 'QueueCheck', style='dashed', label='Next Iteration')
dot.edge('MinTimeCheck', 'End', label='No (Valid)')

# Pruning Logic
dot.edge('Pruning', 'DiscardDominated', label='Yes')
dot.edge('DiscardDominated', 'QueueCheck', style='dashed', label='Next Iteration')
dot.edge('Pruning', 'UpdatePareto', label='No')

# Expansion
dot.edge('UpdatePareto', 'Expand')
dot.edge('Expand', 'Physics')
dot.edge('Physics', 'CalcNewState')
dot.edge('CalcNewState', 'Constraints')

# Constraints (Fuel & Max Time)
dot.edge('Constraints', 'SkipNeighbor', label='Yes')
dot.edge('Constraints', 'Push', label='No')
dot.edge('Push', 'NextNeighbor')

# Neighbor Loop Handling
dot.edge('SkipNeighbor', 'NextNeighbor', style='dashed')
dot.edge('NextNeighbor', 'Expand', label='Yes', style='dashed')
dot.edge('NextNeighbor', 'QueueCheck', label='No (All Neighbors Done)', style='dashed')

# --- Render and Save ---
output_path = 'dijkstra_flowchart_v2'
dot.render(output_path, view=True)
print(f"Flowchart saved to: {os.path.abspath(output_path + '.png')}")