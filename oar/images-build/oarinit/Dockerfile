FROM python:latest

RUN echo "deb http://deb.debian.org/debian bullseye-backports main contrib non-free" >> /etc/apt/sources.list && apt-get update && apt-get install -y vim.tiny oar-server-pgsql oar-user-pgsql oar-server netcat && apt-get clean && pip install --upgrade pip && pip install kubernetes && mkdir /oarconf

COPY generate_oar_conf.py ./
COPY init-postgres.sh ./

CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"
