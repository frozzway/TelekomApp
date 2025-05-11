FROM python:3.10-slim
RUN pip install --no-cache-dir poetry
RUN apt-get update && apt-get install -y curl iputils-ping
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
  && poetry install --no-root --no-interaction --no-ansi
COPY . .
EXPOSE 8000
CMD ["poetry", "run", "python", "-m", "app"]