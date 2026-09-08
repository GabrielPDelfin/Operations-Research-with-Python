Multi agent routing problems solved with Pyomo. Starting from a graph represented by a distance matrix generated using the DistanceMatrix.py file.

Multiple agents must collectively visit all the nodes in the graph and minimize the cost function computed as the cost of travel times the sum of the total distance covered by each agent.

All nodes can be revisited by any agent.

If two nodes have a distance of -1 between them, then they are inaccessible.

The indices are:
- K: Set of agents/people
- T: Number of times an agent can move per trip. If T is too low then the model won't be able to find a feasible solution.
- N: Set of nodes on the graph
- E: Set of valid edges on the graph (no -1s)

The variables are:
- X: Binary. Edges between nodes that are chosen
- Y: Binary. Node where an agent is located at time t
