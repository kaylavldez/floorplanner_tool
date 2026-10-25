# Floorplanner Tool

A web tool that turns room requirements into valid floorplan layouts. You describe which rooms exist and how they relate to each other, and a constraint solver searches for a layout that satisfies every rule.

[Floorplanner screenshot](preview.png)

## Why I built this

I was watching YouTube videos on how floorplans are designed because I wanted to learn. The creator used an adjacency matrix to map out which rooms should connect, and it reminded me of the constraint satisfaction problems (CSPs) I had learned in class, where the goal is to make sure every requirement is met. I wanted to see if I could apply the same idea to house floorplans.

## Features

- **Constraint solver:** Uses AC-3 arc consistency to prune impossible options, then backtracking search with the MRV (minimum remaining values) heuristic to find a layout that satisfies all constraints.
- **Interactive adjacency matrix editor:** Set which rooms should be next to each other directly in the browser.
- **Force-directed diagram (D3.js):** Explore the relationships between rooms visually instead of reading raw data.
- **REST API:** A Flask backend exposes the solver to the browser-based frontend.

## Tech stack

Python, Flask, JavaScript, HTML/CSS, D3.js

## How to run it locally

1. Clone the repo:
   ```
   git clone https://github.com/kaylavldez/floorplanner_tool.git
   cd floorplanner_tool
   ```
2. Install the dependencies:
   ```
   pip install flask
   ```
3. Start the app:
   ```
   python app.py
   ```
4. Open the address printed in the terminal (usually `http://127.0.0.1:5000`) in your browser.

## How to use it

<!-- Check these steps against how your app actually works and edit as needed. -->

1. Enter the rooms you want in your floorplan.
2. Use the adjacency matrix editor to mark which rooms must be next to each other.
3. Run the solver to generate a layout.
4. Use the diagram to inspect how the rooms connect.

## How it works

Each room is a variable, and the constraints come from your adjacency requirements. AC-3 removes placements that can't possibly work, which shrinks the search space. The backtracking search then fills in the layout one room at a time, always choosing the room with the fewest remaining options first (MRV), and backs up whenever a choice breaks a constraint.

## The bubble diagram

The diagram turns your adjacency requirements into something you can see and play with. Each room is a bubble, and the layout comes from a D3 force simulation.

- **Rooms that must be adjacent** are linked by a spring, so they pull together until their bubbles touch.
- **Rooms that must not be adjacent** are pushed apart by a custom force, so they settle at least a short distance from each other.
- **Every bubble repels the others** a little, and a collision force keeps them from overlapping, so the diagram spreads out instead of piling up.
- **Drag a bubble** to move it. The others react, and it settles back into the simulation when you let go.
- **Drag the small handle** on a bubble's edge to resize it. Sizes affect spacing, so the layout adjusts as you resize.
- **Exterior rooms** are drawn with a dashed orange outline.

### Known limitations

The diagram is still a work in progress. Bubbles can crowd together when there are many rooms, and rooms that must not touch are kept apart by force but not drawn as a line. Planned improvements include showing those rules visually and letting bubbles stay where you drop them.

## Author

Kayla Valdez, B.S. Computer Science, University of Maryland