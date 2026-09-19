#!/usr/bin/env python3
from pathlib import Path
import re, sys

out = Path("outputs/01_tin111_relax.out")
template = Path("02_tin111_scf.template.in")
dest = Path("02_tin111_scf.in")

if not out.exists():
    raise SystemExit("Missing outputs/01_tin111_relax.out")

text = out.read_text(errors="ignore")
matches = list(re.finditer(r"ATOMIC_POSITIONS\s*\(angstrom\)\s*\n", text, flags=re.I))
if not matches:
    raise SystemExit("Could not find final ATOMIC_POSITIONS (angstrom) block in relaxation output.")

start = matches[-1].end()
lines = text[start:].splitlines()
atoms = []
for line in lines:
    s=line.strip()
    if not s:
        if atoms:
            break
        continue
    parts=s.split()
    if len(parts) < 4 or parts[0] not in ("Ti","N"):
        if atoms:
            break
        continue
    atoms.append(" ".join(parts[:4]))

if len(atoms) != 19:
    raise SystemExit(f"Expected 19 atoms in final coordinate block; found {len(atoms)}.")

t = template.read_text()
t = t.replace("__RELAXED_POSITIONS__", "\n".join(atoms))
dest.write_text(t)
print(f"Wrote {dest} with {len(atoms)} relaxed atomic positions.")
