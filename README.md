# BioBenchGuard

Rule-based measurement-feasibility audit for biological-prediction benchmarks, and the reproduction package for the
paper *"Certified reference benchmarks reveal the operating characteristics of artefact detectors in biological
prediction."* **CPU-only.** It is a transparent rule set — not a trained model and not an automated reviewer (see
[About](#about)).

## Install
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.lock
pip install --no-deps -e .
```

## Run demo
```bash
biobenchguard demo --out outputs/demo
```

## Audit your own case
```bash
biobenchguard audit examples/minimal_case/case.yaml --out outputs/minimal_audit
```
Write your own `case.yaml` with the schema in [`docs/case_yaml_schema.md`](docs/case_yaml_schema.md). Reports use the
wording *evidence currently supports / does not yet support / not measurable / recommended validation design*.

## Reproduce paper figures
```bash
biobenchguard reproduce-figures --quick --out outputs/reproduced_figures   # redraw headline figures from locked source data
biobenchguard reproduce-results --quick --out outputs/reproduced_results   # re-emit + checksum locked source data
```
Quick mode is CPU-only and runs in seconds from [`source_data/`](source_data/). See
[`docs/reviewer_reproduction.md`](docs/reviewer_reproduction.md).

## Docker
```bash
docker build -t biobenchguard:paper .
docker run --rm -v "$PWD:/work" biobenchguard:paper biobenchguard demo --out /work/outputs/demo
docker run --rm biobenchguard:paper pytest -q
```

## Tests
```bash
pytest -q   # golden-file + CLI regression tests
```

## Repository map
```
biobenchguard/   rule-based engine + 5-command CLI
examples/        case.yaml examples (incl. a not_measurable null) + expected outputs
source_data/     md5-locked source data behind the figures (+ tables/, + manifest)
results_locked/  rendered Fig1–Fig7 + RESULTS_INDEX + GOLDEN_FILES
tests/           golden-file + CLI tests
docs/            command reference, reviewer reproduction, case.yaml schema, ...
```

## Citation & availability
Cite via [`CITATION.cff`](CITATION.cff). Publicly available under **Apache-2.0** ([`LICENSE`](LICENSE)); a citable archival DOI will be deposited on acceptance.

---

## About
BioBenchGuard treats each artefact check (selection leakage, group/structure shortcuts, null-validity) as a
*measurement instrument* and reports its **operating characteristic** — false-positive rate, detection power, limit of
detection, uncertainty, and mechanism specificity — instead of a single clean/leaky verdict. Because a single statistic
is mechanism-specific, it reports a small detector **battery**, not one number.

**It is not** an automated reviewer, a clinical/diagnostic tool, a model leaderboard, or a universal leakage detector,
and it makes **no** claim that any specific published benchmark or paper is wrong. `not measurable` is distinct from
`clean`. The curated record of downgraded/withdrawn/corrected claims is in [`AUDIT_TRAIL.md`](AUDIT_TRAIL.md).

**Limitations:** synthetic injected labels are controlled probes, not biological effects; the C−B statistic is specific
to selection leakage (not a valid detector of group shortcuts); detection limits are grid-based and uncertainty-limited;
drug-chemistry (scaffold) data is a null-validity boundary case, not a characterised domain. The earlier
measurement-feasibility program is documented as a precursor in
[`docs/historical_l2_program.md`](docs/historical_l2_program.md).
