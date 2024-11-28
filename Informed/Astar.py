import heapq

# Define the graph with weighted edges
graph = {
    'A': [('B', 3), ('C', 4), ('D', 2), ('G', 6)],
    'B': [('D', 5), ('H', 4)],
    'C': [('A', 4), ('E', 3)],
    'D': [('F', 4), ('H', 3)],
    'E': [('G', 2)],
    'F': [('H', 7)],
    'G': [('H', 1)],
    'H': []  # Goal node with no outgoing connections
}

# Define heuristic values for each node (estimated cost to reach 'H')
heuristic = {
    'A': 7,
    'B': 6,
    'C': 4,
    'D': 3,
    'E': 6,
    'F': 3,
    'G': 2,
    'H': 0  # Goal node heuristic is always 0
}

# Define the start and goal nodes
start_node = 'A'
goal_node = 'H'

def a_star_search(graph, start, goal, heuristic):
    # Priority queue for the frontier, initialized with the start node
    frontier = [(0 + heuristic[start], 0, start, [start])]  # (f(n), g(n), node, path)
    heapq.heapify(frontier)

    # Dictionary to track the best cost to reach each node
    best_costs = {start: 0}

    while frontier:
        # Pop the node with the lowest f(n) value
        f, g, node, path = heapq.heappop(frontier)

        # If we reached the goal, return the path and the total cost
        if node == goal:
            return path, g

        # Expand neighbors
        for neighbor, cost in graph.get(node, []):
            new_cost = g + cost
            if neighbor not in best_costs or new_cost < best_costs[neighbor]:
                best_costs[neighbor] = new_cost
                f_neighbor = new_cost + heuristic[neighbor]
                new_path = path + [neighbor]
                heapq.heappush(frontier, (f_neighbor, new_cost, neighbor, new_path))

    # If the goal was not reached
    return None, None

# Test the function
path_to_goal, cost_to_goal = a_star_search(graph, start_node, goal_node, heuristic)
print("Path to goal:", path_to_goal)
print("Total cost to goal:", cost_to_goal)
