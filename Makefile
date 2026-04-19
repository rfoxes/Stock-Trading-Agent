.PHONY: install install-talib test lint typecheck run dry-run dashboard docker-up docker-down format

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install ruff mypy pytest pytest-asyncio pytest-cov

install-talib:
	@echo "Installing TA-Lib C library..."
	@if [ "$$(uname)" = "Darwin" ]; then \
		brew install ta-lib; \
	elif [ "$$(uname)" = "Linux" ]; then \
		sudo apt-get update && sudo apt-get install -y libta-lib-dev; \
	fi
	pip install TA-Lib

test:
	pytest tests/ -v

test-safety:
	pytest tests/test_safety_gate.py tests/test_config.py -v

test-cov:
	pytest tests/ --cov=quant_trading_system --cov-report=term-missing -v

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy quant_trading_system/

run:
	python main.py

dry-run:
	python main.py --dry-run --once

dashboard:
	python main.py --dashboard --backtest auto

docker-up:
	docker compose up -d postgres

docker-down:
	docker compose down
