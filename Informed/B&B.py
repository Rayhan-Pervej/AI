import heapq  # Import heapq to use a priority queue

def branch_and_bound_shortest_path(graph, start, goal):
    # Initialize the priority queue with the starting node at cost 0
    frontier = [(0, [start])]  # (cost, path)
    heapq.heapify(frontier)  # Ensure the frontier is a min-heap based on path cost

    # Initialize the upper bound to infinity as no solution has been found yet
    upper_bound = float('inf')
    best_path = None  # To store the best (shortest) path to the goal

    # Main loop to explore the frontier
    while frontier:
        # Pop the path with the lowest cost from the priority queue
        current_cost, path = heapq.heappop(frontier)
        current_node = path[-1]  # Get the last node in the current path

        # Pruning step: If the current path cost is greater than or equal to the best found cost (upper bound), skip expansion
        if current_cost >= upper_bound:
            continue  # Prune this path

        # Check if the current node is the goal
        if current_node == goal:
            # Update the best solution (upper bound) if the current path cost is the lowest found
            upper_bound = current_cost
            best_path = path
            continue  # Continue to explore other potential paths

        # Expand each neighbor of the current node
        for neighbor, edge_cost in graph.get(current_node, []):
            # Calculate the new cost to reach this neighbor
            new_cost = current_cost + edge_cost
            # Create a new path by adding the neighbor to the current path
            new_path = path + [neighbor]

            # Add this new path to the frontier if it's within the current upper bound
            if new_cost < upper_bound:
                heapq.heappush(frontier, (new_cost, new_path))
    
    # Return the best path and cost found after all paths are explored or pruned
    return best_path, upper_bound

# Define a sample graph
graph = {
    'A': [('B', 4), ('C', 2), ('Goal', 3)],
    'B': [('C', 5), ('D', 6), ('Goal', 6)],
    'C': [('D', 3)],
    'D': [('Goal', 4)],
    'F': [('Goal', 2)],
    'Goal': []
}

# Execute the Branch and Bound algorithm
best_path, best_cost = branch_and_bound_shortest_path(graph, 'A', 'Goal')
print("Best path:", best_path)  # Outputs the shortest path to the goal
print("Minimum cost:", best_cost)  # Outputs the minimum cost to reach the goal
