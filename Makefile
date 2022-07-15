test:
	PYTHONPATH=$(PWD) pytest -v -s --cov=mstate --cov-report=term-missing .
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -exec rm -rf {} +
