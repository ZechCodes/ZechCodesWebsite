FROM python:3.11-buster as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    pip install --upgrade pip && \
    pip install poetry

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry export --without-hashes -f requirements.txt --output requirements.txt && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

FROM python:3.11-slim

RUN addgroup --gid 1001 --system app && \
    adduser --no-create-home --shell /bin/false --disabled-password --uid 1001 --system --group app

WORKDIR /app
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache --upgrade pip && \
    pip install --no-cache /wheels/*

RUN chmod ugo+rw /app
COPY website website

USER app
ENTRYPOINT ["python", "-m", "website"]
