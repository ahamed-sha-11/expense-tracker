# Python 3.14 with uv already installed
FROM ghcr.io/astral-sh/uv:python3.14-bookworm-slim

WORKDIR /app

# Copy real files into the venv instead of linking, and precompile .pyc files
ENV UV_LINK_MODE=copy
ENV UV_COMPILE_BYTECODE=1

# Step 1: install only the dependencies.
# This layer is cached and only rebuilds when pyproject.toml or uv.lock change.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Step 2: copy the code and install the project itself
COPY . .
RUN uv sync --frozen --no-dev

# Use the venv's python and uvicorn by default
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8080

CMD ["uvicorn", "expense_tracker.main:app", "--host", "0.0.0.0", "--port", "8080"]
