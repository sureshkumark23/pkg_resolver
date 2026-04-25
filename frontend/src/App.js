import { useState } from "react";
import axios from "axios";

const API = "http://127.0.0.1:8000";

const defaultPackages = `{
  "react": ["react-dom", "scheduler"],
  "react-dom": ["scheduler"],
  "scheduler": [],
  "vue": ["scheduler"]
}`;

const defaultRequirements = `{
  "packageA": {"lodash": "3.0", "axios": "1.0"},
  "packageB": {"lodash": "5.0", "axios": "1.0"}
}`;

export default function App() {
  const [packages, setPackages] = useState(defaultPackages);
  const [requirements, setRequirements] = useState(defaultRequirements);
  const [updatedPkg, setUpdatedPkg] = useState("scheduler");
  const [results, setResults] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function runAll() {
    setLoading(true);
    setError("");
    try {
      const pkgs = JSON.parse(packages);
      const reqs = JSON.parse(requirements);

      const [resolve, cycle, conflict, impact] = await Promise.all([
        axios.post(`${API}/resolve`, { packages: pkgs }),
        axios.post(`${API}/detect-cycle`, { packages: pkgs }),
        axios.post(`${API}/conflicts`, { requirements: reqs }),
        axios.post(`${API}/impact`, {
          packages: pkgs,
          updated_package: updatedPkg
        })
      ]);

      setResults({
        resolve: resolve.data,
        cycle: cycle.data,
        conflict: conflict.data,
        impact: impact.data
      });
    } catch (e) {
      setError("Invalid JSON or server error. Check your input.");
    }
    setLoading(false);
  }

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>📦 Package Dependency Resolver</h1>
      <p style={styles.subtitle}>
        Built from scratch — DFS · Topological Sort · DSU · BFS
      </p>

      {/* Input Section */}
      <div style={styles.grid}>
        <div style={styles.card}>
          <label style={styles.label}>Dependency Graph (JSON)</label>
          <textarea
            style={styles.textarea}
            value={packages}
            onChange={e => setPackages(e.target.value)}
          />
        </div>

        <div style={styles.card}>
          <label style={styles.label}>Version Requirements (JSON)</label>
          <textarea
            style={styles.textarea}
            value={requirements}
            onChange={e => setRequirements(e.target.value)}
          />
          <label style={{ ...styles.label, marginTop: 12 }}>
            Package to update (for impact analysis)
          </label>
          <input
            style={styles.input}
            value={updatedPkg}
            onChange={e => setUpdatedPkg(e.target.value)}
          />
        </div>
      </div>

      <button style={styles.button} onClick={runAll} disabled={loading}>
        {loading ? "Resolving..." : "🚀 Resolve"}
      </button>

      {error && <p style={styles.error}>{error}</p>}

      {/* Results Section */}
      {Object.keys(results).length > 0 && (
        <div style={styles.grid}>
          <ResultCard
            title="✅ Install Order"
            ok={results.resolve?.success}
            content={
              results.resolve?.success
                ? results.resolve.order.join(" → ")
                : results.resolve?.error
            }
          />
          <ResultCard
            title="🔄 Cycle Detection"
            ok={!results.cycle?.has_cycle}
            content={
              results.cycle?.has_cycle
                ? "Cycle: " + results.cycle.cycle.join(" → ")
                : "No circular dependencies found"
            }
          />
          <ResultCard
            title="⚠️ Version Conflicts"
            ok={!results.conflict?.has_conflicts}
            content={
              results.conflict?.has_conflicts
                ? results.conflict.conflicts
                    .map(c => `${c.library}: ${Object.keys(c.conflict).join(" vs ")}`)
                    .join("\n")
                : "No conflicts found"
            }
          />
          <ResultCard
            title="💥 Impact Analysis"
            ok={results.impact?.affected?.length === 0}
            content={
              results.impact?.error
                ? results.impact.error
                : results.impact?.affected?.length > 0
                ? `If '${results.impact.updated_package}' updates:\n${results.impact.affected.join(", ")} are affected`
                : `No packages depend on '${results.impact.updated_package}'`
            }
          />
        </div>
      )}
    </div>
  );
}

function ResultCard({ title, ok, content }) {
  return (
    <div style={{ ...styles.card, borderLeft: `4px solid ${ok ? "#22c55e" : "#ef4444"}` }}>
      <h3 style={{ margin: "0 0 8px", fontSize: 15 }}>{title}</h3>
      <pre style={styles.pre}>{content}</pre>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: 900, margin: "0 auto", padding: 32,
    fontFamily: "system-ui, sans-serif", color: "#1e293b"
  },
  title: { fontSize: 28, fontWeight: 700, margin: 0 },
  subtitle: { color: "#64748b", marginTop: 6, marginBottom: 24 },
  grid: {
    display: "grid", gridTemplateColumns: "1fr 1fr",
    gap: 16, marginBottom: 16
  },
  card: {
    background: "#f8fafc", border: "1px solid #e2e8f0",
    borderRadius: 8, padding: 16
  },
  label: { display: "block", fontWeight: 600, fontSize: 13, marginBottom: 6 },
  textarea: {
    width: "100%", height: 160, fontFamily: "monospace",
    fontSize: 12, border: "1px solid #cbd5e1", borderRadius: 6,
    padding: 8, resize: "vertical", boxSizing: "border-box"
  },
  input: {
    width: "100%", padding: "8px 10px", borderRadius: 6,
    border: "1px solid #cbd5e1", fontSize: 14, boxSizing: "border-box"
  },
  button: {
    background: "#2563eb", color: "#fff", border: "none",
    padding: "12px 32px", borderRadius: 8, fontSize: 15,
    fontWeight: 600, cursor: "pointer", marginBottom: 20
  },
  error: { color: "#ef4444", fontWeight: 600 },
  pre: {
    margin: 0, fontSize: 13, whiteSpace: "pre-wrap",
    wordBreak: "break-word", color: "#334155"
  }
};