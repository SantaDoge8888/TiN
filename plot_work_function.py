import numpy as np
import matplotlib.pyplot as plt
import re

BOHR_TO_ANG = 0.529177210903
RY_TO_EV = 13.605693122994

# ------------------------------------------------------------
# Read average.x output
#
# Column 1 = z in Bohr
# Column 2 = planar-averaged potential in Ry
# Column 3 = macroscopic-averaged potential in Ry
# ------------------------------------------------------------

data = np.loadtxt("outputs/tin111.avg.dat")

z = data[:, 0] * BOHR_TO_ANG
planar = data[:, 1] * RY_TO_EV
macro = data[:, 2] * RY_TO_EV


# ------------------------------------------------------------
# Extract the Fermi energy from the final SCF calculation
# ------------------------------------------------------------

with open("outputs/02_tin111_scf.out") as f:
    scf_text = f.read()

matches = re.findall(
    r"the Fermi energy is\s+([-+]?\d*\.?\d+)\s+ev",
    scf_text,
    flags=re.IGNORECASE,
)

if not matches:
    raise RuntimeError("Could not find Fermi energy")

EF = float(matches[-1])

# ------------------------------------------------------------
# Read the already-calculated work-function quantities
# ------------------------------------------------------------

with open("outputs/work_function.txt") as f:
    wf_text = f.read()


def get_value(label):
    match = re.search(
        rf"{label}\s*=\s*([-+]?\d*\.?\d+)",
        wf_text
    )

    if not match:
        raise RuntimeError(f"Could not find {label}")

    return float(match.group(1))


VLEFT = get_value("Left vacuum level")
VRIGHT = get_value("Right vacuum level")
VVAC = get_value("Mean vacuum level")
WF = get_value("WORK FUNCTION")

# ------------------------------------------------------------
# Make figure
# ------------------------------------------------------------

fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(
    z,
    planar,
    linewidth=0.8,
    label="Planar-averaged potential"
)

ax.plot(
    z,
    macro,
    linewidth=2.0,
    label="Macroscopic-averaged potential"
)

ax.axhline(
    VVAC,
    linestyle="--",
    linewidth=1.4,
    label=fr"$V_{{vac}}$ = {VVAC:.3f} eV"
)

ax.axhline(
    EF,
    linestyle=":",
    linewidth=1.5,
    label=fr"$E_F$ = {EF:.3f} eV"
)

# Approximate region occupied by the TiN slab
ax.axvspan(
    10.0,
    32.0525,
    alpha=0.10,
    label="TiN slab"
)



# Draw an arrow showing the work function
x_arrow = z.max() * 0.89

ax.annotate(
    "",
    xy=(x_arrow, VVAC),
    xytext=(x_arrow, EF),
    arrowprops=dict(
        arrowstyle="<->",
        linewidth=1.5
    )
)

ax.text(
    x_arrow + 0.6,
    (VVAC + EF) / 2,
    fr"$\Phi$ = {WF:.3f} eV",
    va="center"
)

ax.set_xlabel(r"$z$ ($\AA$)")
ax.set_ylabel("Potential energy (eV)")
ax.set_title("Ti-terminated TiN(111): vacuum work function")

ax.legend(frameon=False)
ax.grid(alpha=0.15)

fig.tight_layout()

fig.savefig(
    "results/figures/tin111_work_function.png",
    dpi=300,
    bbox_inches="tight"
)

fig.savefig(
    "results/figures/tin111_work_function.pdf",
    bbox_inches="tight"
)

print()
print("TiN(111) vacuum work-function result")
print("------------------------------------")
print(f"Fermi energy       = {EF:.6f} eV")
print(f"Left vacuum        = {VLEFT:.6f} eV")
print(f"Right vacuum       = {VRIGHT:.6f} eV")
print(f"Mean vacuum        = {VVAC:.6f} eV")
print(f"Work function      = {WF:.6f} eV")
print()
print("Created:")
print("results/figures/tin111_work_function.png")
print("results/figures/tin111_work_function.pdf")

