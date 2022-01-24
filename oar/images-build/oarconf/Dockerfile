FROM python:latest

COPY generate_oar_resources.py ./
COPY del_node.sh ./
COPY add_node.sh ./
COPY init_node.sh ./

RUN echo "deb http://deb.debian.org/debian bullseye-backports main contrib non-free" >> /etc/apt/sources.list && apt-get update && apt-get install -y vim.tiny oar-server oar-server-pgsql && apt-get clean && pip install --upgrade pip && pip install kubernetes && mkdir -p /oarconf && rm -f /etc/oar/oar.conf && ln -s /oarconf/oar.conf /etc/oar/oar.conf && chmod a+x /del_node.sh && chmod a+x /add_node.sh && chmod a+x /init_node.sh

CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"
