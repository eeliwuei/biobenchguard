# Example: minimal_case (microbiome, leave-study-out)

The smallest end-to-end case — a microbiome colorectal-cancer task (`microbiome_crc_loso`, 3 studies/groups,
leave-study-out split, logistic-regression baseline). Use it as the first thing you run.

```bash
biobenchguard audit examples/minimal_case/case.yaml --out out_minimal
```

**Expected per-mechanism status (locked, see `expected_outputs/`):**
- Type E (selection leakage): **present**
- Type C (nonlinear baseline gap): **absent_with_sufficient_contrast**

**How to read it:** "present" means the evidence currently supports that the artefact is detectable here; "absent with
sufficient contrast" means the contrast existed to detect it and it was not found (distinct from `not_measurable`).

**Limitation:** a compact illustrative case; the magnitudes are not a domain characterisation. For the characterised
microbiome results see the manuscript and `source_data/`.
