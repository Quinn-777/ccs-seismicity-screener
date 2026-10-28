"""Generate the validation scatter plot used on the app's overview page.

Run from the project folder:  python make_figure.py
Writes validation_plot.png next to this script.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Validation data: framework risk score vs observed maximum magnitude.
# Scores come from the corrected case tables; Mmax and event counts are
# the published values for each project.
CASES = [
    # name,                      score,  Mmax,  recorded events
    ("Illinois Basin-Decatur",   61.54,  1.2,   221),
    ("In Salah",                 50.00,  1.7,   9506),
    ("Basel",                    85.71,  3.4,   10500),
]

fig, ax = plt.subplots(figsize=(7, 4.5), dpi=160)

for name, score, mmax, events in CASES:
    ax.scatter(score, mmax, s=190, zorder=3,
               color="#1f5f8b", edgecolor="white", linewidth=1.8)
    ax.annotate(f"{name}\n{score:.2f}% · M{mmax}",
                xy=(score, mmax), xytext=(0, 16),
                textcoords="offset points",
                ha="center", va="bottom",
                fontsize=9, color="#2b3a42", linespacing=1.35)

ax.set_xlabel("Framework risk score (%)", fontsize=10, color="#43525c")
ax.set_ylabel("Observed maximum magnitude (Mw)", fontsize=10, color="#43525c")
ax.set_xlim(40, 97)
ax.set_ylim(0.4, 4.6)

ax.grid(True, color="#dfe5e9", linewidth=0.8, zorder=0)
ax.set_axisbelow(True)
for side in ("top", "right"):
    ax.spines[side].set_visible(False)
for side in ("left", "bottom"):
    ax.spines[side].set_color("#c6d0d6")
ax.tick_params(colors="#6b7a83", labelsize=9)

fig.tight_layout()
fig.savefig("validation_plot.png", facecolor="white", bbox_inches="tight")
print("Wrote validation_plot.png")
