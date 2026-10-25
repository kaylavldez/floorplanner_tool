# VERSION 2 (5/28/26)
import random, math

ROWS = 4
COLS = 4

rooms = []
constraints = []

# {"name": "bedroom 1", "type": "bedroom", "size": "large"}
def add_room(room_type, size, count):
    for i in range(1, count + 1):
        name = room_type if count == 1 else f"{room_type} {i}"
        rooms.append({
            "name": name,
            "type": room_type,
            "size": size
        })

exterior_rooms = set()

def matches(room, target):
    # target can be:
    # "bedroom:large"  → match by type and size
    # "bedroom 1"      → match by exact name
    # "bedroom"        → match by type
   
    if ":" in target:
        t, s = target.split(":")
        return room["type"] == t and room["size"] == s
    elif target in [r["name"] for r in rooms]:
        return room["name"] == target
    else:
        return room["type"] == target

def needs_exterior(room_name):
    exterior_rooms.add(room_name)

def get_neighbors(i):
    neighbors = [] # [above, below, left, right]
    i_row = i // COLS
    i_col = i % COLS
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)] # (row_offset, col_offset)
    
    for row_offset, col_offset in directions:
        new_row = i_row + row_offset
        new_col = i_col + col_offset
        if 0 <= new_row < ROWS and 0 <= new_col < COLS:
            neighbors.append(new_row * COLS + new_col)
    
    return neighbors

def is_edge_cell(i):       
    return len(get_neighbors(i)) < 4

def build_domains():
    all_cells = set(range(ROWS * COLS))
    edge_cells = {i for i in all_cells if is_edge_cell(i)}
    domains = {}
    
    for room in rooms:
        name = room["name"]
        if name in exterior_rooms:
            domains[name] = edge_cells.copy()
        else: 
            domains[name] = all_cells.copy()
            
    return domains

def add_constraint(constraints, room1, ctype, room2):
    constraints.append((room1, ctype, room2))

def expand_constraint(room1_target, ctype, room2_target):
    pairs = []
    for r1 in rooms:
        for r2 in rooms:
            if r1["name"] == r2["name"]:
                continue
            if matches(r1, room1_target) and matches(r2, room2_target):
                pairs.append((r1["name"], ctype, r2["name"]))
                
    return pairs
        
def build_queue(constraints):
    queue = []
    
    for room1, ctype, room2 in constraints:
        pairs = expand_constraint(room1, ctype, room2)
        for r1, ct, r2 in pairs:
            queue.append((r1, r2, ct))
            queue.append((r2, r1, ct))
        
    return queue

def revise(domains, room1, room2, ctype):
    to_remove = set()
    
    for cell in domains[room1]:
        neighbors = get_neighbors(cell)
        
        if ctype == "must":
            valid = any(n in domains[room2] for n in neighbors)
        elif ctype == "must_not":
            valid = any(n not in domains[room2] for n in neighbors) 
        
        if not valid:
           to_remove.add(cell)      
    
    domains[room1] -= to_remove
    
    return len(to_remove) > 0

def ac3(domains, constraints):
    queue = build_queue(constraints)
    
    while queue:
        room1, room2, ctype = queue.pop(0)
        if revise(domains, room1, room2, ctype):
            if not domains[room1]:
                return False
            for arc in build_queue(constraints):
                if arc not in queue:
                    queue.append(arc)
                    
    return True

def backtrack(assignment, domains):
    if len(assignment) == len(rooms):
        return assignment
    
    unassigned = [r for r in rooms if r["name"] not in assignment]
    room = unassigned[0]
    room_name = room["name"]
    
    cell_list = list(domains[room_name])
    random.shuffle(cell_list)
    
    for cell in cell_list:
        if cell in assignment.values():
            continue
        saved_domains = {key: d.copy() for key, d in domains.items()}
        assignment[room_name] = cell
        domains[room_name] = {cell}
        
        if ac3(domains, constraints):
            result = backtrack(assignment, domains)
            
            if result is not None:
                return result
            
        del assignment[room_name]
        domains.update(saved_domains)
        
    return None

#########################################################################
        
# get_exterior_rooms()
# get_user_constraints(constraints)
domains = build_domains()
ac3(domains, constraints)
solution = backtrack({}, domains)

# if solution:
#     for room, cell in solution.items():
#         row = cell // COLS
#         col = cell % COLS
#         print(f"{room}: cell {cell} (row {row}, col {col})")
# else:
#     print("No solution found.")

