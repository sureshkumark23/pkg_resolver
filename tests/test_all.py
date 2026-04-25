import pytest
from core.graph import Graph
from core.cycle_detect import detect_cycle
from core.topo_sort import topological_sort
from core.dsu import detect_conflicts
from core.impact import get_impact

# ─── Helpers ──────────────────────────────────────────────

def make_graph(data):
    g = Graph()
    g.build_from_dict(data)
    return g

# ─── Graph Tests ──────────────────────────────────────────

def test_graph_builds_correctly():
    g = make_graph({"A": ["B"], "B": []})
    assert "A" in g.get_all_packages()
    assert "B" in g.get_neighbours("A")

def test_graph_reversed():
    g = make_graph({"A": ["B"], "B": []})
    rev = g.get_reversed()
    assert "A" in rev.get_neighbours("B")

def test_graph_empty():
    g = Graph()
    assert g.get_all_packages() == []

# ─── Cycle Detection Tests ────────────────────────────────

def test_no_cycle():
    g = make_graph({
        "react": ["react-dom", "scheduler"],
        "react-dom": ["scheduler"],
        "scheduler": []
    })
    result = detect_cycle(g)
    assert result["has_cycle"] == False
    assert result["cycle"] == []

def test_simple_cycle():
    g = make_graph({"A": ["B"], "B": ["C"], "C": ["A"]})
    result = detect_cycle(g)
    assert result["has_cycle"] == True
    assert len(result["cycle"]) > 0

def test_self_cycle():
    g = make_graph({"A": ["A"]})
    result = detect_cycle(g)
    assert result["has_cycle"] == True

def test_single_node_no_cycle():
    g = make_graph({"A": []})
    result = detect_cycle(g)
    assert result["has_cycle"] == False

# ─── Topological Sort Tests ───────────────────────────────

def test_topo_sort_correct_order():
    g = make_graph({
        "react": ["scheduler"],
        "scheduler": []
    })
    result = topological_sort(g)
    assert result["success"] == True
    order = result["order"]
    # scheduler must come before react
    assert order.index("scheduler") > order.index("react")

def test_topo_sort_fails_on_cycle():
    g = make_graph({"A": ["B"], "B": ["A"]})
    result = topological_sort(g)
    assert result["success"] == False
    assert "circular" in result["error"].lower()

def test_topo_sort_single_package():
    g = make_graph({"A": []})
    result = topological_sort(g)
    assert result["success"] == True
    assert result["order"] == ["A"]

def test_topo_sort_all_independent():
    g = make_graph({"A": [], "B": [], "C": []})
    result = topological_sort(g)
    assert result["success"] == True
    assert set(result["order"]) == {"A", "B", "C"}

# ─── DSU Conflict Tests ───────────────────────────────────

def test_conflict_detected():
    reqs = {
        "pkgA": {"lodash": "3.0"},
        "pkgB": {"lodash": "5.0"}
    }
    result = detect_conflicts(reqs)
    assert result["has_conflicts"] == True
    assert any(c["library"] == "lodash" for c in result["conflicts"])

def test_no_conflict_same_version():
    reqs = {
        "pkgA": {"lodash": "3.0"},
        "pkgB": {"lodash": "3.0"}
    }
    result = detect_conflicts(reqs)
    assert result["has_conflicts"] == False

def test_no_conflict_empty():
    result = detect_conflicts({})
    assert result["has_conflicts"] == False

# ─── BFS Impact Tests ─────────────────────────────────────

def test_impact_direct():
    g = make_graph({
        "react": ["scheduler"],
        "scheduler": []
    })
    result = get_impact(g, "scheduler")
    assert "react" in result["affected"]

def test_impact_transitive():
    g = make_graph({
        "A": ["B"],
        "B": ["C"],
        "C": []
    })
    result = get_impact(g, "C")
    assert "B" in result["affected"]
    assert "A" in result["affected"]

def test_impact_unknown_package():
    g = make_graph({"A": []})
    result = get_impact(g, "unknown")
    assert result["error"] is not None

def test_impact_no_dependents():
    g = make_graph({"A": ["B"], "B": []})
    result = get_impact(g, "A")
    assert result["affected"] == []