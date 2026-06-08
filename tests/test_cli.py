"""CLI / example regression tests: each bundled example audits to its expected per-mechanism status, and the audit
emits report.md + report.json. Rule-based, deterministic. Run: pytest -q"""
from pathlib import Path
import sys, json
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import pytest
import biobenchguard as bbg
from biobenchguard import cli

EX = ROOT / "examples"

# headline statuses each MVP example must reproduce (subset that is stable)
EXPECT = {
    "minimal_case":            {"E": "present", "C": "absent_with_sufficient_contrast"},
    "typeE_selection_leakage": {"E": "present", "A": "present", "F": "present"},
    "typeA_group_shortcut":    {"A": "present", "C": "present"},
    "null_degenerate_tdc":     {"F": "not_measurable_low_coverage", "E": "absent_with_sufficient_contrast"},
}
OUTPUTS = ["report.md", "report.json", "feasibility_matrix.csv", "type_A_to_G_status.csv",
           "allowed_claims.md", "forbidden_claims.md", "recommended_validation_design.md", "audit_report.md"]

def test_four_examples_present():
    found = sorted(p.name for p in EX.iterdir() if (p / "case.yaml").exists())
    assert set(found) >= set(EXPECT), f"missing examples; found {found}"

@pytest.mark.parametrize("ex", sorted(EXPECT))
def test_example_audit_status_and_outputs(ex, tmp_path):
    case = EX / ex / "case.yaml"
    name, dom, status, outdir = bbg.run_case(case, tmp_path)
    for t, s in EXPECT[ex].items():
        assert status.get(t) == s, f"{ex}: Type {t} expected {s}, got {status.get(t)}"

@pytest.mark.parametrize("ex", sorted(EXPECT))
def test_audit_command_emits_reports(ex, tmp_path):
    import argparse
    rc = cli.cmd_audit(argparse.Namespace(case=str(EX / ex / "case.yaml"), out=str(tmp_path)))
    assert rc == 0
    for f in OUTPUTS:
        assert (tmp_path / f).exists(), f"{ex}: missing {f}"
    rep = json.loads((tmp_path / "report.json").read_text())
    assert rep["tool"] == "BioBenchGuard"
    assert "evidence_currently_supports" in rep and "recommended_validation_design" in rep

def test_validate_minimal_case():
    import argparse
    assert cli.cmd_validate(argparse.Namespace(case=str(EX / "minimal_case" / "case.yaml"))) == 0

def test_null_degenerate_returns_not_measurable():
    case = EX / "null_degenerate_tdc" / "case.yaml"
    _, _, status, _ = bbg.run_case(case, ROOT / "_tmp_null")
    assert any(s.startswith("not_measurable") for s in status.values()), "degenerate-null case must yield not_measurable"
