# Audit trail

## 1. Why an audit trail matters
A benchmark-metrology paper claims to measure the reliability of *other people's* evaluations. It is only credible if
its own claims have been filtered. This page records, openly, which candidate claims were **downgraded**, **withdrawn**,
or **corrected**, which cases are reported as **not measurable**, and which claims are **currently locked**. Documenting
what we removed is part of why the surviving claims are trustworthy. Every locked claim is traceable to the md5-pinned
source data in `paper/source_data/` and the figures in `results_locked/`.

## 2. Candidate claims that were downgraded
- **The claim-audit tally (`≈60%`, later `37/62`; inter-rater `κ`).** Earlier framed as a headline. On re-examination
  it depended on **automated coding without a human gold standard** and on which claims entered the corpus. It is
  retained as **background/motivation only**, not a current result, and not a population estimate. (L2 history:
  `docs/historical_l2_program.md`.)

## 3. Claims that were withdrawn
- **A calibration "sign flip".** A statement implying the leakage statistic moved one fixed direction across artefacts
  was withdrawn after an oracle-vs-observed scale audit: the selection-leakage statistic **C−B is inversely responsive
  to a group/structure shortcut** (opposite sign in that regime). The paper now states C−B is *specific* to selection
  leakage and is *not a valid detector* of group shortcuts — motivating a detector **battery**.

## 4. Coding artefacts that were corrected
- **Binary saturation.** A result reported at face value was found to be an artifact of metric **saturation under the
  binary encoding**, not detection power. It is reported with the saturation caveat and is **not** used as evidence of
  power.
- **Version-naming drift.** Distinct manuscript version names once carried identical content/md5. Corrected: one
  canonical file per version, version stamped in the PDF header, lineage recorded.

## 5. Boundary cases reported as not measurable
- **TDC drug-chemistry (scaffold split).** The available grouping is **singleton-dominated**, so the group-aware null
  is degenerate and **cannot be interpreted as "clean"**. It is reported as **`not_measurable`** and included only as a
  null-validity boundary case (`examples/null_degenerate_tdc/`), **not** a fully characterised active domain.

## 6. Current locked claims
- Artefact detectors have **measurable operating characteristics** (FPR, power, LOD, uncertainty) — reportable as
  instruments, not as a single clean/leaky verdict. (Fig 3, 4, 6)
- Selection-leakage detection power is **geometry-dependent**; the LOD orders microbiome (≈600) < wheat (≈1000) < rice
  (right-censored). (Fig 4)
- A single artefact statistic is **mechanism-specific**; C−B is inversely responsive to a group shortcut → a **battery**
  is required. (Fig 5)
- A degenerate group structure yields **`not_measurable`**, reported as distinct from "clean". (TDC boundary case)

## 7. How to verify from source data
- **Figures:** `biobenchguard reproduce-figures --quick` redraws the headline panels from `paper/source_data/`.
- **Source data:** `biobenchguard reproduce-results --quick` re-emits and checksums the locked CSVs against
  `paper/source_data/source_data_manifest.csv`.
- **Honesty checks (tests):** `pytest -q` — golden-file md5 lock (`tests/test_golden_files.py`) + the TDC
  `not_measurable` case (`tests/test_cli.py::test_null_degenerate_returns_not_measurable`).
- **Lock policy:** `results_locked/GOLDEN_FILES.md` (superseded results must not return).

> No superseded result is hidden. If a number is in the paper it should trace to a file here; if it was removed, it is
> in §2–§5 above.
