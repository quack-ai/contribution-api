FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-alpine3.14

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/app"

# copy requirements file
COPY requirements.txt /app/requirements.txt

# install dependencies
RUN set -eux \
    && pip install -r /app/requirements.txt \
    && rm -rf /root/.cache/pip

# copy project
COPY src/app /app/app
COPY src/alembic /app/alembic
COPY src/alembic.ini /app/alembic.ini
