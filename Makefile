format:
	@isort . && black . && ruff .

install:
	@python3.11 -m pip install -r requirements.txt
