import heapq

# Define the graph as a dictionary where each node has a list of (neighbor, cost) tuples
graph = {
    'A': [('B', 3), ('C', 4), ('D', 5), ('H', 4)],
    'B': [],
    'C': [('E', 3)],
    'D': [('F', 4)],
    'E': [('B', 2)],
    'F': [('H', 7)],
    'G': [('A', 1),('D', 3),('E', 2)],
    'H': [('B', 2), ('D', 4), ('G', 1)]  # Goal node with no outgoing connections
}

# Define the start and goal nodes
start_node = 'A'
goal_node = 'B'

def lowest_cost_search(graph, start, goal):
    # Initialize the frontier with the starting node (cost=0)
    frontier = [(0, start, [start])]  # (cost, node, path)
    heapq.heapify(frontier)  # Ensure it’s a min-heap for cost-based priority

    # Initialize visited dictionary to keep track of the lowest cost to each node
    visited = {}

    while frontier:
        # Pop the path with the lowest accumulated cost
        current_cost, node, path = heapq.heappop(frontier)

        # If we've reached the goal, return the path and the cost
        if node == goal:
            return path, current_cost

        # Skip if we've found a cheaper path to this node already
        if node in visited and visited[node] <= current_cost:
            continue

        # Update the lowest cost to reach this node
        visited[node] = current_cost

        # Explore neighbors
        for neighbor, edge_cost in graph.get(node, []):
            new_cost = current_cost + edge_cost
            new_path = path + [neighbor]
            heapq.heappush(frontier, (new_cost, neighbor, new_path))

    # If the goal was not reached
    return None, float('inf')

# Test the function
path_to_goal, cost_to_goal = lowest_cost_search(graph, start_node, goal_node)
print("Path to goal:", path_to_goal)
print("Cost to goal:", cost_to_goal)
