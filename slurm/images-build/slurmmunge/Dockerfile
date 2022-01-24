FROM debian:latest

RUN apt-get update && apt-get install -y munge && apt-get clean
RUN mkdir /run/munge

COPY start-munge.sh ./

CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"
