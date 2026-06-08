"""Golden-file regression tests for the BioBenchGuard paper artifact.

Locks the packaged source data (md5 against the recorded manifest) and asserts the quick reproduction path runs and
emits the expected outputs. Exact-match on stored CSVs (no recomputation tolerance needed in quick mode). Run: pytest -q
"""
import csv, hashlib
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import biobenchguard as bbg
from biobenchguard import repro

SRC = ROOT / "source_data"

def _md5(p): return hashlib.md5(Path(p).read_bytes()).hexdigest()

def _manifest():
    rows = {}
    with open(SRC / "source_data_manifest.csv") as f:
        for r in csv.DictReader(f):
            rows[r["file"]] = r
    return rows

def test_source_data_manifest_exists_and_nonempty():
    m = _manifest()
    assert len(m) >= 10, f"expected >=10 locked source-data files, found {len(m)}"

def test_source_data_md5_matches_golden():
    """Every packaged source CSV must match its recorded md5 (catch unintended numerical drift)."""
    m = _manifest()
    for fname, row in m.items():
        p = SRC / fname
        assert p.exists(), f"missing locked source file: {fname}"
        got = _md5(p)
        assert got == row["md5"], f"{fname}: md5 drift (golden {row['md5']} != {got})"

def test_quick_reproduce_results(tmp_path):
    rows = repro.reproduce_results(tmp_path, quick=True)
    assert len(rows) >= 10
    assert (tmp_path / "reproduced_results_manifest.csv").exists()
    # copied files must be byte-identical to the locked source
    for r in rows:
        assert _md5(SRC / r["file"]) == _md5(tmp_path / "source_data" / r["file"]), f"{r['file']} not byte-identical"

def test_quick_reproduce_figures(tmp_path):
    written = repro.reproduce_figures(tmp_path, quick=True)
    assert len(written) >= 1, "no figures reproduced"
    for p in written:
        assert Path(p).exists() and Path(p).stat().st_size > 0, f"empty/missing figure: {p}"
    # the two headline figures
    assert (tmp_path / "repro_typeE_power.png").exists()
    assert (tmp_path / "repro_typeA_vs_typeE.png").exists()
