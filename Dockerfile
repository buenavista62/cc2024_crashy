FROM docker.io/library/ubuntu:24.04 as base

RUN apt-get update && \
  DEBIAN_FRONTEND=noninteractive apt-get install -y python3 && \
  rm -rf /var/lib/apt/lists/*

FROM base as builder

COPY --from=ghcr.io/astral-sh/uv:0.4.29-alpine3.20 /usr/local/bin/uv /bin/

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

WORKDIR /app
# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    /bin/uv sync --frozen --no-install-project --no-dev

FROM base
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH" \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    STREAMLIT_SERVER_FILE_WATCHER_TYPE=none

COPY *.py ./

CMD ["streamlit", "run", "crashy.py"]