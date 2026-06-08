# Repository map (artifact MVP)

Only the paths a reviewer needs. The repo also contains earlier research-stage material; the MVP path is self-contained.

```
.
├── README.md                  # entry point: install, demo, reproduce
├── ARTIFACT.md                # what this artifact is / claims / does not claim
├── AUDIT_TRAIL.md             # claims downgraded / withdrawn / corrected (trust feature)
├── LICENSE                    # Apache-2.0
├── CITATION.cff               # how to cite (DOI assigned on publication)
├── pyproject.toml             # package: biobenchguard; console script + extras
├── requirements.lock          # pinned CPU-only runtime
├── Dockerfile / .dockerignore # canonical CPU environment (python:3.11-slim)
├── Makefile                   # convenience targets (install/test/demo/figures)
├── biobenchguard/             # the package
│   ├── engine.py              #   rule-based Type A–G audit engine
│   ├── cli.py                 #   5 MVP commands
│   ├── repro.py               #   reproduce_results / reproduce_figures
│   └── __main__.py
├── examples/                  # 4 case.yaml cases (each: README + expected_outputs/)
│   ├── minimal_case/
│   ├── typeE_selection_leakage/
│   ├── typeA_group_shortcut/
│   └── null_degenerate_tdc/   #   -> not_measurable boundary case
├── source_data/         # md5-locked CSVs behind the headline figures + manifest + README
├── results_locked/            # rendered headline figures + RESULTS_INDEX + GOLDEN_FILES
├── tests/                     # golden-file + CLI regression tests (pytest -q)
├── scripts/                   # smoke test + public-data downloader (md5-verify, no vendoring)
└── docs/                      # this map + charter + command/reproduction/license/rename/data/docker/zenodo
```

Earlier research-stage directories (numbered pilots, prior tooling, prior CI variants) remain for provenance but are
**not** part of the MVP reproduction path. The canonical CI is `.github/workflows/tests.yml` + `docker.yml`.
