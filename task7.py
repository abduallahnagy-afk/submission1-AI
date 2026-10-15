"""
Exercise 7 — BFS vs A*  |  10×10 maze  S(0,0) → E(9,9)
Run:  python maze_solver.py
"""

from collections import deque
import heapq, time

OPEN = {
    (0,0),(0,1),(0,3),(0,4),(0,5),(0,7),(0,8),(0,9),
    (1,1),(1,3),(1,5),(1,6),(1,8),
    (2,0),(2,1),(2,2),(2,3),(2,5),(2,7),(2,8),(2,9),
    (3,0),(3,2),(3,4),(3,5),(3,7),(3,9),
    (4,0),(4,2),(4,3),(4,4),(4,6),(4,7),(4,9),
    (5,0),(5,1),(5,4),(5,6),(5,8),(5,9),
    (6,1),(6,2),(6,4),(6,5),(6,6),(6,8),
    (7,0),(7,2),(7,3),(7,4),(7,6),(7,7),(7,8),(7,9),
    (8,0),(8,4),(8,5),(8,9),
    (9,0),(9,1),(9,2),(9,3),(9,4),(9,6),(9,7),(9,8),(9,9),
}
S, E = (0, 0), (9, 9)

def nbrs(r, c):
    return [(r+dr, c+dc) for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]
            if (r+dr, c+dc) in OPEN]

def bfs():
    t0 = time.perf_counter()
    q = deque([(S, [S])]); vis = {S}; exp = 0; mf = 1
    while q:
        mf = max(mf, len(q)); node, p = q.popleft(); exp += 1
        if node == E:
            return dict(path=p, steps=len(p)-1, ms=(time.perf_counter()-t0)*1e3)
        for nb in nbrs(*node):
            if nb not in vis: vis.add(nb); q.append((nb, p+[nb]))

def astar():
    t0 = time.perf_counter()
    h  = lambda a, b: abs(a[0]-b[0]) + abs(a[1]-b[1])
    heap = [(h(S,E), 0, 0, S, [S])]; g = {S: 0}; exp = 0; mf = 1; ctr = 0
    while heap:
        mf = max(mf, len(heap)); f, gc, _, node, p = heapq.heappop(heap)
        if gc > g.get(node, 1e9): continue
        exp += 1
        if node == E:
            return dict(path=p, steps=len(p)-1, ms=(time.perf_counter()-t0)*1e3)
        for nb in nbrs(*node):
            ng = gc + 1
            if ng < g.get(nb, 1e9):
                g[nb] = ng; ctr += 1
                heapq.heappush(heap, (ng+h(nb,E), ng, ctr, nb, p+[nb]))

# ── Colours ───────────────────────────────────────────────────
RD = "\033[91;1m"; GN = "\033[92;1m"; YL = "\033[93;1m"
CY = "\033[96;1m"; WT = "\033[97m";   N  = "\033[0m"
ARROWS = {(1,0):"↓", (-1,0):"↑", (0,1):"→", (0,-1):"←"}

# ── Table ─────────────────────────────────────────────────────
def table(b, a):
    LW, CW = 22, 18
    line = "  ╠" + "═"*LW + "╬" + "═"*CW + "╬" + "═"*CW + "╣"
    top  = "  ╔" + "═"*LW + "╦" + "═"*CW + "╦" + "═"*CW + "╗"
    bot  = "  ╚" + "═"*LW + "╩" + "═"*CW + "╩" + "═"*CW + "╝"

    def hdr():
        return (f"  ║{' Metric':<{LW}}║"
                f" {RD}{'BFS':^{CW-1}}{N}║"
                f" {GN}{'A*':^{CW-1}}{N}║")

    def row(label, bv, av):
        return (f"  ║ {CY}{label:<{LW-1}}{N}║"
                f" {WT}{str(bv):^{CW-1}}{N}║"
                f" {WT}{str(av):^{CW-1}}{N}║")

    print(top)
    print(hdr())
    print(line)
    print(row("Path Length",       b['steps'],          a['steps']))
    print(line)
    print(row("Time Complexity",   "O(V + E)",           "O(b^d · log b^d)"))
    print(line)
    print(row("Space Complexity",  "O(V)",               "O(b^d)"))
    print(line)
    print(row("Time Taken (ms)",   f"{b['ms']:.3f}",     f"{a['ms']:.3f}"))
    print(bot)

# ── Draw maze ─────────────────────────────────────────────────
def draw(result, title):
    path = result['path']
    pm   = {path[i]: ARROWS[(path[i+1][0]-path[i][0], path[i+1][1]-path[i][1])]
            for i in range(len(path)-1)}
    print(f"\n  ╔{'═'*20}╗")
    print(f"  ║  {title:<18}║")
    print(f"  ╠{'═'*20}╣")
    for r in range(10):
        row = "  ║"
        for c in range(10):
            p = (r, c)
            if   p == S:    row += f"{RD}S {N}"
            elif p == E:    row += f"{GN}E {N}"
            elif p in pm:   row += f"{YL}{pm[p]} {N}"
            elif p in OPEN: row += f"{WT}· {N}"
            else:           row += "  "
        print(row + "║")
    print(f"  ╚{'═'*20}╝")

# ── Main ──────────────────────────────────────────────────────
b, a = bfs(), astar()

print(f"\n{'═'*52}")
print(f"{'BFS vs A*  ·  10×10 Maze  ·  S(0,0) → E(9,9)':^52}")
print(f"{'═'*52}\n")

table(b, a)
draw(b, "BFS — Breadth-First")
draw(a, "A* — Manhattan h(n)")
print(f"\n  Legend: {RD}S{N} Start  {GN}E{N} End  {YL}↑↓←→{N} Path  {WT}·{N} Open  (space) Wall\n")