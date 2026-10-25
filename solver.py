# VERSION 3: Matrix + Bubble (5/28/26)
import random, math
from collections import deque

def make_grid(num_rooms):
    size = math.ceil(math.sqrt(num_rooms))
    size = max(size, 2)
    return size, size # ROWS, COLS

def get_neighbors(cell, ROWS, COLS):
    row, col = divmod(cell, COLS)
    neighbors = [] # [above, below, left, right]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # (row_offset, col_offset)
    
    for row_offset, col_offset in directions:
        new_row = row + row_offset
        new_col = col + col_offset
        if 0 <= new_row < ROWS and 0 <= new_col < COLS:
            neighbors.append(new_row * COLS + new_col)
    
    return neighbors

def is_edge_cell(cell, ROWS, COLS):       
    return len(get_neighbors(cell, ROWS, COLS)) < 4

def build_domains(room_data, ROWS, COLS):
    all_cells = set(range(ROWS * COLS))
    edge_cells = {cell for cell in all_cells if is_edge_cell(cell, ROWS, COLS)}
    domains = {}
    
    for room in room_data:
        if room["exterior"]:
            domains[room["name"]] = edge_cells.copy()
        else: 
            domains[room["name"]] = all_cells.copy()
            
    return domains

def revise(domains, room1, room2, ctype, ROWS, COLS):
    to_remove = set()

    for cell in domains[room1]:
        neighbors = get_neighbors(cell, ROWS, COLS)

        if ctype == "must":
            valid = any(n in domains[room2] for n in neighbors)
        elif ctype == "must_not":
            valid = any(c not in neighbors for c in domains[room2])
        else:
            valid = True # neutral — no restriction

        if not valid:
            to_remove.add(cell)

    domains[room1] -= to_remove
    return len(to_remove) > 0


def ac3(domains, constraints, ROWS, COLS):
    queue = deque()
    for room1, ctype, room2 in constraints:
        if ctype == "neutral":
            continue
        queue.append((room1, room2, ctype))
        queue.append((room2, room1, ctype))

    while queue:
        room1, room2, ctype = queue.popleft()
        if revise(domains, room1, room2, ctype, ROWS, COLS):
            if not domains[room1]:
                return False
            for r1, ct, r2 in constraints:
                if ct == "neutral":
                    continue
                if r2 == room1 and r1 != room2:
                    queue.append((r1, room1, ct))
                if r1 == room1 and r2 != room2:
                    queue.append((r2, room1, ct))

    return True

def backtrack(assignment, domains, room_names, constraints, ROWS, COLS):
    if len(assignment) == len(room_names):
        return assignment

    # pick the unassigned room with the smallest domain (MRV heuristic)
    unassigned = [r for r in room_names if r not in assignment]
    room = min(unassigned, key=lambda r: len(domains[r]))

    cell_list = list(domains[room])
    random.shuffle(cell_list)

    for cell in cell_list:
        if cell in assignment.values():
            continue

        saved_domains = {r: d.copy() for r, d in domains.items()}
        assignment[room] = cell
        domains[room] = {cell}

        if ac3(domains, constraints, ROWS, COLS):
            result = backtrack(assignment, domains, room_names, constraints, ROWS, COLS)
            if result is not None:
                return result

        del assignment[room]
        domains.update(saved_domains)

    return None