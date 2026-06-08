# Example: typeA_group_shortcut (crop genomic prediction, leave-cluster)

A crop genomic-prediction case (`crop_wheat_GP`, 5 clusters, leave-cluster split, tuned-GBLUP baseline) dominated by a
**group/structure shortcut (Type A)**.

```bash
biobenchguard audit examples/typeA_group_shortcut/case.yaml --out out_typeA
```

**Expected per-mechanism status (locked):**
- Type A (group shortcut): **present**
- Type C (nonlinear baseline gap): **present**

**How to read it:** the gap between random-split and leave-group-out performance evidences a group shortcut. This is a
*different mechanism* from selection leakage — the contrast that detects A is not the contrast that detects E, which is
the paper's mechanism-separation point (Fig 5).

**Limitation:** illustrative; the corrected vs uncorrected magnitudes for wheat are in `wheat_typeA_g3.csv`.
