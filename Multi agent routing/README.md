Multi agent routing problems solved with Pyomo. Starting from a distance matrix generated using the DistanceMatrix.py file.

Multiple agents must collectively travel to all the nodes in the matrix and minimize the cost function computed as the cost of travel times the sum of the total distance covered by each agent.

Nodes can be revisited.

If two nodes have a distance of -1 between them, then they are inaccessible.