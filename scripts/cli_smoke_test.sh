#!/usr/bin/env bash
# BioBenchGuard MVP smoke test — every advertised command must run.
# Works whether or not the `biobenchguard` console script is on PATH (falls back to `python -m biobenchguard`).
set -euo pipefail
if command -v biobenchguard >/dev/null 2>&1; then BBG="biobenchguard"; else BBG="${PYTHON:-python} -m biobenchguard"; fi
echo "using: $BBG"
echo "[1] help/version";       $BBG --version; $BBG --help >/dev/null
echo "[2] demo";               $BBG demo --out demo_results
echo "[3] validate";           $BBG validate examples/minimal_case/case.yaml
echo "[4] audit";              $BBG audit examples/typeE_selection_leakage/case.yaml --out audit_results
echo "[5] reproduce-results";  $BBG reproduce-results --quick --out reproduced_results
echo "[6] reproduce-figures";  $BBG reproduce-figures --quick --out reproduced_figures
echo "ALL CLI COMMANDS OK"
