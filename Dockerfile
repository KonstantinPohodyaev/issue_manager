FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-root


CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
