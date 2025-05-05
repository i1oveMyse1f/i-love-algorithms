import matplotlib.pyplot as plt
import numpy as np

# Node labels and coordinates for 5-element doubly linked list
nodes = ["A", "B", "C", "D", "E"]
n = len(nodes)
spacing = 1.5
x_positions = np.arange(n) * spacing - spacing * (n - 1) / 2
y_pos = 0
radius = 0.3

# Create coordinate mapping
coords = {label: (x_positions[i], y_pos) for i, label in enumerate(nodes)}

# Plot setup
fig, ax = plt.subplots(figsize=(10, 4))
ax.set_aspect("equal")
ax.axis("off")
ax.set_xlim(x_positions.min() - 1, x_positions.max() + 1)
ax.set_ylim(-1, 1)

# Draw circles and labels
for label, (x, y) in coords.items():
    circle = plt.Circle((x, y), radius, fill=False, linewidth=1.5, edgecolor="black")
    ax.add_patch(circle)
    ax.text(x, y, label, ha="center", va="center", fontsize=14, color="black")

# Draw bidirectional arrows between adjacent nodes
for i in range(n - 1):
    start_label = nodes[i]
    end_label = nodes[i + 1]
    x0, y0 = coords[start_label]
    x1, y1 = coords[end_label]
    # Compute boundary points
    dx, dy = x1 - x0, y1 - y0
    dist = np.hypot(dx, dy)
    ux, uy = dx / dist, dy / dist
    start_pt = (x0 + ux * radius, y0 + uy * radius)
    end_pt = (x1 - ux * radius, y1 - uy * radius)
    ax.annotate(
        "",
        xy=end_pt,
        xytext=start_pt,
        arrowprops=dict(arrowstyle="<->", color="black", linewidth=1.5),
    )

plt.show()
