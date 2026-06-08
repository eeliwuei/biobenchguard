# BioBenchGuard paper artifact — convenience targets (CPU-only; no GPU).
PY ?= python
.PHONY: install demo audit test reproduce-figures reproduce-results docker-build docker-demo smoke

install:
	pip install -e .[test]
demo:
	$(PY) -m biobenchguard demo --out demo_results
audit:
	$(PY) -m biobenchguard audit examples/typeE_selection_leakage/case.yaml --out audit_results
test:
	$(PY) -m pytest -q
reproduce-figures:
	$(PY) -m biobenchguard reproduce-figures --quick --out reproduced_figures
reproduce-results:
	$(PY) -m biobenchguard reproduce-results --quick --out reproduced_results
smoke:
	bash scripts/cli_smoke_test.sh
docker-build:
	docker build -t biobenchguard:paper .
docker-demo:
	docker run --rm -v "$$PWD:/work" biobenchguard:paper biobenchguard demo --out /work/demo_results
