FROM debian:latest

ARG slurm_version=21.08.5
ARG ompi_version_major=4.1
ARG ompi_version_minor=4.1.2

RUN apt-get update && apt-get install -y procps vim.tiny netcat gcc g++ wget bzip2 make python3 perl libhttp-parser-dev libjson-c-dev libmunge-dev daemontools host && apt-get clean && wget https://download.schedmd.com/slurm/slurm-$slurm_version.tar.bz2 && tar -xjf slurm-$slurm_version.tar.bz2 && useradd -d /var/slurm -r -u 600 -U slurm && mkdir /var/slurm && chown slurm:slurm /var/slurm && mkdir /etc/slurm && mkdir /run/munge && mkdir /locate && mkdir -p /service/slurmctld && mkdir -p /service/slurmd && wget https://download.open-mpi.org/release/open-mpi/v$ompi_version_major/openmpi-$ompi_version_minor.tar.bz2 && tar -xjf openmpi-$ompi_version_minor.tar.bz2 && useradd -s /bin/bash nico

WORKDIR "/slurm-$slurm_version"
RUN ./configure --enable-multiple-slurmd --with-munge --enable-slurmrestd && make && make install && make contrib && make install-contrib

WORKDIR "/openmpi-$ompi_version_minor"
RUN ./configure --with-slurm --with-pmi=/usr/local && make && make install
WORKDIR "/"

COPY infinite.sh pi.c ./home/nico/
COPY infinite.sh ./home/nico/
COPY start-slurmctld.sh ./service/slurmctld/run
COPY start-slurmd.sh ./service/slurmd/run

RUN chmod a+x /service/slurmctld/run && chmod a+x /service/slurmd/run && rm -rf slurm-$slurm_version && rm -f slurm-$slurm_version.tar.bz2 && rm -rf openmpi-$ompi_version_minor && rm -f openmpi-$ompi_version_minor.tar.bz2 && ldconfig && echo "export SLURM_CONF=/etc/slurm/slurm.conf" >> /root/.bashrc

CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"
