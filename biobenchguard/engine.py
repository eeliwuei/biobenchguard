#!/usr/bin/env python3
"""BioBenchGuard — a TRANSPARENT, RULE-BASED audit tool for structured-biological-prediction benchmarks.

It is NOT a trained or predictive model. Every verdict is an explicit threshold/branch on the reported evaluation
design (the measurement-feasibility gate, Type A-G). Input: one case.yaml describing a benchmark/claim. Output:
feasibility_matrix.csv, type_A_to_G_status.csv, allowed_claims.md, forbidden_claims.md,
recommended_validation_design.md, audit_report.md.

Usage (prefer the CLI):
  biobenchguard audit <case.yaml> --out DIR
  biobenchguard demo --out DIR
See docs/case_yaml_schema.md for the input contract and the manuscript Methods for the formal framework.
"""
import sys, csv, json, argparse
from pathlib import Path
try:
    import yaml
except ImportError:
    print("pyyaml required: pip install pyyaml"); raise

# ---- thresholds (explicit; carried from the framework; override in case.yaml: thresholds:) ----
DEFAULTS = dict(tau_contrast=0.05,      # Type B relatedness/structure contrast gate
                collapse_eps=0.03,      # Type A material random-vs-structure gap
                baseline_eps=0.03,      # Type C baseline-competitiveness band
                leak_eps=0.02,          # Type E material leakage
                typef_min_group=30,     # Type F minimum units per group
                typef_eps=0.03,         # Type F material pooled-vs-within gap
                struct_aware_splits={"structure_aware","scaffold","leave_study_out","cold_target",
                                     "leave_cluster","leave_family","leave_environment","cross_ancestry"})

def g(d, *path, default=None):
    for p in path:
        if not isinstance(d, dict) or p not in d or d[p] is None: return default
        d = d[p]
    return d

# ---------------- the 8 transparent functions ----------------
def check_evidence_tier(c):
    md = c.get("dataset_metadata", {})
    return dict(raw_features=bool(md.get("raw_features_available")),
                labels=bool(md.get("labels_available")),
                structure_axis=md.get("structure_axis","none"),
                evidence_tier=md.get("evidence_tier","unknown"))

def compute_structure_contrast(c):
    sm = c.get("split_metadata", {})
    return dict(contrast=sm.get("structure_contrast"), split_type=sm.get("split_type","none"))

def detect_sample_size_coupling(c):
    sm = c.get("split_metadata", {}); r = c.get("results", {})
    return dict(matched_n_reported=bool(sm.get("matched_n_reported")),
                matched_n_metric=r.get("matched_n_metric"), random_metric=r.get("random_metric"))

def audit_baseline_tuning(c):
    bc = c.get("baseline_config", {})
    return dict(tuned=bool(bc.get("tuned_baseline_present")), name=bc.get("baseline_name","(none)"))

def audit_leakage_risk(c):
    pp = c.get("preprocessing_log", {}); r = c.get("results", {})
    return dict(feature_selection=pp.get("feature_selection","unknown"),
                duplicate_control=pp.get("duplicate_control"),
                global_scaling_before_split=pp.get("global_scaling_before_split"),
                three_arm=r.get("three_arm"))

def compare_pooled_within_group(c):
    gs = c.get("group_structure", {}); r = c.get("results", {})
    return dict(n_groups=gs.get("n_groups"), groups_ge_min=gs.get("groups_with_ge_min"),
                pooled=r.get("pooled_metric"), within=r.get("within_group_metric"))

def _num(x):
    try: return float(x)
    except (TypeError, ValueError): return None

