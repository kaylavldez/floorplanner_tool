from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from solver import make_grid, build_domains, backtrack
 
app = Flask(__name__)
CORS(app)
 
@app.route("/")
def serve_frontend():
    return send_from_directory(".", "floorplan.html")
 
@app.route("/solve", methods=["POST"])
def solve():
    data = request.get_json()
    room_data = data.get("rooms", [])
    constraints = [
        (c["room1"], c["type"], c["room2"])
        for c in data.get("constraints", [])
    ]
 
    room_names_set = {r["name"] for r in room_data}
    for room1, ctype, room2 in constraints:
        if room1 not in room_names_set or room2 not in room_names_set:
            return jsonify({"error": f"Constraint references unknown room: '{room1}' or '{room2}'"}), 400
 
    ROWS, COLS = make_grid(len(room_data))
    domains = build_domains(room_data, ROWS, COLS)
    room_names = [r["name"] for r in room_data]
 
    result = backtrack({}, domains, room_names, constraints, ROWS, COLS)
 
    if result is None:
        return jsonify({"error": "No solution found — constraints may be unsatisfiable for this grid size."}), 400
 
    # Build solution as { room_name: { row, col, cell } }
    solution = {}
    for room_name, cell in result.items():
        row, col = divmod(cell, COLS)
        solution[room_name] = {"row": row, "col": col, "cell": cell}
 
    nodes = [
        {"id": room["name"], "exterior": room["exterior"]}
        for room in room_data
    ]
    links = [
        {"source": room1, "target": room2, "type": ctype}
        for room1, ctype, room2 in constraints
        if ctype != "neutral"
    ]
 
    return jsonify({
        "nodes": nodes,
        "links": links,
        "solution": solution,
        "grid": {"rows": ROWS, "cols": COLS}
    })
 
if __name__ == "__main__":
    app.run(debug=True)