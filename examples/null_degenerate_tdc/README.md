# Example: null_degenerate_tdc (drug scaffold — NOT a characterised domain)

A drug-chemistry case (`tdc_bbb_martins_scaffold`, BBB_Martins, scaffold split). It is included **only as a
null-validity boundary case**: the scaffold structure here is **degenerate** for the artefact contrast, so the artefact
is **not measurable** — which is a distinct, honest state, not "clean".

```bash
biobenchguard audit examples/null_degenerate_tdc/case.yaml --out out_null
```

**Expected per-mechanism status (locked):**
- Type F: **not_measurable_low_coverage**
- Type E (selection leakage): **absent_with_sufficient_contrast**

**How to read it:** `not_measurable` means the data could not support the measurement (insufficient/degenerate
contrast). The tool says so explicitly rather than reporting a misleading "absent". This case exists to demonstrate
that behaviour (and is exercised by `tests/test_cli.py::test_null_degenerate_returns_not_measurable`).

**Limitation (important):** drug-chemistry is **not** a characterised domain in this work. Do **not** read any
detector magnitude from this example as a result about drug benchmarks. See `AUDIT_TRAIL.md` #4.
