#!/usr/bin/env bash
set -e
echo "=== Executables ==="
for x in pw.x pp.x average.x python3; do
  printf "%-12s " "$x"
  command -v "$x" || true
done
echo
echo "=== Pseudopotentials ==="
for f in pseudo/Ti.pbe-spn-rrkjus_psl.1.0.0.UPF pseudo/N.pbe-n-rrkjus_psl.1.0.0.UPF; do
  if [ -s "$f" ]; then echo "OK  $f"; else echo "MISSING  $f"; fi
done
echo
echo "=== System ==="
echo -n "CPU threads: "; nproc 2>/dev/null || sysctl -n hw.logicalcpu 2>/dev/null || true
free -h 2>/dev/null || true
