from core.graph import Graph
from core.cycle_detect import detect_cycle

def topological_sort(graph: Graph):
    """
    Find valid installation order using DFS-based Topological Sort.
    
    Logic:
    - Visit each node via DFS
    - Only add a node to result AFTER all its dependencies are processed
    - This guarantees dependencies always come before the package that needs them
    
    NOTE: We first check for cycles — topological sort is only
    possible on a DAG (Directed Acyclic Graph).
    """
    cycle_result = detect_cycle(graph)
    if cycle_result["has_cycle"]:
        return {
            "success": False,
            "order": [],
            "error": f"Cannot resolve — circular dependency detected: {' → '.join(cycle_result['cycle'])}"
        }

    visited = set()
    result_stack = []

    def dfs(node):
        visited.add(node)
        for neighbour in graph.get_neighbours(node):
            if neighbour not in visited:
                dfs(neighbour)
        # Add to stack AFTER all dependencies are processed
        result_stack.append(node)

    for pkg in graph.get_all_packages():
        if pkg not in visited:
            dfs(pkg)

    # Stack is in reverse order — flip it
    install_order = result_stack[::-1]

    return {
        "success": True,
        "order": install_order,
        "error": None
    }