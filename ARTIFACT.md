# Artifact description — BioBenchGuard

This repository is the research artifact accompanying the manuscript *"Certified reference benchmarks reveal the
operating characteristics of artefact detectors in biological prediction"* (benchmark-metrology line). It is designed
to be **reviewer-runnable and reproducible on a laptop, CPU-only**.

## What the artifact contains
- **`biobenchguard/`** — a transparent, rule-based engine and a 5-command CLI (`demo`, `validate`, `audit`,
  `reproduce-figures`, `reproduce-results`).
- **`examples/`** — four `case.yaml` cases, each with a README and an `expected_outputs/` snapshot, spanning a present
  artefact, selection leakage, a group shortcut, and a degenerate `not_measurable` null.
- **`source_data/`** — the locked, md5-pinned source data behind the paper's headline figures.
- **`results_locked/`** — the rendered headline figures and an index mapping each to its source data.
- **`tests/`** — golden-file + CLI regression tests (`pytest -q`).
- **`Dockerfile`, `requirements.lock`** — a pinned, canonical CPU environment.
- **`AUDIT_TRAIL.md`** — the staged record of claims that were downgraded, withdrawn, or corrected.

## What we claim — and what we do not
We aim for the **Available / Functional / Reusable** qualities used by artifact-evaluation committees:
- **Available** — a single repository with a license (Apache-2.0) and an archival plan (DOI assigned upon publication).
- **Functional** — documented, exercised by automated tests, and runnable from the documented commands.
- **Reusable** — others can audit their **own** benchmark via `case.yaml`, with a documented schema and examples.

We **do not** claim any artifact-evaluation **badge**, and we do **not** claim independent third-party reproduction.
Those are conferred by reviewers/committees, not asserted by authors. We follow **FAIR** practice in spirit
(identifier on archival, rich metadata, open formats, license) without asserting a formal FAIR score.

## Scope boundaries (read before interpreting any output)
- BioBenchGuard is a **rule set**, not a trained model and not an automated reviewer.
- It reports **measurement feasibility and operating characteristics**, not a verdict that a benchmark or paper is wrong.
- `not_measurable` is a distinct state from `clean`/`absent`; absence is only meaningful with sufficient contrast.
- No clinical, diagnostic, or causal utility is claimed.
- Running the artifact changes **no** production threshold and touches **no** external system.

## How to start
See [`README.md`](README.md) for install + quick demo, [`docs/reviewer_reproduction.md`](docs/reviewer_reproduction.md)
for the one-page reproduction table, and [`docs/command_reference.md`](docs/command_reference.md) for the CLI.
