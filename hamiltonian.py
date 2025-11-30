import argparse
from typing import List, Tuple
import subprocess
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
def varnum(v, i, n):
    return (v - 1) * n + i
def add_position_at_least_one(clauses, n):
    for i in range(1, n+1):
        clause = []
        for p in range(1, n+1):
            clause.append(varnum(p, i, n))
        clauses.append(clause)
def add_position_at_most_one(clauses, n):
    for i in range(1, n+1):
        for v in range(1, n+1):
            for w in range(v+1, n+1):
                clauses.append([-varnum(v, i, n), -varnum(w, i, n)])
def add_vertex_at_least_one(clauses, n):
    for v in range(1, n+1):
        clause = []
        for i in range(1, n+1):
            clause.append(varnum(v, i, n))
        clauses.append(clause)
def add_vertex_at_most_one(clauses, n):
    for v in range(1, n+1):
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clauses.append([-varnum(v, i, n), -varnum(v, j, n)])
def add_edge_constraints(clauses, graph):
    n = graph.n
    edges = graph.edge_set()
    for i in range(1, n):
        for u in range(1, n+1):
            for v in range(1, n+1):
                if u == v:
                    continue
                if graph.directed:
                    has_edge = (u, v) in edges
                else:
                    a = min(u, v)
                    b = max(u, v)
                    has_edge = (a, b) in edges
                    if not has_edge:
                        clauses.append([-varnum(u, i, n), -varnum(v, i+1, n)])


def build_cnf(graph: Graph):
    n = graph.n
    num_vars = n*n
    clauses = []
    add_position_at_least_one(clauses, n)
    add_position_at_most_one(clauses, n)
    add_vertex_at_least_one(clauses, n)
    add_vertex_at_most_one(clauses, n)
    add_edge_constraints(clauses, graph)
    return clauses, num_vars


def run_glucose(glucose_path: str, cnf_path: str):
    result = subprocess.run(
        [glucose_path, "-model", cnf_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout = result.stdout
    model = []
    sat = None

    for line in stdout.splitlines():
        line = line.strip()

        if line.startswith("s "):
            if "UNSAT" in line:
                sat = False
            elif "SAT" in line:
                sat = True

        if line.startswith("v "):
            for token in line.split()[1:]:
                lit = int(token)
                if lit != 0:
                    model.append(lit)

    return sat, model, stdout


def decode_hamiltonian_path(graph: Graph, model: list):
    n = graph.n
    positive = {lit for lit in model if lit > 0}

    vertex_at_position = [None] * (n + 1)

    for v in range(1, n+1):
        for i in range(1, n+1):
            if varnum(v, i, n) in positive:
                vertex_at_position[i] = v

    return vertex_at_position[1:]
def write_cnf(num_vars: int, clauses: list, path: str, print_cnf: bool = False):
    with open(path, "w", encoding="utf-8") as f:
        header = f"p cnf {num_vars} {len(clauses)}\n"
        f.write(header)
        if print_cnf:
            print(header, end="")

        for clause in clauses:
            line = " ".join(map(str, clause)) + " 0\n"
            f.write(line)
            if print_cnf:
                print(line, end="")

def main():
    args = parse_args()

    graph = read_graph(args.instance, directed=args.directed)
    clauses, num_vars = build_cnf(graph)
    write_cnf(num_vars, clauses, args.cnf_output, args.print_cnf)
    sat, model, raw_output = run_glucose(args.glucose, args.cnf_output)

    if args.print_stats:
        print("Glucose statistics")
        print(raw_output)

    if not sat:
        print("UNSAT: no Hamiltonian path exists for this instance.")
        return

    path = decode_hamiltonian_path(graph, model)

    print("SAT: Hamiltonian path found:")
    print(" ".join(map(str, path)))
if __name__ == "__main__":
    main()