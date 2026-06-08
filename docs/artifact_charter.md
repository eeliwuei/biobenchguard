# Artifact charter

**Goal:** a *few-but-stable* artifact — a small number of commands that always work — rather than a large surface that
half-works. We optimise for a reviewer who clones, runs five commands, and reproduces the headline claims on a laptop.

## Design principles
1. **Stable over feature-rich.** Five MVP commands (`demo`, `validate`, `audit`, `reproduce-figures`,
   `reproduce-results`), each tested, beats a dozen flaky ones.
2. **CPU-only.** No GPU is required anywhere in the documented path. Heavy "full" recomputation is CPU-bound.
3. **Locked numbers.** Headline results are md5-pinned in `source_data/`; tests fail on drift.
4. **Honest states.** `not_measurable` ≠ `clean`. Reports say *evidence currently supports / does not yet support /
   not measurable / recommended validation design*.
5. **Traceability.** Every paper number traces to a file here; every removed claim is in `AUDIT_TRAIL.md`.

## Quality targets (Available / Functional / Reusable)
- **Available:** licensed (Apache-2.0), single repo, archival-on-publication plan.
- **Functional:** documented commands, exercised by `pytest`, deterministic.
- **Reusable:** audit your own benchmark via a documented `case.yaml` schema + examples.

## Explicit non-goals
- No artifact-evaluation **badge** is claimed (committees confer badges; authors do not).
- No claim of **independent third-party reproduction**.
- No formal **FAIR score** asserted (FAIR practice followed in spirit).
- Not an automated reviewer; no clinical/causal/universal-detector claims.
