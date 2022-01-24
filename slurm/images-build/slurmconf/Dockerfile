FROM python:latest

ARG slurm_version=21.08.5

COPY generate_slurm_conf.py ./
COPY restart-slurm.sh ./

RUN apt-get update && apt-get install -y vim.tiny procps netcat gcc g++ wget bzip2 make python3 perl libhttp-parser-dev libjson-c-dev libmunge-dev && apt-get clean && mkdir /run/munge && wget https://download.schedmd.com/slurm/slurm-$slurm_version.tar.bz2 && tar -xjf slurm-$slurm_version.tar.bz2 && pip install --upgrade pip && pip install kubernetes ClusterShell psutil && mkdir -p /etc/slurm && chmod a+x /restart-slurm.sh && mkdir -p /var/slurm && mkdir -p /run/munge && useradd -d /var/slurm -r -u 600 -U slurm

RUN pip install --upgrade pip
RUN pip install kubernetes ClusterShell psutil
RUN mkdir -p /etc/slurm

WORKDIR "/slurm-$slurm_version"
RUN ./configure --enable-multiple-slurmd --with-munge --enable-slurmrestd && make && make install && make contrib && make install-contrib && echo "export SLURM_CONF=/etc/slurm/slurm.conf" >> /root/.bashrc

WORKDIR "/"
RUN rm -f slurm-$slurm_version.tar.bz2

CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"
