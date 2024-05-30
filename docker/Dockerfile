FROM python:3.12-slim as builder
ENV POETRY_CACHE_DIR=/app/poetry_cache \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1
WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN --mount=type=cache,target=$POETRY_CACHE_DIR pip install poetry && poetry lock --no-update && poetry install --no-root



FROM python:3.12-slim as runner
WORKDIR /app
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}
COPY . /app
RUN apt-get update &&  \
    apt-get install binutils libproj-dev gdal-bin -y && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ENTRYPOINT ["gunicorn", "service_area_api.wsgi:application", "--workers", "4", "--log-level", "info", "--bind", "unix:/app/sockets/backend.sock"]