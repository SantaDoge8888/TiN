#!/usr/bin/env bash
set -euo pipefail
NP=${NP:-1}
mkdir -p tmp outputs
if [ ! -f 02_tin111_scf.in ]; then
  echo "02_tin111_scf.in not found. Run run_1_relax.sh first."
  exit 1
fi
echo "Running final SCF with NP=$NP ..."
if [ "$NP" -gt 1 ] && command -v mpirun >/dev/null 2>&1; then
  mpirun -np "$NP" pw.x -in 02_tin111_scf.in > outputs/02_tin111_scf.out
  mpirun -np "$NP" pp.x -in 03_tin111_pp.in > outputs/03_tin111_pp.out
else
  pw.x -in 02_tin111_scf.in > outputs/02_tin111_scf.out
  pp.x -in 03_tin111_pp.in > outputs/03_tin111_pp.out
fi
average.x < 04_tin111_avg.in > outputs/04_tin111_avg.out
mv -f avg.dat outputs/tin111.avg.dat
python3 05_analyze_wf.py