def assign_status(c, T):
    """Return {Type: (status, rationale)} for A-G using explicit rules only."""
    et = check_evidence_tier(c); sc = compute_structure_contrast(c); ss = detect_sample_size_coupling(c)
    bt = audit_baseline_tuning(c); lk = audit_leakage_risk(c); pw = compare_pooled_within_group(c)
    r = c.get("results", {}); out = {}

    # Type G — evidence tier (decide measurability ceiling first)
    tier = et["evidence_tier"]
    g_notes = []
    if tier in ("matrix_only",): g_notes.append("relationship-matrix-only: SNP/feature-level (Type E) not measurable")
    if tier in ("summary_level",): g_notes.append("summary-level only: no individual-level modelling")
    if tier in ("score_only",): g_notes.append("model-scores only: raw-feature artefacts not measurable")
    if not et["structure_axis"] or et["structure_axis"]=="none": g_notes.append("no structure axis recorded")
    out["G"] = ("tier_limited" if g_notes else "measurable_structure_present",
                "; ".join(g_notes) if g_notes else f"raw_features={et['raw_features']}, structure={et['structure_axis']}")

    # Type A — structure-aware collapse
    ra, saw = _num(r.get("random_metric")), _num(r.get("structure_aware_metric"))
    if et["structure_axis"] in (None,"none"):
        out["A"] = ("not_measurable_no_structure","no structure axis to build a structure-aware split")
    elif ra is None or saw is None:
        if sc["split_type"] in T["struct_aware_splits"]:
            out["A"] = ("not_tested","structure-aware split used but random-vs-strict gap not reported")
        else:
            out["A"] = ("not_measurable_no_structure","only a random/in-distribution metric reported; no structure-aware comparison")
    else:
        gap = ra - saw
        out["A"] = (("present" if gap > T["collapse_eps"] else "absent_with_sufficient_contrast"),
                    f"random {ra:.3f} vs structure-aware {saw:.3f} (gap {gap:+.3f}; eps {T['collapse_eps']})")

    # Type B — support vs structure (the headline gate)
    con = _num(sc["contrast"])
    if con is None:
        coupling = g(c,"split_metadata","sample_size_coupling")
        if coupling in ("confounded_with_n","coupled_n_confound"):
            out["B"] = ("present_sample_size_confounding","decay coupled with training-set size, not a relatedness budget")
        else:
            out["B"] = ("not_tested","no train-test structure contrast reported")
    elif con < T["tau_contrast"]:
        out["B"] = ("inconclusive_low_contrast",
                    f"contrast {con:.3f} < gate {T['tau_contrast']}: absence NOT inferable (measurement feasibility fails)")
    else:
        if ss["matched_n_reported"]:
            mn, rm = _num(ss["matched_n_metric"]), _num(ss["random_metric"])
            if mn is not None and rm is not None and abs(mn-rm) <= T["collapse_eps"]:
                out["B"] = ("present_structural",
                            f"contrast {con:.3f} >= gate; matched-N metric {mn:.3f} ~ random {rm:.3f} -> structural, not support")
            else:
                out["B"] = ("confounded_sample_size",
                            f"contrast {con:.3f} >= gate but effect changes at matched-N -> sample-size confound")
        else:
            out["B"] = ("present","contrast >= gate; relatedness/structure budget measurable (matched-N not reported)")

    # Type C — tuned-baseline competitiveness
    fmb = _num(r.get("flexible_minus_baseline"))
    if not bt["tuned"]:
        out["C"] = ("not_tested","no tuned baseline reported")
    elif fmb is None:
        out["C"] = ("not_tested",f"tuned baseline '{bt['name']}' present but flexible-minus-baseline not reported")
    else:
        out["C"] = (("absent_with_sufficient_contrast" if fmb > T["baseline_eps"] else "present"),
                    f"flexible - tuned baseline = {fmb:+.3f} (eps {T['baseline_eps']}); 'present' = baseline competitive")

    # Type D — residual nonlinear advantage (reserved)
    if out["C"][0]=="absent_with_sufficient_contrast" and out["A"][0]=="present":
        out["D"] = ("candidate_not_isolated","flexible edge survives, but not isolated from leakage (E); reserved")
    else:
        out["D"] = ("not_applicable","no surviving flexible advantage after A/C controls")

    # Type E — leakage (matched three-arm where available)
    if not et["raw_features"]:
        out["E"] = ("not_measurable_no_raw_features","no raw features: cannot re-do within-fold selection")
    else:
        ta = lk["three_arm"]
        if isinstance(ta, dict) and all(k in ta for k in ("clean_variance","clean_supervised","leaky_supervised")):
            A_,B_,C_ = _num(ta["clean_variance"]),_num(ta["clean_supervised"]),_num(ta["leaky_supervised"])
            pure = C_-B_; sel = B_-A_; tot = C_-A_
            out["E"] = (("present" if pure > T["leak_eps"] else "absent_with_sufficient_contrast"),
                        f"three-arm: selector {sel:+.3f}, pure-leak {pure:+.3f}, total {tot:+.3f} (eps {T['leak_eps']})")
        elif lk["feature_selection"]=="full_data" or lk["global_scaling_before_split"] or lk["duplicate_control"] is False:
            risks=[]
            if lk["feature_selection"]=="full_data": risks.append("feature selection on full data")
            if lk["global_scaling_before_split"]: risks.append("global scaling before split")
            if lk["duplicate_control"] is False: risks.append("no duplicate/overlap control")
            out["E"] = ("present_risk_uquantified","leakage risk present: "+", ".join(risks)+"; run matched three-arm to quantify")
        elif lk["feature_selection"]=="within_fold":
            out["E"] = ("absent_with_sufficient_contrast","within-fold selection + (no flagged leak); residual leak not quantified")
        else:
            out["E"] = ("not_tested","preprocessing/leakage controls not fully reported")

    # Type F — aggregation (pooled vs within-group)
    ng, gge = pw["n_groups"], pw["groups_ge_min"]; pooled, within = _num(pw["pooled"]), _num(pw["within"])
    if et["structure_axis"] in (None,"none"):
        out["F"] = ("not_measurable_no_structure","no grouping to compute within-group metric")
    elif gge is not None and gge < 2:
        out["F"] = ("not_measurable_low_coverage",
                    f"only {gge} group(s) with >= {T['typef_min_group']} units: within-group metric not reliably measurable")
    elif pooled is None or within is None:
        out["F"] = ("not_tested","pooled and within-group metrics not both reported")
    else:
        out["F"] = (("present" if abs(pooled-within) > T["typef_eps"] else "absent_with_sufficient_contrast"),
                    f"pooled {pooled:.3f} vs within-group {within:.3f} (gap {pooled-within:+.3f}; eps {T['typef_eps']})")
    return out, dict(evidence=et, contrast=sc, support=ss, baseline=bt, leakage=lk, aggregation=pw)

