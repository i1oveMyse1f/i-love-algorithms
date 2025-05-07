import matplotlib.pyplot as plt
import matplotlib.patches as patches

# High-resolution figure
fig, ax = plt.subplots(figsize=(8, 13), dpi=300)
ax.axis("off")

# Box dimensions and vertical gaps
box_w, box_h = 1.0, 0.8
gap_input = 0.3
gap_pass0 = 0.2
gap_pass1 = 0.5
gap_pass2 = 0.5

# Compute Y levels (bottom of each pass)
y_pass2 = gap_pass2
y_pass1 = y_pass2 + 4 * box_h + gap_pass1  # enough height for up to 4 chunks
y_pass0 = y_pass1 + 4 * box_h + gap_pass0
y_input = y_pass0 + box_h + gap_input

y_levels = {"input": y_input, "pass0": y_pass0, "pass1": y_pass1, "pass2": y_pass2}

# Input runs (pairs or single numbers)
inputs = ["3,4", "6,2", "9,4", "8,7", "5,6", "3,1", "2"]

# Ensure view area
total_width = len(inputs) * (box_w + gap_pass0)
ax.set_xlim(0, total_width + 0.5)
ax.set_ylim(0, y_input + box_h + gap_input)


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
    return (x, y, w, h)


def draw_arrow(src, tgt):
    x1, y1, w1, h1 = src
    x2, y2, w2, h2 = tgt
    start = (x1 + w1 / 2, y1)  # bottom-center of src
    end = (x2 + w2 / 2, y2 + h2)  # top-center of tgt
    ax.annotate("", xy=end, xytext=start, arrowprops=dict(arrowstyle="-|>", lw=2))


def flatten_numbers(run_txts):
    nums = []
    for t in run_txts:
        if "," in t:
            a, b = t.split(",")
            nums.extend([int(a), int(b)])
        else:
            nums.append(int(t))
    return sorted(nums)


# 1) INPUT (orange) and PASS0 (white), with arrows
input_boxes = []
pass0_boxes = []
for i, txt in enumerate(inputs):
    x = 0.5 + i * (box_w + gap_pass0)
    ib = draw_box(x, y_levels["input"], box_w, box_h, txt, facecolor="#f7c873")
    pb = draw_box(x, y_levels["pass0"], box_w, box_h, txt)
    input_boxes.append(ib)
    pass0_boxes.append(pb)
    draw_arrow(ib, pb)

# 2) PASS1: merge groups of 4 page-runs -> segments into chunks of 4 numbers
pass1_indices = [list(range(0, 4)), list(range(4, len(pass0_boxes)))]
pass1_run_chunks = []  # store lists of chunk-boxes for each run

for indices in pass1_indices:
    run_txts = [inputs[i] for i in indices]
    nums = flatten_numbers(run_txts)
    chunks = [nums[i : i + 4] for i in range(0, len(nums), 4)]
    # compute x position for this run
    xs = [pass0_boxes[i][0] for i in indices]
    x = sum(xs) / len(xs)
    # draw chunk boxes vertically (top-down)
    boxes = []
    for j, chunk in enumerate(chunks):
        txt = ",".join(str(n) for n in chunk)
        y = y_levels["pass1"] + (len(chunks) - j - 1) * box_h
        b = draw_box(x, y, box_w, box_h, txt)
        boxes.append(b)
    # arrows from each pass0 to top chunk
    for i in indices:
        draw_arrow(pass0_boxes[i], boxes[0])
    pass1_run_chunks.append(boxes)

# 3) PASS2: final merge of all runs, grouped into chunks of 4 numbers
all_nums = flatten_numbers(inputs)
final_chunks = [all_nums[i : i + 4] for i in range(0, len(all_nums), 4)]
# compute final x
run_xs = [boxes[0][0] for boxes in pass1_run_chunks]
x_final = sum(run_xs) / len(run_xs)

final_boxes = []
for j, chunk in enumerate(final_chunks):
    txt = ",".join(str(n) for n in chunk)
    y = y_levels["pass2"] + (len(final_chunks) - j - 1) * box_h
    b = draw_box(x_final, y, box_w, box_h, txt)
    final_boxes.append(b)

# arrows from bottom chunk of each pass1 run to top final chunk
for boxes in pass1_run_chunks:
    draw_arrow(boxes[-1], final_boxes[0])

plt.tight_layout()
plt.show()
