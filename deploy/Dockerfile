FROM python:3.9-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=source/requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

RUN apt-get update
RUN apt-get install libx11-6 libgl1 libxrender1 -y

COPY source .

EXPOSE 8050

ENV OILCASEX_URL=${OILCASEX_URL}

CMD ["gunicorn", "--bind", "0.0.0.0:8050", "--workers", "8", "--threads", "4", "main:server"]
