import graphviz
import os

# Create the Directed Graph
dot = graphviz.Digraph(comment='Dynamic Dijkstra Flowchart', format='png')
dot.attr(rankdir='TB', size='8,12')  # Top-Bottom direction

# --- Define Nodes ---
# Styles
dot.attr('node', shape='box', style='filled', fillcolor='#E3F2FD', fontname='Arial')

# 1. Initialization
dot.node('Start', 'Start\n(Init Queue: StartNode, Time=0, Weight=Initial)', shape='oval', fillcolor='#C8E6C9')

# 2. Main Loop
dot.node('QueueCheck', 'Is Queue Empty?', shape='diamond', fillcolor='#FFE0B2')
dot.node('NoPath', 'No Path Found', shape='oval', fillcolor='#FFCDD2')
dot.node('Pop', 'Pop Lowest Cost State\n(cost, u, time, weight)')

# 3. Goal Check
dot.node('GoalCheck', 'Is Node (u) == Destination?', shape='diamond', fillcolor='#FFE0B2')
dot.node('End', 'Reconstruct Path & Return\n(Apply ToA penalty if applicable)', shape='oval', fillcolor='#A5D6A7')

# 4. Pruning Logic
dot.node('Pruning', 'Is State Dominated?\n(Pareto Check at time bin)', shape='diamond', fillcolor='#FFCDD2')
dot.node('DiscardDominated', 'Discard State\n(Dominated)', shape='oval', fillcolor='#EF9A9A')
dot.node('UpdatePareto', 'Update Pareto Frontier\n(Remove dominated states)')

# 5. Expansion Logic
dot.node('Expand', 'For Each Neighbor (v)\nin Adjacency List')
dot.node('Physics', 'Physics Engine:\n1. Get Wind @ Time\n2. Calc Fuel Burn & Time\n3. Calc Segment Cost')
dot.node('CalcNewState', 'Calculate New State:\nnew_cost = cost + segment_cost\nnew_weight = weight - fuel_burn\nnew_time = time + segment_time')
dot.node('Feasible', 'Is new_weight >= 0?', shape='diamond', fillcolor='#FFCDD2')
dot.node('SkipNeighbor', 'Skip Neighbor\n(Infeasible)', shape='oval', fillcolor='#EF9A9A')
dot.node('ApplyPenalty', 'If v == Destination:\nApply ToA Penalty to cost')
dot.node('Push', 'Push New State to Queue\n(new_cost, v, new_time, new_weight)')
dot.node('NextNeighbor', 'More Neighbors?', shape='diamond', fillcolor='#FFE0B2')

# --- Define Edges ---
dot.edge('Start', 'QueueCheck')

# Queue Check
dot.edge('QueueCheck', 'Pop', label='No (has states)')
dot.edge('QueueCheck', 'NoPath', label='Yes (empty)')

# Pop and Goal Check
dot.edge('Pop', 'GoalCheck')
dot.edge('GoalCheck', 'End', label='Yes')
dot.edge('GoalCheck', 'Pruning', label='No')

# Pruning
dot.edge('Pruning', 'DiscardDominated', label='Yes')
dot.edge('DiscardDominated', 'QueueCheck', style='dashed', label='Loop Back')
dot.edge('Pruning', 'UpdatePareto', label='No')
dot.edge('UpdatePareto', 'Expand')

# Neighbor Expansion
dot.edge('Expand', 'Physics')
dot.edge('Physics', 'CalcNewState')
dot.edge('CalcNewState', 'Feasible')


dot.edge('Feasible', 'SkipNeighbor', label='No (crash)')
dot.edge('Feasible', 'ApplyPenalty', label='Yes')
dot.edge('ApplyPenalty', 'Push')
dot.edge('Push', 'NextNeighbor')

# Neighbor Loop
dot.edge('SkipNeighbor', 'NextNeighbor', style='dashed')
dot.edge('NextNeighbor', 'Expand', label='Yes', style='dashed')
dot.edge('NextNeighbor', 'QueueCheck', label='No (all done)', style='dashed')

# --- Render and Save ---
output_path = 'dijkstra_flowchart'
dot.render(output_path, view=True)
print(f"Flowchart saved to: {os.path.abspath(output_path + '.png')}")