FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

ENV RAGNA0_SQLITE_PATH="/data/ragna0.db"

RUN pip install SQLAlchemy

COPY ./scraper /app/scraper
COPY ./app /app/
