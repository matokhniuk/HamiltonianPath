import argparse
from typing import List, Tuple
def parse_args():
    parser = argparse.ArgumentParser(
        description="Hamiltonian Path → SAT → Glucose"
    )

    parser.add_argument(
        "--instance", required=True,
        help="Path to graph instance file"
    )

    parser.add_argument(
        "--glucose", required=True,
        help="Path to Glucose 4.2 executable"
    )

    parser.add_argument(
        "--directed", action="store_true",
        help="Interpret input graph as directed. Default: undirected."
    )

    parser.add_argument(
        "--cnf-output", default="formula.cnf",
        help="Where to write generated DIMACS CNF. Default: formula.cnf"
    )

    parser.add_argument(
        "--print-cnf", action="store_true",
        help="Also print CNF formula to stdout"
    )

    parser.add_argument(
        "--print-stats", action="store_true",
        help="Print Glucose statistics (raw solver output)"
    )

    return parser.parse_args()
class Graph:
    def __init__(self, n: int, edges: List[Tuple[int, int]], directed: bool = False):
        self.n = n                
        self.edges = edges         
        self.directed = directed  

    def edge_set(self):
        s = set()
        if self.directed:
            for u, v in self.edges:
                s.add((u, v))
        else:
            for u, v in self.edges:
                if u > v:
                    u, v = v, u
                s.add((u, v))
        return s
def read_graph(path: str, directed: bool = False) -> Graph:
    lines = []
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            lines.append(line)

    if not lines:
        raise ValueError("File is empty or contains only comments.")

    header = lines[0].split()
    if len(header) != 2:
        raise ValueError("The first non-comment line must be in the format: n m")

    n = int(header[0])
    m = int(header[1])

    edges: List[Tuple[int, int]] = []

    for idx, line in enumerate(lines[1:], start=2):
        parts = line.split()
        if len(parts) != 2:
            raise ValueError(f"Invalid line (expected 'u v'): line {idx}: {line}")
        u = int(parts[0])
        v = int(parts[1])

        if not (1 <= u <= n and 1 <= v <= n):
            raise ValueError(f"Error: vertices {u},{v} are outside the range 1..{n} (line {idx})")

        edges.append((u, v))

    if len(edges) != m:
        print(f"Warning: header says m={m}, but found {len(edges)} edges.")

    return Graph(n=n, edges=edges, directed=directed)