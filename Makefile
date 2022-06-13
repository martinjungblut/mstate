test:
	pytest -v -s --cov=mstate --cov-report=term-missing .
test-feature:
	pytest -v -s --cov=mstate --cov-report=term-missing -m feature .
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -exec rm -rf {} +
