FROM python:3.14-slim

RUN pip install --no-cache-dir uv

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY webapp ./webapp
COPY translations ./translations
COPY static ./static
COPY fonts ./fonts
COPY wsgi.py ./

ENV PATH="/app/.venv/bin:$PATH" \
    TZ="America/Toronto" \
    FLASK_APP=wsgi:app

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
