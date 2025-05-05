import matplotlib.pyplot as plt
import numpy as np

# Base nodes and coordinates
nodes = ["A", "B", "C", "D", "E"]
spacing = 1.5
x_pos = np.arange(len(nodes)) * spacing - spacing * (len(nodes) - 1) / 2
y_base = 0
radius = 0.3

coords = {label: (x_pos[i], y_base) for i, label in enumerate(nodes)}
coords["F"] = ((coords["B"][0] + coords["C"][0]) / 2, y_base - 1.0)
coords["G"] = ((coords["C"][0] + coords["D"][0]) / 2, y_base - 1.0)
coords["H"] = ((coords["F"][0] + coords["G"][0]) / 2, y_base - 1.8)

# Bottom primes: B' and D' at same level as F; deeper for F', G', H'
coords["Bprime"] = (coords["B"][0], coords["F"][1])
coords["Dprime"] = (coords["D"][0], coords["F"][1])
coords["Fprime"] = (coords["F"][0], coords["F"][1] - 2.0)
coords["Gprime"] = (coords["G"][0], coords["G"][1] - 2.0)
coords["Hprime"] = (coords["H"][0], coords["H"][1] - 2.0)

# K between B' and F'
coords["K"] = (
    (coords["Bprime"][0] + coords["Fprime"][0]) / 2,
    (coords["Bprime"][1] + coords["Fprime"][1]) / 2,
)

# Plot setup
fig, ax = plt.subplots(figsize=(10, 6))
ax.set_aspect("equal")
ax.axis("off")
ax.set_xlim(min(x_pos) - 1, max(x_pos) + 1)
ax.set_ylim(-5, 1)


# Helper for bidirectional arrow
def bidir(a, b, color):
    x0, y0 = coords[a]
    x1, y1 = coords[b]
    dx, dy = x1 - x0, y1 - y0
    dist = np.hypot(dx, dy)
    ux, uy = dx / dist, dy / dist
    start = (x0 + ux * radius, y0 + uy * radius)
    end = (x1 - ux * radius, y1 - uy * radius)
    ax.annotate(
        "",
        xy=end,
        xytext=start,
        arrowprops=dict(arrowstyle="<->", color=color, linewidth=1.5),
    )


# Draw base list (all black)
for label in nodes:
    x, y = coords[label]
    ax.add_patch(
        plt.Circle((x, y), radius, fill=False, edgecolor="black", linewidth=1.5)
    )
    ax.text(x, y, label, ha="center", va="center", fontsize=14)
for i in range(len(nodes) - 1):
    bidir(nodes[i], nodes[i + 1], "black")

# Draw F, G, H
for label, col in [("F", "green"), ("G", "blue"), ("H", "orange")]:
    x, y = coords[label]
    ax.add_patch(plt.Circle((x, y), radius, fill=False, edgecolor=col, linewidth=1.5))
    ax.text(x, y, label, ha="center", va="center", fontsize=14, color=col)
bidir("B", "F", "green")
bidir("F", "C", "green")
bidir("C", "G", "blue")
bidir("G", "D", "blue")
bidir("F", "H", "orange")
bidir("H", "G", "orange")

# Draw deep primes and K in purple
primes = ["Bprime", "K", "Fprime", "Gprime", "Hprime", "Dprime"]
for label in primes:
    x, y = coords[label]
    ax.add_patch(
        plt.Circle((x, y), radius, fill=False, edgecolor="purple", linewidth=1.5)
    )
    text = label.replace("prime", "'") if "prime" in label else "K"
    ax.text(x, y, text, ha="center", va="center", fontsize=14, color="purple")

# Connect bottom path arrows
bidir("A", "Bprime", "purple")  # only this arrow purple
bidir("Bprime", "K", "purple")
bidir("K", "Fprime", "purple")
bidir("Fprime", "Hprime", "purple")
bidir("Hprime", "Gprime", "purple")
bidir("Gprime", "Dprime", "purple")
bidir("Dprime", "E", "black")  # back to black

plt.show()
