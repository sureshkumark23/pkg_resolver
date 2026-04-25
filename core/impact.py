from core.graph import Graph
from collections import deque

def get_impact(graph: Graph, updated_package: str):
    """
    Find all packages affected when updated_package changes.

    Logic:
    - Reverse the graph (flip all edges)
    - In reversed graph: edge goes FROM dependency TO dependent
    - BFS from updated_package on reversed graph
    - All reachable nodes = packages that depend on it (directly or indirectly)

    Example:
    Original:  react → scheduler,  react-dom → scheduler
    Reversed:  scheduler → react,  scheduler → react-dom

    BFS from scheduler → finds react-dom, react
    Meaning: if scheduler updates, react-dom and react are affected
    """
    if updated_package not in graph.get_all_packages():
        return {
            "updated_package": updated_package,
            "affected": [],
            "error": f"Package '{updated_package}' not found in graph"
        }

    reversed_graph = graph.get_reversed()

    visited = set()
    queue = deque()

    queue.append(updated_package)
    visited.add(updated_package)

    while queue:
        current = queue.popleft()
        for neighbour in reversed_graph.get_neighbours(current):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)

    # Remove the updated package itself from affected list
    affected = [pkg for pkg in visited if pkg != updated_package]

    return {
        "updated_package": updated_package,
        "affected": affected,
        "error": None
    }