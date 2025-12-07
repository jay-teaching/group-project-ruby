# Pick a base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install uv as per official docs
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy uv project configuration
COPY pyproject.toml .
COPY uv.lock .
COPY .python-version .

# Copy project files
COPY notebooks/* notebooks/
COPY input/* input/

# Install dependencies with uv
RUN uv sync

# Expose port for marimo
EXPOSE 8080

# Run marimo with uv
CMD ["uv", "run", "marimo", "run", "--host", "0.0.0.0", "--port", "8080", "notebooks/telco_marimo.py"]