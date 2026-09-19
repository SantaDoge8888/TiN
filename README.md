# Ti-terminated TiN(111) vacuum work-function benchmark

This is the **vacuum control** to run before the TiN/HfO2 interface calculation.

## Physics target
Fonseca & Knizhnik, Phys. Rev. B 74, 195304 (2006), report a GGA vacuum
work function of about **4.67 eV** for a **Ti-terminated 19-layer rocksalt
TiN(111) slab**.

This project builds the same *type* of benchmark in Quantum ESPRESSO:
- rocksalt TiN lattice constant: 4.2440 Å
- 19 alternating Ti/N (111) atomic planes
- Ti termination on both surfaces (Ti10N9)
- slab thickness: 22.052 Å
- total vacuum: 20.0 Å
- symmetric slab, so no dipole correction is required
- PBE, PSlibrary ultrasoft pseudopotentials
- 60 Ry wavefunction / 600 Ry charge-density cutoffs
- 12x12x1 k grid for relaxation
- 24x24x1 k grid for final SCF
- central 7 planes fixed, outer 6 planes on each side relaxed

## Why this comes before HfO2
It validates the exact QE slab -> potential -> vacuum level -> work-function
pipeline. If this is reasonable, the later TiN/HfO2 calculation can focus on
interface VBO/W_eff rather than basic setup errors.

## Run
```bash
chmod +x *.sh *.py
./00_download_pseudos.sh
./check_setup.sh
NP=4 bash run_1_relax.sh
NP=4 bash run_2_final.sh
cat outputs/work_function.txt
```

Start with NP=1 if MPI gives trouble.

## Work function
The script uses
    Phi = V_vac - E_F
where V_vac is obtained from the macroscopic average of the electrostatic
potential in the two vacuum regions.

The postprocessing follows Quantum ESPRESSO's official WorkFct_example
(`pw.x -> pp.x -> average.x`, with `plot_num=11`).

## Important
4.67 eV is a literature benchmark, not a guaranteed exact output. Different
pseudopotentials, lattice constant, relaxation details, and numerical settings
can shift the number. Once the pipeline works, test convergence against:
1. k-grid
2. vacuum thickness
3. slab thickness
4. cutoffs
