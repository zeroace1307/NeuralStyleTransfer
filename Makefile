export PYTHONPATH := $(CURDIR)

test:
	pytest tests/

lint:
	black neuralstyletransfer/
	black tests/
	pylint neuralstyletransfer/
	pylint tests/