from core.graph import Graph

def detect_cycle(graph: Graph):
    """
    Detect circular dependencies using DFS 3-colour marking.
    WHITE (0) = not visited
    GRAY  (1) = currently being visited (in current DFS path)
    BLACK (2) = fully processed

    If we hit a GRAY node during DFS → cycle found.
    """
    WHITE, GRAY, BLACK = 0, 1, 2
    colour = {pkg: WHITE for pkg in graph.get_all_packages()}
    cycle_path = []

    def dfs(node, path):
        colour[node] = GRAY
        path.append(node)

        for neighbour in graph.get_neighbours(node):
            if colour[neighbour] == GRAY:
                # Found cycle — extract the cycle portion
                cycle_start = path.index(neighbour)
                cycle_path.extend(path[cycle_start:] + [neighbour])
                return True
            if colour[neighbour] == WHITE:
                if dfs(neighbour, path):
                    return True

        colour[node] = BLACK
        path.pop()
        return False

    for pkg in graph.get_all_packages():
        if colour[pkg] == WHITE:
            if dfs(pkg, []):
                return {
                    "has_cycle": True,
                    "cycle": cycle_path
                }

    return {
        "has_cycle": False,
        "cycle": []
    }