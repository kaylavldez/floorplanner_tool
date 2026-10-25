from flask import Flask, render_template, request, jsonify
import sys
sys.path.append('.')

from solver2 import build_domains, ac3, backtrack, add_constraint, needs_exterior
import solver2
import math

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/solve", methods=["POST"])
def solve():
    data = request.json

    # update solver state with data from browser
    solver2.rooms = data["rooms"]
    solver2.exterior_rooms = set(data["exterior_rooms"])
    
    solver2.constraints = []
    for r1, ctype, r2 in data["constraints"]:
        add_constraint(solver2.constraints, r1, ctype, r2)

    # calculate grid size
    total = len(solver2.rooms) + 4
    solver2.COLS = math.ceil(math.sqrt(total))
    solver2.ROWS = math.ceil(total / solver2.COLS)

    # run solver
    domains = build_domains()
    ac3(domains, solver2.constraints)
    solution = backtrack({}, domains)

    if solution is None:
        return jsonify({"solution": None})

    # convert solution to cell index → room name
    cell_to_room = {v: k for k, v in solution.items()}

    return jsonify({
        "solution": cell_to_room,
        "rows": solver2.ROWS,
        "cols": solver2.COLS
    })

if __name__ == "__main__":
    app.run(debug=True)