import heapq
import time

# Goal state of the 8-puzzle (0 represents the empty space)
GOAL_STATE = (
    (1, 2, 3),
    (4, 5, 6),
    (7, 8, 0)
)

# Precompute goal positions for fast heuristic lookups
GOAL_POS = {}
for r in range(3):
    for c in range(3):
        val = GOAL_STATE[r][c]
        GOAL_POS[val] = (r, c)


# ==========================================
# HELPER: 3X3 BOX GRID VISUALIZER
# ==========================================
def print_grid(state):
    """Prints a state as a clean 3x3 visual box."""
    print("┌───┬───┬───┐")
    for i, row in enumerate(state):
        row_str = " │ ".join(str(val) if val != 0 else " " for val in row)
        print(f"│ {row_str} │")
        if i < 2:
            print("├───┼───┼───┤")
    print("└───┴───┴───┘")


# ==========================================
# 1. HEURISTIC FUNCTIONS DESIGN
# ==========================================

def h_misplaced(state):
    """Heuristic 1: Number of misplaced tiles (Hamming distance)."""
    count = 0
    for r in range(3):
        for c in range(3):
            val = state[r][c]
            if val != 0 and val != GOAL_STATE[r][c]:
                count += 1
    return count

def h_manhattan(state):
    """Heuristic 2: Sum of Manhattan distances for all tiles."""
    dist = 0
    for r in range(3):
        for c in range(3):
            val = state[r][c]
            if val != 0:
                goal_r, goal_c = GOAL_POS[val]
                dist += abs(r - goal_r) + abs(c - goal_c)
    return dist

def h_linear_conflict(state):
    """Heuristic 3: Manhattan Distance + Linear Conflict (Advanced)."""
    manhattan = h_manhattan(state)
    conflicts = 0
    
    # Check row conflicts
    for r in range(3):
        max_val = -1
        for c in range(3):
            val = state[r][c]
            if val != 0 and GOAL_POS[val][0] == r:
                if val > max_val:
                    max_val = val
                else:
                    conflicts += 2
                    
    # Check column conflicts
    for c in range(3):
        max_val = -1
        for r in range(3):
            val = state[r][c]
            if val != 0 and GOAL_POS[val][1] == c:
                if val > max_val:
                    max_val = val
                else:
                    conflicts += 2
                    
    return manhattan + conflicts


# ==========================================
# SOLVABILITY CHECK
# ==========================================
def is_solvable(state):
    """An 8-puzzle is solvable if the number of inversions is even."""
    flat = [val for row in state for val in row if val != 0]
    inversions = 0
    for i in range(len(flat)):
        for j in range(i + 1, len(flat)):
            if flat[i] > flat[j]:
                inversions += 1
    return inversions % 2 == 0


# ==========================================
# A* SEARCH ALGORITHM
# ==========================================
def get_neighbors(state):
    neighbors = []
    empty_pos = None
    for r in range(3):
        for c in range(3):
            if state[r][c] == 0:
                empty_pos = (r, c)
                break
        if empty_pos:
            break
            
    r, c = empty_pos
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)] # Up, Down, Left, Right
    
    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            new_state = [list(row) for row in state]
            new_state[r][c], new_state[nr][nc] = new_state[nr][nc], new_state[r][c]
            neighbors.append(tuple(tuple(row) for row in new_state))
            
    return neighbors

def a_star_search(initial_state, heuristic_func):
    """Runs A* search and returns performance metrics."""
    if not is_solvable(initial_state):
        return {"solvable": False, "nodes_expanded": 0, "time_taken": 0, "path_length": 0}
        
    start_time = time.perf_counter()
    
    h_start = heuristic_func(initial_state)
    pq = [(h_start, 0, initial_state, [initial_state])]
    g_scores = {initial_state: 0}
    nodes_expanded = 0
    
    while pq:
        f, g, current, path = heapq.heappop(pq)
        
        if current == GOAL_STATE:
            end_time = time.perf_counter()
            return {
                "solvable": True,
                "nodes_expanded": nodes_expanded,
                "time_taken": (end_time - start_time) * 1000, # in milliseconds
                "path_length": len(path) - 1
            }
            
        if g > g_scores.get(current, float('inf')):
            continue
            
        nodes_expanded += 1
        
        for neighbor in get_neighbors(current):
            new_g = g + 1
            if new_g < g_scores.get(neighbor, float('inf')):
                g_scores[neighbor] = new_g
                f_score = new_g + heuristic_func(neighbor)
                heapq.heappush(pq, (f_score, new_g, neighbor, path + [neighbor]))
                
    return {"solvable": True, "nodes_expanded": nodes_expanded, "time_taken": 0, "path_length": 0}


# ==========================================
# 2. INITIAL STATES BENCHMARK
# ==========================================
INITIAL_STATES = [
    {
        "name": "State 1 (Easy - 4 moves)",
        "grid": ((1, 2, 3), (4, 5, 6), (7, 0, 8))
    },
    {
        "name": "State 2 (Medium - 10 moves)",
        "grid": ((1, 2, 3), (4, 0, 5), (7, 8, 6))
    },
    {
        "name": "State 3 (Hard - 18 moves)",
        "grid": ((1, 3, 0), (4, 2, 5), (7, 8, 6))
    },
    {
        "name": "State 4 (Complex - 24 moves)",
        "grid": ((8, 6, 7), (2, 5, 4), (3, 0, 1))
    },
    {
        "name": "State 5 (Unsolvable Configuration)",
        "grid": ((1, 2, 3), (4, 5, 6), (8, 7, 0))
    }
]

HEURISTICS = [
    ("Misplaced Tiles", h_misplaced),
    ("Manhattan Distance", h_manhattan),
    ("Linear Conflict + Manhattan", h_linear_conflict)
]

if __name__ == "__main__":
    print("=" * 95)
    print(f"{'8-PUZZLE PRACTICAL BENCHMARK: HEURISTIC COMPARISON':^95}")
    print("=" * 95)
    
    for state_info in INITIAL_STATES:
        name = state_info["name"]
        grid = state_info["grid"]
        
        print(f"\n--- {name} ---")
        print_grid(grid)
        
        if not is_solvable(grid):
            print("\nStatus: Unsolvable state detected. A* correctly identifies and skips search.\n")
            continue
            
        print(f"\n{'Heuristic Name':<30} | {'Nodes Expanded':<16} | {'Time Taken (ms)':<18} | {'Path Length':<12}")
        print("-" * 84)
        
        for h_name, h_func in HEURISTICS:
            res = a_star_search(grid, h_func)
            print(f"{h_name:<30} | {res['nodes_expanded']:<16} | {res['time_taken']:<18.4f} | {res['path_length']:<12}")
            
    print("\n" + "=" * 95)