FROM --platform=linux/amd64 python:3.13

ENV SOLIDITY_VERSION=${SOLIDITY_VERSION:-v0.8.0}
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y postgresql-client curl && \
    rm -rf /var/lib/apt/lists/*

RUN curl -L https://github.com/ethereum/solidity/releases/download/${SOLIDITY_VERSION}/solc-static-linux -o /usr/local/bin/solc \
    && chmod +x /usr/local/bin/solc

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/