import matplotlib.pyplot as plt
import numpy as np

# Base nodes and coordinates
base_nodes = ["A", "B", "C", "D", "E"]
n = len(base_nodes)
spacing = 1.5
x_positions = np.arange(n) * spacing - spacing * (n - 1) / 2
y_base = 0
radius = 0.3

# Coordinate mapping for original nodes
coords = {label: (x_positions[i], y_base) for i, label in enumerate(base_nodes)}

# Compute inserted vertices F (green) and G (blue)
coords["F"] = ((coords["B"][0] + coords["C"][0]) / 2, y_base - 1.0)
coords["G"] = ((coords["C"][0] + coords["D"][0]) / 2, y_base - 1.0)

# Compute H (orange) at a lower layer
coords["H"] = ((coords["F"][0] + coords["G"][0]) / 2, y_base - 1.8)

# Plot setup
fig, ax = plt.subplots(figsize=(10, 5))
ax.set_aspect("equal")
ax.axis("off")
ax.set_xlim(x_positions.min() - 1, x_positions.max() + 1)
ax.set_ylim(-2.5, 1)

# Draw black base list A<->B<->C<->D<->E
for label in base_nodes:
    x, y = coords[label]
    circle = plt.Circle((x, y), radius, fill=False, linewidth=1.5, edgecolor="black")
    ax.add_patch(circle)
    ax.text(x, y, label, ha="center", va="center", fontsize=14, color="black")
for i in range(n - 1):
    x0, y0 = coords[base_nodes[i]]
    x1, y1 = coords[base_nodes[i + 1]]
    dx, dy = x1 - x0, y1 - y0
    dist = np.hypot(dx, dy)
    ux, uy = dx / dist, dy / dist
    ax.annotate(
        "",
        xy=(x1 - ux * radius, y1 - uy * radius),
        xytext=(x0 + ux * radius, y0 + uy * radius),
        arrowprops=dict(arrowstyle="<->", color="black", linewidth=1.5),
    )

# Draw green F
xF, yF = coords["F"]
ax.add_patch(plt.Circle((xF, yF), radius, fill=False, linewidth=1.5, edgecolor="green"))
ax.text(xF, yF, "F", ha="center", va="center", fontsize=14, color="green")
for pair in [("B", "F"), ("F", "C")]:
    x0, y0 = coords[pair[0]]
    x1, y1 = coords[pair[1]]
    dx, dy = x1 - x0, y1 - y0
    dist = np.hypot(dx, dy)
    ux, uy = dx / dist, dy / dist
    ax.annotate(
        "",
        xy=(x1 - ux * radius, y1 - uy * radius),
        xytext=(x0 + ux * radius, y0 + uy * radius),
        arrowprops=dict(arrowstyle="<->", color="green", linewidth=1.5),
    )

# Draw blue G
xG, yG = coords["G"]
ax.add_patch(plt.Circle((xG, yG), radius, fill=False, linewidth=1.5, edgecolor="blue"))
ax.text(xG, yG, "G", ha="center", va="center", fontsize=14, color="blue")
for pair in [("C", "G"), ("G", "D")]:
    x0, y0 = coords[pair[0]]
    x1, y1 = coords[pair[1]]
    dx, dy = x1 - x0, y1 - y0
    dist = np.hypot(dx, dy)
    ux, uy = dx / dist, dy / dist
    ax.annotate(
        "",
        xy=(x1 - ux * radius, y1 - uy * radius),
        xytext=(x0 + ux * radius, y0 + uy * radius),
        arrowprops=dict(arrowstyle="<->", color="blue", linewidth=1.5),
    )

# Draw orange H at lower layer between F and G
xH, yH = coords["H"]
ax.add_patch(
    plt.Circle((xH, yH), radius, fill=False, linewidth=1.5, edgecolor="orange")
)
ax.text(xH, yH, "H", ha="center", va="center", fontsize=14, color="orange")
for pair in [("F", "H"), ("H", "G")]:
    x0, y0 = coords[pair[0]]
    x1, y1 = coords[pair[1]]
    dx, dy = x1 - x0, y1 - y0
    dist = np.hypot(dx, dy)
    ux, uy = dx / dist, dy / dist
    ax.annotate(
        "",
        xy=(x1 - ux * radius, y1 - uy * radius),
        xytext=(x0 + ux * radius, y0 + uy * radius),
        arrowprops=dict(arrowstyle="<->", color="orange", linewidth=1.5),
    )

plt.show()
