import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Figure setup with high DPI
fig, ax = plt.subplots(figsize=(8, 12), dpi=300)
ax.axis("off")

# Box dimensions and vertical gaps
box_w, box_h = 1.0, 0.8
gap_input = 0.3  # space above pass0 to input
gap_pass0 = 0.2  # between pass0/pass1 & horizontal spacing
gap_pass1 = 0.2  # between pass1/pass2
gap_pass2 = 0.1  # bottom margin

# Compute y-levels (bottom coordinates)
y_pass2 = gap_pass2  # final run
h_pass2 = 7 * box_h  # 7 lines for final
y_pass1 = y_pass2 + h_pass2 + gap_pass1  # pass1 band
h_pass1 = max(4, 3) * box_h  # max height of pass1 runs
y_pass0 = y_pass1 + h_pass1 + gap_pass0  # pass0 band
h_pass0 = box_h  # 1-page runs
y_input = y_pass0 + h_pass0 + gap_input  # input row

y_levels = {
    "pass2": y_pass2,
    "pass1": y_pass1,
    "pass0": y_pass0,
    "input": y_input,
}

# Input data (sorted within each page)
inputs = ["3,4", "6,2", "9,4", "8,7", "5,6", "3,1", "2"]

# Ensure full layout visible
total_width = len(inputs) * (box_w + gap_pass0)
top = y_levels["input"] + box_h + 0.1
ax.set_xlim(0, total_width + 0.5)
ax.set_ylim(0, top)


def draw_box(x, y, w, h, text, facecolor="white"):
    rect = patches.Rectangle(
        (x, y), w, h, linewidth=2, edgecolor="black", facecolor=facecolor
    )
    ax.add_patch(rect)
    lines = text.split("\n")
    for i, line in enumerate(lines):
        ax.text(
            x + w / 2,
            y + h - (i + 0.5) * (h / len(lines)),
            line,
            ha="center",
            va="center",
            fontsize=10,
        )
    if len(lines) > 1:
        # horizontal splits
        for j in range(1, len(lines)):
            y_split = y + j * (h / len(lines))
            ax.hlines(y_split, x, x + w, linewidth=2, color="black")
    return (x, y, w, h)


def draw_arrow(src, tgt):
    x1, y1, w1, h1 = src
    x2, y2, w2, h2 = tgt
    start = (x1 + w1 / 2, y1)
    end = (x2 + w2 / 2, y2 + h2)
    ax.annotate("", xy=end, xytext=start, arrowprops=dict(arrowstyle="-|>", lw=2))


# 1) Input page-runs (orange)
input_boxes = []
for i, txt in enumerate(inputs):
    x = 0.5 + i * (box_w + gap_pass0)
    b = draw_box(x, y_levels["input"], box_w, box_h, txt, facecolor="#f7c873")
    input_boxes.append(b)

# 2) PASS0: 1-page runs (white)
pass0_boxes = []
for i, txt in enumerate(inputs):
    x = 0.5 + i * (box_w + gap_pass0)
    b = draw_box(x, y_levels["pass0"], box_w, box_h, txt)
    pass0_boxes.append(b)

# Arrows: Input -> PASS0
for src, tgt in zip(input_boxes, pass0_boxes):
    draw_arrow(src, tgt)

# 3) PASS1: 4-way merge into runs of ≤4 pages
pass1_texts = [
    "2,3\n4,4\n6,7\n8,9",  # merged first 4 inputs
    "1,2\n3,5\n6",
]  # merged last 3 inputs
pass1_boxes = []
for i, txt in enumerate(pass1_texts):
    lines = txt.count("\n") + 1
    h = box_h * lines
    idx_start = 4 * i
    idx_end = min(idx_start + 4, len(pass0_boxes))
    xs = [pass0_boxes[j][0] for j in range(idx_start, idx_end)]
    x = sum(xs) / len(xs)
    b = draw_box(x, y_levels["pass1"], box_w, h, txt)
    pass1_boxes.append(b)
    # arrows from PASS0 -> PASS1
    for j in range(idx_start, idx_end):
        draw_arrow(pass0_boxes[j], b)

# 4) PASS2: final <=4-way merge
final_txt = "1,2\n2,3\n3,4\n4,5\n6,6\n7,8\n9"
h_final = box_h * (final_txt.count("\n") + 1)
x_final = sum(b[0] for b in pass1_boxes) / len(pass1_boxes)
final_box = draw_box(x_final, y_levels["pass2"], box_w, h_final, final_txt)

# Arrows: PASS1 -> PASS2
for b in pass1_boxes:
    draw_arrow(b, final_box)

plt.tight_layout()
plt.show()
