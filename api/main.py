from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from core.graph import Graph
from core.topo_sort import topological_sort
from core.cycle_detect import detect_cycle
from core.dsu import detect_conflicts
from core.impact import get_impact

app = FastAPI(title="Package Dependency Resolver")

# Allow React frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# ─── Request Models ───────────────────────────────────────

class DepsInput(BaseModel):
    packages: dict  # { "react": ["react-dom", "scheduler"] }

class ConflictInput(BaseModel):
    requirements: dict  # { "pkgA": {"lodash": "3.0"} }

class ImpactInput(BaseModel):
    packages: dict
    updated_package: str

# ─── Routes ───────────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "Package Dependency Resolver API is running"}


@app.post("/resolve")
def resolve(data: DepsInput):
    """Return valid install order via topological sort."""
    g = Graph()
    g.build_from_dict(data.packages)
    return topological_sort(g)


@app.post("/detect-cycle")
def cycle(data: DepsInput):
    """Detect circular dependencies."""
    g = Graph()
    g.build_from_dict(data.packages)
    return detect_cycle(g)


@app.post("/conflicts")
def conflicts(data: ConflictInput):
    """Detect version conflicts using DSU."""
    return detect_conflicts(data.requirements)


@app.post("/impact")
def impact(data: ImpactInput):
    """Find all packages affected when one package updates."""
    g = Graph()
    g.build_from_dict(data.packages)
    return get_impact(g, data.updated_package)