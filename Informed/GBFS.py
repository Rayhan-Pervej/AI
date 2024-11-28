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

def greedy_best_first_search(graph, start, goal, heuristic):
    # Initialize the frontier with the starting node (with its heuristic value)
    frontier = [(heuristic[start], start, [start])]  # (heuristic, node, path)
    heapq.heapify(frontier)  # Ensure it’s a min-heap based on heuristic value

    # Visited set to keep track of explored nodes
    visited = set()

    while frontier:
        # Pop the node with the lowest heuristic value
        _, node, path = heapq.heappop(frontier)

        # If we've reached the goal, return the path
        if node == goal:
            return path

        # Mark the node as visited
        if node in visited:
            continue
        visited.add(node)

        # Expand neighbors
        for neighbor, _ in graph.get(node, []):
            if neighbor not in visited:
                new_path = path + [neighbor]
                heapq.heappush(frontier, (heuristic[neighbor], neighbor, new_path))

    # If the goal was not reached
    return None

# Test the function
path_to_goal = greedy_best_first_search(graph, start_node, goal_node, heuristic)
print("Path to goal:", path_to_goal)
