class Graph:
    def __init__(self):
        # adjacency list: { "react": ["react-dom", "scheduler"] }
        self.adj = {}

    def add_package(self, package: str):
        """Add a package node if it doesn't exist."""
        if package not in self.adj:
            self.adj[package] = []

    def add_dependency(self, package: str, depends_on: str):
        """Add edge: package → depends_on"""
        self.add_package(package)
        self.add_package(depends_on)
        if depends_on not in self.adj[package]:
            self.adj[package].append(depends_on)

    def get_neighbours(self, package: str):
        """Return all dependencies of a package."""
        return self.adj.get(package, [])

    def get_all_packages(self):
        """Return all package names."""
        return list(self.adj.keys())

    def build_from_dict(self, data: dict):
        """
        Build graph from a dict like:
        { "react": ["react-dom", "scheduler"], "scheduler": [] }
        """
        for package, deps in data.items():
            self.add_package(package)
            for dep in deps:
                self.add_dependency(package, dep)

    def get_reversed(self):
        """
        Return a new Graph with all edges flipped.
        Used for BFS impact analysis.
        A → B becomes B → A
        """
        reversed_graph = Graph()
        for package in self.adj:
            reversed_graph.add_package(package)
        for package, deps in self.adj.items():
            for dep in deps:
                reversed_graph.add_dependency(dep, package)
        return reversed_graph

    def __repr__(self):
        return f"Graph({self.adj})"