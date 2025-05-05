import matplotlib.pyplot as plt
import numpy as np

# Coordinates for original nodes
coords = {
    "root": (0, 0),
    "left": (-1, -1),
    "right": (1, -1),
    "leaf1": (-1.5, -2),
    "leaf2": (-0.5, -2),
    "leaf3": (0.5, -2),
    "leaf4": (1.5, -2),
}

# Original sums
orig_values = {
    "root": 10,
    "left": 3,
    "right": 7,
    "leaf1": 1,
    "leaf2": 2,
    "leaf3": 3,
    "leaf4": 4,
}

# Updated path values
new_values = {
    "root": 6,
    "right": 3,
    "leaf4": 0,
}

# Larger horizontal offset for updated nodes
offset_x = 0.8
radius = 0.3

fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect("equal")
ax.axis("off")
ax.set_xlim(-2, 3)
ax.set_ylim(-3, 1.5)

# Draw original black tree
for node, (x, y) in coords.items():
    circle = plt.Circle((x, y), radius, fill=False, linewidth=1.5)
    ax.add_patch(circle)
for start, end in [
    ("root", "left"),
    ("root", "right"),
    ("left", "leaf1"),
    ("left", "leaf2"),
    ("right", "leaf3"),
    ("right", "leaf4"),
]:
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
for node, (x, y) in coords.items():
    ax.text(x, y, str(orig_values[node]), ha="center", va="center", fontsize=12)

# Add labels above roots
x0, y0 = coords["root"]
ax.text(x0, y0 + radius + 0.1, "$V_0$", ha="center", va="bottom", fontsize=14)
ax.text(
    x0 + offset_x,
    y0 + radius + 0.1,
    "$V_1$",
    ha="center",
    va="bottom",
    fontsize=14,
    color="green",
)

# Draw new green nodes at same y-level and shifted right
for node, val in new_values.items():
    x, y = coords[node]
    x_new = x + offset_x
    circle = plt.Circle(
        (x_new, y), radius, fill=False, linewidth=1.5, edgecolor="green"
    )
    ax.add_patch(circle)
    ax.text(x_new, y, str(val), ha="center", va="center", fontsize=12, color="green")

# Draw green arrows from updated nodes to both children
green_connections = [
    ("root", "left"),
    ("root", "right"),
    ("right", "leaf3"),
    ("right", "leaf4"),
]
for parent, child in green_connections:
    x0, y0 = coords[parent]
    x1, y1 = coords[child]
    # apply offset to start; offset to end only if child updated
    x0 += offset_x
    if child in new_values:
        x1 += offset_x
    dx, dy = x1 - x0, y1 - y0
    dist = np.hypot(dx, dy)
    ux, uy = dx / dist, dy / dist
    start_pt = (x0 + ux * radius, y0 + uy * radius)
    end_pt = (x1 - ux * radius, y1 - uy * radius)
    ax.annotate(
        "",
        xy=end_pt,
        xytext=start_pt,
        arrowprops=dict(arrowstyle="->", color="green", linewidth=1.5),
    )

plt.show()
