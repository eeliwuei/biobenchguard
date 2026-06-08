# Example: typeE_selection_leakage (genomic prediction, leave-cluster)

A genomic-prediction case (`livestock_pig_GP`, 8 clusters, leave-cluster split, tuned GBLUP/Ridge baseline) where
**selection leakage (Type E)** is present.

```bash
biobenchguard audit examples/typeE_selection_leakage/case.yaml --out out_typeE
```

**Expected per-mechanism status (locked):**
- Type E (selection leakage): **present**
- Type A (group shortcut): **present**
- Type F (feature-count / weighting sensitivity): **present**

**How to read it:** the three-arm contrast C−B is the selection-leakage detector and fires here. Note that C−B is
**specific to selection leakage** — it is *inversely responsive* to a pure group shortcut — which is exactly why
BioBenchGuard reports a **battery** rather than one statistic (see `AUDIT_TRAIL.md` #2/#5).

**Limitation:** illustrative geometry; detection limits depend on the base (see Fig 4 / `*lod*` source data).
