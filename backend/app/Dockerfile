FROM python:3.11-slim

WORKDIR /app

RUN apt-get update --fix-missing \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir alembic

COPY backend/app/ /app
COPY backend/app/alembic.ini /app/alembic.ini
COPY backend/app/migrations /app/migrations

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
