FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry==2.1.2
RUN poetry config virtualenvs.create false

COPY pyproject.toml ./
RUN poetry install --no-root

COPY . .
RUN poetry install

CMD ["poetry", "run", "start"]