# ---------------- claim-boundary generation ----------------
ALLOWED = {
 "present":"the artefact is present and was properly measured.",
 "present_structural":"a structure (relatedness/budget) effect is present at matched support.",
 "present_sample_size_confounding":"an accuracy-vs-support effect is present (reported as sample-size confounding, not a structure budget).",
 "absent_with_sufficient_contrast":"the artefact was measurable and not detected (true absence in this benchmark).",
}
FORBIDDEN = {
 "inconclusive_low_contrast":"do NOT infer the artefact is absent (measurement feasibility failed: contrast below gate).",
 "not_measurable_no_structure":"do NOT claim the artefact is absent (no structure axis to measure it).",
 "not_measurable_no_raw_features":"do NOT make a feature/SNP-level claim (no raw features).",
 "not_measurable_low_coverage":"do NOT report the within-group metric as a finding (too few groups).",
 "not_measurable_no_labels":"do NOT claim predictive performance (no labels).",
 "present_risk_uquantified":"do NOT report performance as model capability until leakage is quantified (run the matched three-arm).",
 "confounded_sample_size":"do NOT attribute the effect to structure (it changes at matched-N: sample-size confound).",
 "candidate_not_isolated":"do NOT claim a genuine nonlinear advantage until leakage (E) is excluded.",
}
RECO = {
 "A":"report a structure-aware split (leave-cluster/scaffold/leave-study/cross-ancestry) alongside random CV.",
 "B":"vary structure distance at matched training-N; ensure train-test contrast >= gate before any absence claim.",
 "C":"include a properly tuned simple/linear baseline under the strict regime.",
 "E":"redo all feature selection/preprocessing inside the training fold; run the matched three-arm (A/B/C arms).",
 "F":"report pooled AND within-group metrics over groups with sufficient units.",
 "G":"state the evidence tier; do not assert claims the tier cannot support.",
}

