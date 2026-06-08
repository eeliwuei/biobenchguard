"""Reproduce locked paper figures/results from packaged source data (quick mode).

Quick mode verifies *plotting and locked source-data packaging* — it redraws the main figures and re-emits a
checksum manifest from source_data/. It does NOT recompute the analysis from raw inputs (that is full mode,
which recomputes the source data on CPU and can take hours; see docs/reviewer_reproduction.md). No GPU is required.
"""
import os, csv, hashlib
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SRC = REPO / "source_data"
NAME = {"wheat": "wheat", "microbiome_crc": "microbiome CRC", "microbiome_ob": "microbiome OB",
        "microbiome_crc_kmeans": "microbiome CRC (imposed)", "rice_rdp1": "rice RDP1"}
CMAP = {"wheat": "#1f77b4", "microbiome_crc": "#d62728", "microbiome_ob": "#ff7f0e",
        "microbiome_crc_kmeans": "#9467bd", "rice_rdp1": "#2ca02c"}

def _md5(p): return hashlib.md5(Path(p).read_bytes()).hexdigest()[:12]

def reproduce_results(out_dir, quick=True, source=SRC):
    """Copy locked source-data CSVs to out_dir and write a checksum manifest. Returns the manifest rows."""
    import pandas as pd
    out = Path(out_dir); (out / "source_data").mkdir(parents=True, exist_ok=True)
    rows = []
    for f in sorted(Path(source).glob("*.csv")):
        dst = out / "source_data" / f.name
        dst.write_bytes(f.read_bytes())
        try:
            df = pd.read_csv(f); nr, nc = df.shape
        except Exception:
            nr = nc = -1
        rows.append({"file": f.name, "md5": _md5(f), "rows": nr, "cols": nc})
    with open(out / "reproduced_results_manifest.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["file", "md5", "rows", "cols"]); w.writeheader(); w.writerows(rows)
    (out / "REPRODUCE_NOTE.md").write_text(
        "# Quick reproduction (results)\n\nQuick mode verifies locked source-data packaging: it copies the "
        "frozen source-data CSVs and records their md5 + shape. It does **not** recompute the analysis from raw "
        "inputs (that is full mode). No GPU is required.\n")
    return rows

def reproduce_figures(out_dir, quick=True, source=SRC):
    """Redraw the two headline figures (Type E operating characteristic; Type A vs Type E mechanism) from packaged
    source data. Returns the list of written figure paths."""
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import pandas as pd, numpy as np
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True); written = []
    plt.rcParams.update({"font.size": 12, "axes.spines.top": False, "axes.spines.right": False,
                         "savefig.bbox": "tight", "figure.dpi": 150})

    # ---- Fig: Type E operating characteristic (power vs L; 3 geometries) ----
    try:
        pw = pd.read_csv(source / "typeE_matched_fpr_power.csv")
        rp = pd.read_csv(source / "rice_typeE_power.csv")
        pw = pd.concat([pw[["dataset", "target_fpr", "L", "power"]], rp[["dataset", "target_fpr", "L", "power"]]],
                       ignore_index=True)
        fig, ax = plt.subplots(figsize=(7, 5))
        for nm in ["wheat", "microbiome_crc", "rice_rdp1"]:
            d = pw[(pw.dataset == nm) & (pw.target_fpr == 0.05)].sort_values("L")
            if len(d): ax.plot(d.L, d.power, "-o", color=CMAP.get(nm, "#888"), label=NAME.get(nm, nm))
        ax.axhline(0.8, color="#888", ls=":", lw=1)
        ax.set_xlabel("candidate-pool size L"); ax.set_ylabel("detection power @ FPR=0.05")
        ax.set_title("Type E operating characteristic (quick repro from locked source data)")
        ax.legend(); ax.grid(axis="y"); ax.set_ylim(0, 1.05)
        p = out / "repro_typeE_power.png"; fig.savefig(p); plt.close(fig); written.append(str(p))
    except Exception as e:
        print(f"  [warn] Type E figure skipped: {e}")

    # ---- Fig: Type A vs Type E mechanism specificity (4 bases) ----
    try:
        frames = []
        for f, keep in [("typeA_corrected_g3.csv", ["microbiome_crc", "microbiome_ob"]),
                        ("typeA_rice_g3.csv", None), ("wheat_typeA_g3.csv", None)]:
            fp = source / f
            if fp.exists():
                df = pd.read_csv(fp)
                frames.append(df[df.dataset.isin(keep)] if keep else df)
        nat = pd.concat(frames, ignore_index=True)
        fig, ax = plt.subplots(1, 2, figsize=(12, 5))
        for nm, d in nat.groupby("dataset"):
            d = d.sort_values("eta_group")
            ax[0].plot(d.eta_group, d.typeA_optimism_median, "-o", color=CMAP.get(nm, "#888"), label=NAME.get(nm, nm))
            ax[1].plot(d.eta_group, d.typeE_CminusB_median, "-s", color=CMAP.get(nm, "#888"), label=NAME.get(nm, nm))
        for a, t in zip(ax, ["Type A optimism RISES with eta", "Type E C-B does NOT rise (inversely responsive)"]):
            a.axhline(0, color="#999", lw=1); a.set_xlabel("group-shortcut severity eta"); a.set_title(t)
            a.legend(fontsize=8); a.grid(axis="y")
        ax[0].set_ylabel("Type A optimism (random - leave-group-out)"); ax[1].set_ylabel("Type E statistic C-B")
        p = out / "repro_typeA_vs_typeE.png"; fig.savefig(p); plt.close(fig); written.append(str(p))
    except Exception as e:
        print(f"  [warn] Type A/E figure skipped: {e}")

    (out / "REPRODUCE_NOTE.md").write_text(
        "# Quick reproduction (figures)\n\nRedrawn from packaged locked source data in `source_data/`. Quick "
        "mode verifies plotting + locked source-data packaging, not analysis recomputation (full mode). No GPU "
        "required. Publication figures are in the manuscript `figures/` directory.\n")
    return written
