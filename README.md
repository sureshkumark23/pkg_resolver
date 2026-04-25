# 📦 Package Dependency Resolver

![CI](https://github.com/sureshkumark23/pkg_resolver/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.11%20|%203.12-blue)
![Tests](https://img.shields.io/badge/tests-17%20passing-green)

A full-stack developer tool that resolves package dependencies using
core graph algorithms implemented entirely from scratch — no NetworkX
or external graph libraries.

> Every time you run `npm install` or `pip install`, something like
> this runs under the hood. This project builds that engine from scratch.

---

## 🚀 Live Demo

| Input | Output |
|---|---|
| Dependency graph (JSON) | Valid install order |
| Same graph | Circular dependency detection |
| Version requirements (JSON) | Conflict detection |
| Package name | Full impact analysis |

---

## ⚙️ Algorithms Implemented (From Scratch)

| Algorithm | Problem Solved | 
|---|---|
| DFS Topological Sort | Valid install order | 
| DFS Cycle Detection | Circular dependency check | 
| Disjoint Set Union (DSU) | Version conflict detection | 
| BFS on Reversed Graph | Impact analysis | 

---
## 🗂️ Project Structure

```
pkg_resolver/
├── core/
│   ├── graph.py          # Graph builder (adjacency list)
│   ├── topo_sort.py      # Topological sort via DFS
│   ├── cycle_detect.py   # Cycle detection via DFS
│   ├── dsu.py            # Disjoint Set Union + conflict detection
│   └── impact.py         # BFS impact analysis
├── api/
│   └── main.py           # FastAPI REST backend
├── frontend/
│   └── src/
│       └── App.js        # React UI
├── tests/
│   └── test_all.py       # 17 pytest tests
├── .github/
│   └── workflows/
│       └── ci.yml        # GitHub Actions CI
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🛠️ Setup and Run

### Backend

```bash
# Clone the repo
git clone https://github.com/sureshkumark23/pkg_resolver.git
cd pkg_resolver

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start API server
python3 -m uvicorn api.main:app --reload
```

API runs at `http://127.0.0.1:8000`
Interactive docs at `http://127.0.0.1:8000/docs`

### Frontend

```bash
cd frontend
npm install
npm start
```

UI runs at `http://localhost:3000`

---

## 📡 API Endpoints

### POST `/resolve`
Returns valid installation order.
```json
{
  "packages": {
    "react": ["react-dom", "scheduler"],
    "react-dom": ["scheduler"],
    "scheduler": []
  }
}
```
Response:
```json
{
  "success": true,
  "order": ["scheduler", "react-dom", "react"],
  "error": null
}
```

### POST `/detect-cycle`
Detects circular dependencies.
```json
{ "packages": { "A": ["B"], "B": ["C"], "C": ["A"] } }
```
Response:
```json
{ "has_cycle": true, "cycle": ["A", "B", "C", "A"] }
```

### POST `/conflicts`
Detects version conflicts using DSU.
```json
{
  "requirements": {
    "packageA": { "lodash": "3.0" },
    "packageB": { "lodash": "5.0" }
  }
}
```
Response:
```json
{
  "has_conflicts": true,
  "conflicts": [{ "library": "lodash", "conflict": { "3.0": ["packageA"], "5.0": ["packageB"] } }]
}
```

### POST `/impact`
Finds all packages affected when one updates.
```json
{
  "packages": { "react": ["scheduler"], "vue": ["scheduler"], "scheduler": [] },
  "updated_package": "scheduler"
}
```
Response:
```json
{ "updated_package": "scheduler", "affected": ["react", "vue"], "error": null }
```

---

## 🧪 Running Tests

```bash
python3 -m pytest tests/test_all.py -v
```

17 tests covering: graph construction, cycle detection, topological sort,
DSU conflict detection, BFS impact analysis, edge cases, and error handling.

---

## 💡 Why This Project

Most students use NetworkX or similar libraries. This project implements
every algorithm from first principles, directly applying concepts from the
**NPTEL course — Algorithmic Graph Theory and Data Structures (noc26_cs08)**
by Prof. Sourav Mukhopadhyay, IIT Kharagpur.

The problem it solves is not academic — npm, pip, Maven, Gradle, and apt
all use topological sort and cycle detection at their core.

---

## 🏗️ Tech Stack

- **Backend:** Python, FastAPI, Uvicorn
- **Frontend:** React.js
- **Testing:** pytest
- **CI/CD:** GitHub Actions (Python 3.11 + 3.12)
- **Algorithms:** Pure Python — no external graph libraries