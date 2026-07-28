.PHONY: install demo-local test lint format typecheck validate-infra check clean-local

install:
	python -m pip install -r requirements.txt

demo-local:
	python -m fraud_detection demo --transactions 1000 --seed 42

test:
	python -m pytest

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy src

validate-infra:
	terraform fmt -check -recursive terraform
	cd terraform/environments/dev && terraform init -backend=false && terraform validate

check: lint typecheck test validate-infra

clean-local:
	python scripts/clean_local.py
