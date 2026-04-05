FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project


FROM docker.io/library/python:3.12-slim

WORKDIR /app

COPY --from=builder /app/.venv .venv
COPY app/ app/

ENV PATH="/app/.venv/bin:$PATH"
