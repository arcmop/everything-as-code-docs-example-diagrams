FROM python:3.8.10-slim

RUN apt update \
    && apt install -y graphviz \
    && rm -rf /var/lib/apt/lists/* \
    && pip install diagrams

ENTRYPOINT ["python"]
