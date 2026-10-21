FROM python:3.11-slim-bookworm AS builder

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:0.13.4 /uv /bin/uv
COPY scripts/refresh_ca_trust.py scripts/refresh_ca_trust.py

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    uv pip install --system "pip==26.2.2" "poetry==1.8.5" "certifi==2026.10.19" && \
    python scripts/refresh_ca_trust.py

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry export --without-hashes -f requirements.txt --output requirements.txt && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.11-slim-bookworm

RUN addgroup --gid 1001 --system app && \
    adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group app

WORKDIR /app
COPY --from=builder /bin/uv /bin/uv
COPY --from=builder /app/scripts /app/scripts
COPY --from=builder /app/wheels /wheels
RUN uv pip install --system "certifi==2026.10.19" && \
    python scripts/refresh_ca_trust.py && \
    uv pip install --system /wheels/*

RUN chmod ugo+rw /app
COPY website website

USER app
ENTRYPOINT ["python", "-m", "website"]
