# Docker quickstart

A pinned, CPU-only canonical environment (`python:3.11-slim`). No GPU. `MPLBACKEND=Agg` so figures render headless.

```bash
# build
docker build -t biobenchguard:paper .

# tool runs
docker run --rm biobenchguard:paper biobenchguard --version          # -> BioBenchGuard 0.3.0
docker run --rm biobenchguard:paper pytest -q                        # -> 15 passed

# audit a bundled example, writing results to the host
docker run --rm -v "$PWD:/work" biobenchguard:paper \
  biobenchguard audit examples/typeE_selection_leakage/case.yaml --out /work/audit_results

# reproduce headline figures to the host (quick mode)
docker run --rm -v "$PWD:/work" biobenchguard:paper \
  biobenchguard reproduce-figures --quick --out /work/reproduced_figures
```

Notes:
- The image installs from `requirements.lock` + the package; the default `CMD` is `biobenchguard --help`.
- `-v "$PWD:/work"` mounts the host working directory so outputs land on the host.
- The image contains the locked source data, so quick reproduction works with no network access.
- Full recomputation inside Docker additionally needs the `full` extra and public datasets (see `docs/data_sources.md`).
