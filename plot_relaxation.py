

import re
import matplotlib.pyplot as plt

# Read the entire structural-relaxation output
with open("outputs/01_tin111_relax.out") as f:
    text = f.read()

# Extract every Total force value printed by QE
forces = [
    float(x)
    for x in re.findall(
        r"Total force\s*=\s*([-+]?\d*\.?\d+(?:[Ee][-+]?\d+)?)",
        text
    )
]

steps = list(range(1, len(forces) + 1))

if not forces:
    raise RuntimeError(
        "No Total force values found in relaxation output."
    )

fig, ax = plt.subplots(figsize=(7, 5))

ax.plot(
    steps,
    forces,
    marker="o"
)

ax.axhline(
    1.0e-3,
    linestyle="--",
    label=r"$10^{-3}$ Ry/Bohr reference"
)
ax.set_yscale("log")

ax.set_xlabel(
    "Ionic relaxation step"
)

ax.set_ylabel(
    "Total force (Ry/Bohr)"
)

ax.set_title(
    "TiN(111) surface relaxation"
)

ax.legend(frameon=False)
ax.grid(alpha=0.2)

fig.tight_layout()

fig.savefig(
    "results/figures/tin111_relaxation.png",
    dpi=300,
    bbox_inches="tight"
)

fig.savefig(
    "results/figures/tin111_relaxation.pdf",
    bbox_inches="tight"
)

plt.close(fig)

print(
    f"Ionic steps found: {len(forces)}"
)

print(
    f"Final total force: {forces[-1]} Ry/Bohr"
)

print("Created:")
print("results/figures/tin111_relaxation.png")
print("results/figures/tin111_relaxation.pdf")

