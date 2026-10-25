# I was watching YouTube videos of how to make floorplans because I wanted to learn.
# The YouTuber I watched used an adjacency matrix, and it reminded me of when I
# learned to do CSP, making sure requirements were met. I felt inspired to do the same
# with house floorplans.

# VERSION 1 (5/27/26)
import random

# 1. rooms list
rooms = ["mudroom", 
         "living room",
         "powder room",
         "bathroom", 
         "kitchen", 
         "dining room", 
         "utility room", 
         "bedroom1",
         "bedroom2", 
         "master bedroom", 
         "master bathroom", 
         "garage"]

exterior_rooms = set()

def needs_exterior(room):
    exterior_rooms.add(room)

# 2. grid size
ROWS = 4
COLS = 4

# 3. constraints
constraints = [('master bedroom', 'must', 'master bathroom')]

# 4. build_domains()
def build_domains():
    all_cells = set(range(ROWS * COLS))
    edge_cells = {i for i in all_cells if is_edge_cell(i)}
    domains = {}
    
    for room in rooms:
        if room in exterior_rooms:
            domains[room] = edge_cells.copy()
        else: 
            domains[room] = all_cells.copy()
            
    return domains

# 5. get_neighbors()
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

# 6. is_edge_cell()
def is_edge_cell(i):       
    return len(get_neighbors(i)) < 4

# 7. add_constraint()
def add_constraint(constraints, room1, ctype, room2):
    constraints.append((room1, ctype, room2))
    
def get_user_constraints(constraints):
    print("\nAdd your own constraints.")
    print("Rooms:", rooms)
    print("Types: must, must_not")
    print("Type 'done' when finished.\n")
    
    while True:
        room1 = input("Room 1: ").strip()
        if room1 == "done":
            break
        if room1 not in rooms:
            print("Unknown room, try again.")
            continue
            
        ctype = input("Type (must/must_not): ").strip()
        if ctype not in ("must", "must_not"):
            print("Must be 'must' or 'must_not', try again.")
            continue
            
        room2 = input("Room 2: ").strip()
        if room2 not in rooms:
            print("Unknown room, try again.")
            continue
            
        add_constraint(constraints, room1, ctype, room2)
        print(f"Added: {room1} {ctype} {room2}\n")

def get_exterior_rooms():
    print("\nWhich rooms need exterior access?")
    print("Rooms:", rooms)
    print("Type 'done' when finished.\n")
    
    while True:
        room = input("Room: ").strip()
        if room == "done":
            break
        if room not in rooms:
            print("Unknown room, try again.")
            continue
        needs_exterior(room)
        print(f"{room} marked as exterior.\n")
        
# 8. AC-3 solver
def build_queue(constraints):
    queue = []
    
    for room1, ctype, room2 in constraints:
        queue.append((room1, room2, ctype))
        queue.append((room2, room1, ctype))
        
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

# 9. Backtracking search
def backtrack(assignment, domains):
    if len(assignment) == len(rooms):
        return assignment
    
    unassigned = [r for r in rooms if r not in assignment]
    room = unassigned[0]
    
    cell_list = list(domains[room])
    random.shuffle(cell_list)
    
    for cell in cell_list:
        if cell in assignment.values():
            continue
        saved_domains = {r: d.copy() for r, d in domains.items()}
        assignment[room] = cell
        domains[room] = {cell}
        
        if ac3(domains, constraints):
            result = backtrack(assignment, domains)
            
            if result is not None:
                return result
            
        del assignment[room]
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