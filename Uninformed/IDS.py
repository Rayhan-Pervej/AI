
graph = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': [],
    'E': [],
    'F': ['H'],  # 'H' is a node at depth 4 from the start 'A'
    'G': [],
    'H': []      # Target node
}



def iterative_deepening_search(graph, start, goal, max_depth):

    for depth in range(1, max_depth + 1):
        # Initialize frontier with the start node and initial depth
        frontier = [(start, [start], depth)]
        
        while frontier:
            # Pop a path from the frontier
            node, path, remaining_depth = frontier.pop()
            
            # If the node is the goal, return the path
            if node == goal:
                return path
            
            # If there is depth remaining, add neighbors to the frontier
            if remaining_depth > 0:
                for neighbor in graph.get(node, []):
                    new_path = path + [neighbor]
                    frontier.append((neighbor, new_path, remaining_depth - 1))
                    
    # If goal is not found within max_depth
    return None


start_node = 'A'  # Starting point of the search
goal_node = 'H'   # Target node to search for
max_depth=4
path_to_goal = iterative_deepening_search(graph, start_node, goal_node, max_depth)
print("Path to goal:", path_to_goal)

