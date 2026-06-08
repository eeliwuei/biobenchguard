"""BioBenchGuard — transparent, rule-based measurement-feasibility audit tool for structured biological
prediction benchmarks. NOT a trained model, NOT an automated reviewer, NOT a clinical tool. It reports
which artefact claims the evidence currently supports, does not yet support, or cannot measure, and a
recommended validation design. No production threshold is changed by running it.

Public API:
    run_case(case_path, out_dir=None) -> (name, domain, {Type: status}, out_dir)
    assign_status(case_dict, thresholds) -> ({Type: (status, rationale)}, detail)
    examples_dir() -> Path to bundled example cases
"""
import os
from pathlib import Path
from . import engine

run_case = engine.run_case
assign_status = engine.assign_status
generate_claim_boundary_report = engine.generate_claim_boundary_report
DEFAULTS = engine.DEFAULTS
__version__ = "0.3.0"

def examples_dir():
    return Path(__file__).resolve().parent.parent / "examples"

__all__ = ["run_case", "assign_status", "generate_claim_boundary_report", "DEFAULTS", "engine",
           "examples_dir", "__version__"]
