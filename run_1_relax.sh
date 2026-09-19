#!/usr/bin/env bash
set -euo pipefail
NP=${NP:-1}
mkdir -p tmp outputs
echo "Running TiN(111) slab relaxation with NP=$NP ..."
if [ "$NP" -gt 1 ] && command -v mpirun >/dev/null 2>&1; then
  mpirun -np "$NP" pw.x -in 01_tin111_relax.in > outputs/01_tin111_relax.out
else
  pw.x -in 01_tin111_relax.in > outputs/01_tin111_relax.out
fi
grep "JOB DONE" outputs/01_tin111_relax.out
python3 02_extract_relaxed.py
echo "Relaxation finished and 02_tin111_scf.in created."
