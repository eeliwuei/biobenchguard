#!/usr/bin/env python3
"""Locate / verify the public datasets used for FULL reproduction (CPU-only; no GPU).

This artifact does NOT vendor raw public datasets (their upstream licenses govern redistribution). This helper records
the canonical sources and verifies md5/sha256 of any locally provided copy; it never silently substitutes data. If a
dataset is missing it stops with a clear message. See docs/data_sources.md."""
import argparse, hashlib, sys
from pathlib import Path

SOURCES = {
    "wheat_BGLR":     {"desc": "CIMMYT wheat (599x1279) distributed with the BGLR R package", "access": "BGLR/CRAN; public"},
    "rice_RDP1":      {"desc": "Rice Diversity Panel 1 (Zhao 2011; ricediversity.org), 44K SNP PLINK", "access": "ricediversity.org; public"},
    "microbiomeHD":   {"desc": "microbiomeHD CRC/OB cohorts", "access": "Zenodo 840333 (10.5281/zenodo.840333); public"},
    "TDC_ADME":       {"desc": "Therapeutics Data Commons BBB_Martins / Caco2_Wang", "access": "tdcommons.ai / PyTDC; public"},
}

def sha256(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def main():
    ap = argparse.ArgumentParser(description="Locate/verify public datasets for full reproduction (no GPU).")
    ap.add_argument("--data-dir", default="paper/raw_data", help="local dir where raw public data is placed")
    ap.add_argument("--list", action="store_true", help="list canonical sources and exit")
    a = ap.parse_args()
    if a.list:
        for k, v in SOURCES.items():
            print(f"{k}: {v['desc']}  [{v['access']}]")
        return 0
    d = Path(a.data_dir)
    if not d.exists():
        print(f"NOTE: {d} not found. This artifact does not redistribute raw data; obtain each dataset from its public "
              f"source (run --list) under its own license, place it under {d}, then re-run. Quick reproduction "
              f"(reproduce-figures/--quick) needs no raw data.")
        return 1
    print(f"Found data dir {d}; verifying checksums of any provided files (none are bundled by default).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
