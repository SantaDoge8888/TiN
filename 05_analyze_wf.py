#!/usr/bin/env python3
from pathlib import Path
import re, statistics

RY_TO_EV = 13.605693122994
BOHR_TO_ANG = 0.529177210903
ZMIN_SLAB_A = 10.0000000000
ZMAX_SLAB_A = 32.0524708820
VAC_MARGIN_A = 3.0

scf = Path("outputs/02_tin111_scf.out")
avg = Path("outputs/tin111.avg.dat")
report = Path("outputs/work_function.txt")

if not scf.exists():
    raise SystemExit("Missing outputs/02_tin111_scf.out")
if not avg.exists():
    raise SystemExit("Missing outputs/tin111.avg.dat")

txt = scf.read_text(errors="ignore")
vals = re.findall(r"the Fermi energy is\s+([-+0-9.Ee]+)\s+ev", txt, flags=re.I)
if not vals:
    raise SystemExit("Could not find the Fermi energy in SCF output.")
ef = float(vals[-1])

rows=[]
for line in avg.read_text(errors="ignore").splitlines():
    p=line.split()
    if len(p) < 3:
        continue
    try:
        z_bohr=float(p[0]); planar=float(p[1]); macro=float(p[2])
    except ValueError:
        continue
    rows.append((z_bohr*BOHR_TO_ANG, planar, macro))

left=[r[2] for r in rows if r[0] < ZMIN_SLAB_A - VAC_MARGIN_A]
right=[r[2] for r in rows if r[0] > ZMAX_SLAB_A + VAC_MARGIN_A]
if not left or not right:
    raise SystemExit("Could not identify both vacuum plateaus from avg.dat.")

vl = statistics.mean(left)*RY_TO_EV
vr = statistics.mean(right)*RY_TO_EV
vv = (vl+vr)/2
wf = vv-ef
asym=abs(vl-vr)

body = f"""Ti-terminated TiN(111) / vacuum benchmark

Fermi energy (slab)        = {ef:.6f} eV
Left vacuum level          = {vl:.6f} eV
Right vacuum level         = {vr:.6f} eV
Mean vacuum level          = {vv:.6f} eV
Vacuum asymmetry           = {asym:.6f} eV
WORK FUNCTION              = {wf:.6f} eV

Literature comparison:
Fonseca & Knizhnik (PRB 74, 195304 (2006)) report ~4.67 eV
for a Ti-terminated 19-layer rocksalt TiN(111) slab in GGA.

Do not expect bitwise agreement: this benchmark uses Quantum ESPRESSO,
a different pseudopotential family, 60/600 Ry cutoffs, and this specific
relaxation/vacuum setup. A result in the neighborhood of the literature
value is the validation target; convergence should then be checked versus
k-grid, vacuum thickness, slab thickness, and cutoff.
"""
report.write_text(body)
print(body)
