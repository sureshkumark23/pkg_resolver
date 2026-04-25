class DSU:
    """
    Disjoint Set Union (Union-Find) with:
    - Path compression (find is O(α(n)) ≈ O(1))
    - Union by rank (keeps tree flat)
    """
    def __init__(self):
        self.parent = {}
        self.rank = {}

    def add(self, x):
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0

    def find(self, x):
        # Path compression
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        # Union by rank
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1

    def connected(self, x, y):
        return self.find(x) == self.find(y)


def detect_conflicts(version_requirements: dict):
    """
    Detect version conflicts across packages.

    Input format:
    {
        "packageA": {"lodash": "3.0"},
        "packageB": {"lodash": "5.0"},
        "packageC": {"lodash": "3.0"}
    }

    Logic:
    - For each library, group all required versions
    - If same library has 2+ different versions required → conflict
    - DSU groups compatible (same version) requirements together
    """
    dsu = DSU()
    # library → { version → requiring_package }
    library_versions = {}

    for pkg, deps in version_requirements.items():
        for library, version in deps.items():
            if library not in library_versions:
                library_versions[library] = {}
            if version not in library_versions[library]:
                library_versions[library][version] = []
            library_versions[library][version].append(pkg)

    conflicts = []

    for library, versions in library_versions.items():
        version_list = list(versions.keys())

        # Add all versions of this library to DSU
        for v in version_list:
            node = f"{library}@{v}"
            dsu.add(node)

        # Union same-version nodes (they are compatible)
        for i in range(1, len(version_list)):
            if version_list[i] == version_list[0]:
                dsu.union(
                    f"{library}@{version_list[0]}",
                    f"{library}@{version_list[i]}"
                )

        # If multiple distinct versions exist → conflict
        if len(version_list) > 1:
            distinct = list(set(version_list))
            if len(distinct) > 1:
                conflicts.append({
                    "library": library,
                    "conflict": {
                        v: versions[v] for v in distinct
                    }
                })

    return {
        "has_conflicts": len(conflicts) > 0,
        "conflicts": conflicts
    }