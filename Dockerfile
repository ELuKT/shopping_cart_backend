# docker build -t fastapi-sc-backend:latest -f Dockerfile .
# docker run --env-file .env -d -p 8000:8000 --name fastapi-sc-backend --network fastapi-sc-backend_mongodb-network fastapi-sc-backend:latest
FROM python:3.8.16 as builder
WORKDIR /wrokspace

RUN python -m venv dep
ENV PATH="/wrokspace/dep/bin:$PATH"

COPY requirements.txt ./
RUN pip install --no-cache-dir -r /wrokspace/requirements.txt

FROM python:3.8.16-slim
WORKDIR /wrokspace

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y \
    curl && \
    rm -rf /var/lib/apt/lists/*

COPY --from=builder /wrokspace/dep /wrokspace/dep
ENV PATH="/wrokspace/dep/bin:$PATH"

COPY log-config.ini ./
COPY app app
ENTRYPOINT [ "uvicorn", "app.app:app", "--host", "0.0.0.0", "--log-config", "log-config.ini"]
