test:
    uv run --all-extras --frozen pytest

test-all:
    uv run --all-extras --frozen --python 3.11 pytest
    uv run --all-extras --frozen --python 3.12 pytest
    uv run --all-extras --frozen --python 3.13 pytest

lint:
    uv run --frozen pre-commit run --all-files