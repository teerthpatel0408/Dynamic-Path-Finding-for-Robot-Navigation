from collections import deque

graph = {'A': ['M', 'P'],
         'M': ['A', 'N'],
         'N': ['M', 'B'],
         'P': ['A', 'B'],
         'B': ['P', 'N']}

def dfs(current, goal, graph, visited):
    if current == goal:
        return True

    for neighbor in graph[current]:
        if neighbor not in visited:
            visited[neighbor] = current
            if dfs(neighbor, goal, graph, visited):
                return True

    return False

def find_path_dfs(start, goal, graph):
    visited = {start: None}
    if dfs(start, goal, graph, visited):
        path = [goal]
        while goal != start:
            goal = visited[goal]
            path.insert(0, goal)
        return path
    else:
        return "No path found"

start = 'A'
goal = 'B'
path = find_path_dfs(start, goal, graph)
if isinstance(path, list):
    print(f'Path from {start} to {goal}:')
    print(' -> '.join(path))
else:
    print(path)