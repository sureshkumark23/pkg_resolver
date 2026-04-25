from core.graph import Graph
from core.impact import get_impact

g = Graph()
g.build_from_dict({
    "react": ["react-dom", "scheduler"],
    "react-dom": ["scheduler"],
    "scheduler": [],
    "vue": ["scheduler"]
})

print(get_impact(g, "scheduler"))
print(get_impact(g, "react-dom"))
print(get_impact(g, "angular"))