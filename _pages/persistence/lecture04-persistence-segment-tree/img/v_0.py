import matplotlib.pyplot as plt
import numpy as np

# Coordinates for nodes
coords = {
    "root": (0, 0),
    "left": (-1, -1),
    "right": (1, -1),
    "leaf1": (-1.5, -2),
    "leaf2": (-0.5, -2),
    "leaf3": (0.5, -2),
    "leaf4": (1.5, -2),
}

# Sum values for each node
values = {
    "root": 10,
    "left": 3,
    "right": 7,
    "leaf1": 1,
    "leaf2": 2,
    "leaf3": 3,
    "leaf4": 4,
}

# Edges to draw
edges = [
    ("root", "left"),
    ("root", "right"),
    ("left", "leaf1"),
    ("left", "leaf2"),
    ("right", "leaf3"),
    ("right", "leaf4"),
]

radius = 0.3

fig, ax = plt.subplots()
ax.set_aspect("equal")
ax.axis("off")
ax.set_xlim(-2, 2)
ax.set_ylim(-3, 1)

# Draw circles
for node, (x, y) in coords.items():
    circle = plt.Circle((x, y), radius, fill=False, linewidth=1.5)
    ax.add_patch(circle)

# Draw arrows between borders
for start, end in edges:
    x0, y0 = coords[start]
    x1, y1 = coords[end]
    dx, dy = x1 - x0, y1 - y0
    dist = np.hypot(dx, dy)
    ux, uy = dx / dist, dy / dist
    start_pt = (x0 + ux * radius, y0 + uy * radius)
    end_pt = (x1 - ux * radius, y1 - uy * radius)
    ax.annotate(
        "",
        xy=end_pt,
        xytext=start_pt,
        arrowprops=dict(arrowstyle="->", color="black", linewidth=1.5),
    )

# Add labels
for node, (x, y) in coords.items():
    ax.text(x, y, str(values[node]), ha="center", va="center", fontsize=12)

plt.show()
