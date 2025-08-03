# Ralex Development Makefile

.PHONY: help install dev-install format lint type-check test test-unit test-integration clean build pre-commit security

# Default target
help:
	@echo "Ralex Development Commands:"
	@echo ""
	@echo "Setup:"
	@echo "  install         Install production dependencies"
	@echo "  dev-install     Install development dependencies"
	@echo "  pre-commit      Install pre-commit hooks"
	@echo ""
	@echo "Code Quality:"
	@echo "  format          Format code with Black"
	@echo "  lint            Lint code with Ruff"
	@echo "  type-check      Type check with MyPy"
	@echo "  security        Security scan with Bandit"
	@echo ""
	@echo "Testing:"
	@echo "  test            Run all tests"
	@echo "  test-unit       Run unit tests only"
	@echo "  test-integration Run integration tests only"
	@echo ""
	@echo "Build:"
	@echo "  clean           Clean build artifacts"
	@echo "  build           Build distribution packages"
	@echo ""
	@echo "CI/CD:"
	@echo "  ci              Run full CI pipeline locally"

# Installation
install:
	pip install -r requirements.txt
	pip install -e .

dev-install: install
	pip install black ruff mypy pytest pytest-cov bandit safety pre-commit
	pip install build twine

pre-commit: dev-install
	pre-commit install
	pre-commit autoupdate

# Code Quality
format:
	@echo "🎨 Formatting code with Black..."
	black ralex_core/ tools/ tests/

lint:
	@echo "🔍 Linting code with Ruff..."
	ruff check ralex_core/ tools/ tests/

lint-fix:
	@echo "🔧 Fixing linting issues with Ruff..."
	ruff check --fix ralex_core/ tools/ tests/

type-check:
	@echo "🔬 Type checking with MyPy..."
	mypy ralex_core/ --ignore-missing-imports

security:
	@echo "🔒 Running security scan with Bandit..."
	bandit -r ralex_core/ -f txt
	@echo "🛡️  Checking dependencies with Safety..."
	safety check || true

# Testing
test:
	@echo "🧪 Running test suite..."
	pytest tests/ -v --cov=ralex_core --cov-report=term --cov-report=xml

test-unit:
	@echo "🔬 Running unit tests..."
	pytest tests/unit/ -v

test-integration:
	@echo "🔄 Running integration tests..."
	pytest tests/integration/ -v

# Build
clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf .mypy_cache/
	rm -rf .coverage
	rm -rf coverage.xml
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	@echo "📦 Building distribution packages..."
	python -m build
	twine check dist/*

# CI/CD Pipeline
ci: format lint type-check security test
	@echo "✅ CI pipeline completed successfully!"

# Quick development cycle
dev: format lint-fix test-unit
	@echo "🚀 Quick development cycle completed!"

# Full validation
validate: clean ci build
	@echo "🎯 Full validation completed!"