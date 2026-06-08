"""BioBenchGuard MVP command-line interface.

Commands (few and stable, by design):
  biobenchguard demo               --out OUTDIR     run the bundled minimal example end-to-end
  biobenchguard validate CASE.yaml                  check a case.yaml has the required structure
  biobenchguard audit CASE.yaml    --out OUTDIR     audit a case -> report.md + report.json (+ raw tables)
  biobenchguard reproduce-figures  --quick --out D  redraw headline figures from locked source data
  biobenchguard reproduce-results  --quick --out D  re-emit + checksum locked source data

Rule-based and transparent: not a trained model, not an automated reviewer, not a clinical tool. No production
threshold is changed by running it. Reports say what the evidence currently supports / does not yet support /
cannot measure, plus a recommended validation design.
"""
import argparse, json, sys
from pathlib import Path
from . import engine, examples_dir, __version__

REQUIRED_TOP = ["name", "domain", "dataset_metadata"]

def _status_full(case_path):
    import yaml
    c = yaml.safe_load(Path(case_path).read_text())
    T = dict(engine.DEFAULTS); T.update(c.get("thresholds", {})); T["struct_aware_splits"] = set(T["struct_aware_splits"])
    status, detail = engine.assign_status(c, T)
    allowed, forbidden, reco = engine.generate_claim_boundary_report(status)
    return c, status, allowed, forbidden, reco

def cmd_validate(args):
    import yaml
    p = Path(args.case)
    if not p.exists():
        print(f"ERROR: case file not found: {p}"); return 2
    try:
        c = yaml.safe_load(p.read_text())
    except Exception as e:
        print(f"ERROR: not valid YAML: {e}"); return 2
    missing = [k for k in REQUIRED_TOP if k not in (c or {})]
    if missing:
        print(f"INVALID: missing required top-level keys: {missing}"); return 1
    # try a dry status assignment to confirm the engine can read it
    try:
        _status_full(p)
    except Exception as e:
        print(f"INVALID: engine could not interpret the case: {e}"); return 1
    print(f"VALID: {c.get('name')} ({c.get('domain')}) — {p}")
    return 0

def _write_reports(name, dom, status, allowed, forbidden, reco, out):
    out = Path(out); out.mkdir(parents=True, exist_ok=True)
    supports = [a for a in allowed]
    not_yet = [f for f in forbidden]
    report = {
        "tool": "BioBenchGuard", "version": __version__, "mode": "rule-based (not a trained model)",
        "benchmark": name, "domain": dom,
        "per_mechanism_status": {t: s for t, (s, _) in status.items()},
        "evidence_currently_supports": supports,
        "evidence_does_not_yet_support": not_yet,
        "recommended_validation_design": reco,
        "disclaimer": "Rule-based audit of measurement feasibility. Not an automated reviewer; does not claim any "
                      "benchmark or paper is wrong. 'not measurable' is distinct from 'clean'. No production threshold changed.",
    }
    (out / "report.json").write_text(json.dumps(report, indent=2))
    lines = [f"# BioBenchGuard audit — {name} ({dom})", "",
             "_Rule-based, transparent (not a trained model, not an automated reviewer, not a clinical tool)._", "",
             "## Per-mechanism status", ""]
    for t, (s, why) in status.items():
        lines.append(f"- **Type {t}**: `{s}` — {why}")
    lines += ["", "## Evidence currently supports", *(supports or ["- (none licensed by the evidence)"]),
              "", "## Evidence does not yet support", *(not_yet or ["- (none flagged)"]),
              "", "## Recommended validation design", *(reco or ["- design adequate for the artefacts assessed"]),
              "", "_'not measurable' is distinct from 'clean'; no production threshold is changed by this audit._"]
    (out / "report.md").write_text("\n".join(lines) + "\n")

def cmd_audit(args):
    p = Path(args.case)
    if not p.exists():
        print(f"ERROR: case file not found: {p}"); return 2
    c, status, allowed, forbidden, reco = _status_full(p)
    name = c.get("name", p.stem); dom = c.get("domain", "?")
    # engine raw outputs (feasibility_matrix, type_A_to_G_status, allowed/forbidden/recommended, audit_report)
    engine.run_case(p, args.out)
    _write_reports(name, dom, status, allowed, forbidden, reco, args.out or (p.parent / "output"))
    print(f"audited {name} ({dom}); reports -> {args.out or (p.parent / 'output')}")
    print(json.dumps({t: s for t, (s, _) in status.items()}, indent=2))
    return 0

def cmd_demo(args):
    case = examples_dir() / "minimal_case" / "case.yaml"
    if not case.exists():
        cands = sorted(examples_dir().glob("*/case.yaml"))
        if not cands: print("ERROR: no bundled examples found"); return 2
        case = cands[0]
    print(f"running demo on {case.parent.name} ...")
    ns = argparse.Namespace(case=str(case), out=args.out)
    return cmd_audit(ns)

def cmd_reproduce_figures(args):
    from . import repro
    w = repro.reproduce_figures(args.out, quick=args.quick)
    print(f"reproduced {len(w)} figure(s) from locked source data -> {args.out}")
    for p in w: print(f"  {p}")
    return 0

def cmd_reproduce_results(args):
    from . import repro
    rows = repro.reproduce_results(args.out, quick=args.quick)
    print(f"re-emitted + checksummed {len(rows)} locked source-data file(s) -> {args.out}")
    return 0

def build_parser():
    ap = argparse.ArgumentParser(prog="biobenchguard",
        description="Rule-based measurement-feasibility audit for biological-prediction benchmarks (not a trained model).")
    ap.add_argument("--version", action="version", version=f"BioBenchGuard {__version__}")
    sub = ap.add_subparsers(dest="cmd")
    d = sub.add_parser("demo", help="run the bundled minimal example"); d.add_argument("--out", default="demo_results"); d.set_defaults(fn=cmd_demo)
    v = sub.add_parser("validate", help="check a case.yaml structure"); v.add_argument("case"); v.set_defaults(fn=cmd_validate)
    a = sub.add_parser("audit", help="audit a case.yaml -> report.md + report.json"); a.add_argument("case"); a.add_argument("--out"); a.set_defaults(fn=cmd_audit)
    rf = sub.add_parser("reproduce-figures", help="redraw headline figures from locked source data")
    rf.add_argument("--quick", action="store_true", default=True); rf.add_argument("--out", default="reproduced_figures"); rf.set_defaults(fn=cmd_reproduce_figures)
    rr = sub.add_parser("reproduce-results", help="re-emit + checksum locked source data")
    rr.add_argument("--quick", action="store_true", default=True); rr.add_argument("--out", default="reproduced_results"); rr.set_defaults(fn=cmd_reproduce_results)
    return ap

def main(argv=None):
    ap = build_parser(); args = ap.parse_args(argv)
    if not getattr(args, "fn", None):
        ap.print_help(); return 1
    return args.fn(args)
