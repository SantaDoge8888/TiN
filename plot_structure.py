
from ase.io import read
from ase.visualize.plot import plot_atoms
import matplotlib.pyplot as plt

# Read the relaxed geometry used in the final SCF calculation
atoms = read(
    "02_tin111_scf.in",
    format="espresso-in"
)


# ============================================================
# SIDE VIEW
# ============================================================

fig, ax = plt.subplots(figsize=(9, 6))

plot_atoms(
    atoms,
    ax,
    rotation="90x,0y,0z",
    radii=0.7
)

ax.set_title(
    "Relaxed Ti-terminated TiN(111) slab — side view"
)

fig.tight_layout()

fig.savefig(
    "results/figures/tin111_slab_side.png",
    dpi=300,
    bbox_inches="tight"
)

fig.savefig(
    "results/figures/tin111_slab_side.pdf",
    bbox_inches="tight"
)

plt.close(fig)

# ============================================================
# TOP VIEW
# ============================================================

fig, ax = plt.subplots(figsize=(7, 7))

plot_atoms(
    atoms,
    ax,
    rotation="0x,0y,0z",
    radii=0.7
)

ax.set_title(
    "TiN(111) surface — top view"
)

fig.tight_layout()

fig.savefig(
    "results/figures/tin111_slab_top.png",
    dpi=300,
    bbox_inches="tight"
)

fig.savefig(
    "results/figures/tin111_slab_top.pdf",
    bbox_inches="tight"
)

plt.close(fig)

print("Created:")
print("results/figures/tin111_slab_side.png")
print("results/figures/tin111_slab_side.pdf")
print("results/figures/tin111_slab_top.png")
print("results/figures/tin111_slab_top.pdf")
