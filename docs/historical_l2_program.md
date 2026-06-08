# Historical precursor: the measurement-feasibility (L2) program

This page documents the **earlier research line** that preceded the current benchmark-metrology manuscript. It is kept
openly for provenance and as an audit trail. **It is background, not the current paper's headline.** The current paper
is centered on certified reference benchmarks and the operating characteristics of artefact detectors (see the root
[`README.md`](../README.md)).

The full stage-by-stage materials live under [`development/`](../development/) (moved there from the repository root so
the landing page reflects the current artifact). Nothing was deleted.

## What the L2 program was
- **Measurement-feasibility principle** — "model ranking is downstream of measurability": before comparing models on a
  benchmark, ask whether the benchmark can even *measure* the evaluation artefact a superiority claim depends on.
- **A cross-domain claim audit** — a corpus of published model-superiority claims was screened for artefact
  sensitivity across several biological-prediction domains (genomics, microbiome, crop, protein, drug, human-PRS).
- **A six-domain pilot set** and a **Type A–G feasibility taxonomy**.
- **BioBenchGuard v0.6.0-rc1** — an early private-beta release candidate of the rule-based tool.

## Why those headline numbers are no longer the current result
The L2 audit produced figures such as a fraction of claims being artefact-sensitive (the "≈60%", later quoted as a
`37/62` tally) and an inter-rater agreement (`κ`). On re-examination these were **downgraded to background**:
- the claim tally depended on automated coding without a human gold standard and on which claims entered the corpus;
- it is motivation, not a population estimate.

These and other corrections (calibration sign convention; binary-saturation coding artefact; the TDC scaffold case as
`not_measurable`) are recorded in the curated [`AUDIT_TRAIL.md`](../AUDIT_TRAIL.md).

## How L2 became the benchmark-metrology paper
The feasibility taxonomy matured into a **metrology** framing: instead of a binary "can/can't measure" gate, treat each
artefact detector as a **measurement instrument** with operating characteristics — false-positive rate, detection
power, limit of detection, uncertainty, and mechanism specificity — validated on **certified reference benchmarks**
(real feature geometry + an injected synthetic label of known truth). That is the current manuscript.

## Where the L2 files are now
| Material | Location |
|----------|----------|
| L2 manuscript drafts | `development/08_manuscript_future/L2_measurement_feasibility/` |
| Six-domain pilots | `development/04_domain_pilots/` |
| Published-claim audit | `development/05_published_claim_audit/` |
| Feasibility-gate / theory | `development/02_theory/`, `development/03_feasibility_gate/` |
| Early tool + private-beta | `development/06_tools/`, `development/12_release_engineering/`, `development/13_private_beta_trial/` |
| Metrology development stages | `development/16_benchmark_metrology/`, `development/18_semisynthetic_reference_benchmarks/` |

> The current, reviewer-facing artifact is the curated set at the repository root (`biobenchguard/`, `source_data/`,
> `results_locked/`, `examples/`, `tests/`). `development/` is the honest "how we got here" — not the deliverable.
