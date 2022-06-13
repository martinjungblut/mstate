test:
	pytest -v -s --cov=mstate --cov-report=term-missing .
test-feature:
	pytest -m feature -v -s --cov=mstate --cov-report=term-missing .
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -exec rm -rf {} +
