FROM python:latest

RUN pip install --upgrade pip
RUN pip install kubernetes
RUN mkdir -p /locate

COPY probe.py ./

CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"