def generate_claim_boundary_report(status):
    allowed, forbidden, reco = [], [], []
    for t,(s,why) in status.items():
        base = next((v for k,v in ALLOWED.items() if s.startswith(k)), None)
        if base: allowed.append(f"- Type {t}: {base}  ({why})")
        fb = FORBIDDEN.get(s)
        if fb: forbidden.append(f"- Type {t}: {fb}  ({why})")
        if (s.startswith("not_measurable") or s.startswith("inconclusive") or s in ("not_tested","present_risk_uquantified","confounded_sample_size")) and t in RECO:
            reco.append(f"- Type {t}: {RECO[t]}")
    return allowed, forbidden, reco

# ---------------- run one case ----------------
def run_case(case_path, out_dir=None):
    c = yaml.safe_load(Path(case_path).read_text())
    T = dict(DEFAULTS); T.update(c.get("thresholds", {}))
    T["struct_aware_splits"] = set(T["struct_aware_splits"])
    status, detail = assign_status(c, T)
    allowed, forbidden, reco = generate_claim_boundary_report(status)
    out = Path(out_dir or (Path(case_path).parent/"output")); out.mkdir(parents=True, exist_ok=True)
    name = c.get("name", Path(case_path).stem); dom = c.get("domain","?")
    # feasibility matrix
    with open(out/"feasibility_matrix.csv","w",newline="") as f:
        w=csv.writer(f); w.writerow(["artefact","measurable"])
        for t,(s,_) in status.items():
            meas = not (s.startswith("not_measurable") or s=="not_tested")
            w.writerow([t, "yes" if meas else ("inconclusive" if s.startswith("inconclusive") else "no")])
    # status table
    with open(out/"type_A_to_G_status.csv","w",newline="") as f:
        w=csv.writer(f); w.writerow(["artefact","status","rationale"])
        for t,(s,why) in status.items(): w.writerow([t,s,why])
    (out/"allowed_claims.md").write_text(f"# Allowed claims — {name} ({dom})\n\n"+("\n".join(allowed) if allowed else "- (none licensed)")+"\n")
    (out/"forbidden_claims.md").write_text(f"# Forbidden claims — {name} ({dom})\n\n"+("\n".join(forbidden) if forbidden else "- (none flagged)")+"\n")
    (out/"recommended_validation_design.md").write_text(f"# Recommended validation design — {name} ({dom})\n\n"+("\n".join(reco) if reco else "- design adequate for the artefacts assessed")+"\n")
    # report
    lines=[f"# BioBenchGuard audit report — {name} ({dom})","",
           "Rule-based, transparent (not a trained model). Status per Type A-G:",""]
    for t,(s,why) in status.items(): lines.append(f"- **Type {t}**: `{s}` — {why}")
    lines += ["","## Allowed", *(allowed or ["- (none)"]), "","## Forbidden", *(forbidden or ["- (none)"]),
              "","## Recommended validation design", *(reco or ["- adequate"])]
    (out/"audit_report.md").write_text("\n".join(lines)+"\n")
    return name, dom, {t:s for t,(s,_) in status.items()}, str(out)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("case", nargs="?"); ap.add_argument("--out"); ap.add_argument("--all", action="store_true")
    a=ap.parse_args()
    root=Path(__file__).resolve().parent.parent
    if a.all:
        cases=sorted(root.glob("examples/*/case.yaml"))
        print(f"running {len(cases)} demo cases:")
        for cp in cases:
            n,d,st,o=run_case(cp); print(f"  {n} ({d}): "+", ".join(f"{t}={s}" for t,s in st.items()))
        return
    if not a.case: ap.error("provide a case.yaml or --all")
    n,d,st,o=run_case(a.case, a.out)
    print(f"audited {n} ({d}); outputs -> {o}")
    print(json.dumps(st, indent=2))

if __name__=="__main__": main()
