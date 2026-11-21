MAZE_ZIP	= mazegenerator-00001.zip
LIBS		= libs
MAIN		= pac-man.py
CONFIG		= config.json
EXCLUDE		= .venv,$(LIBS),prototype

.PHONY: install run debug clean fclean lint lint-strict

install:
	unzip -o $(MAZE_ZIP) -d $(LIBS)
	uv sync --reinstall-package mazegenerator

run:
	uv run python $(MAIN) $(CONFIG)

debug:
	uv run python -m pdb $(MAIN) $(CONFIG)

clean:
	find . -name "__pycache__" -type d -prune -exec rm -rf {} +
	rm -rf .mypy_cache .pytest_cache

fclean: clean
	rm -rf .venv $(LIBS)

lint:
	uv run flake8 . --exclude $(EXCLUDE)
	uv run mypy . --exclude '\.venv|$(LIBS)|prototype' --warn-return-any \
		--warn-unused-ignores --ignore-missing-imports \
		--disallow-untyped-defs --check-untyped-defs

lint-strict:
	uv run flake8 . --exclude $(EXCLUDE)
	uv run mypy . --exclude '\.venv|$(LIBS)|prototype' --strict
