FROM debian:latest

ARG ompi_version_major=4.1
ARG ompi_version_minor=4.1.2

RUN echo "deb http://deb.debian.org/debian bullseye-backports main contrib non-free" >> /etc/apt/sources.list && apt-get update && apt-get install -y make bzip2 wget g++ gcc vim.tiny oar-server oar-server-pgsql oar-node oar-user oar-user-pgsql && apt-get clean && mkdir /oarconf && rm -f /etc/oar/oar.conf && ln -s /oarconf/oar.conf /etc/oar/oar.conf && mkdir -p /var/run/sshd && useradd -m nico -s /bin/bash && wget https://download.open-mpi.org/release/open-mpi/v$ompi_version_major/openmpi-$ompi_version_minor.tar.bz2 && tar -xjf openmpi-$ompi_version_minor.tar.bz2

WORKDIR "/openmpi-$ompi_version_minor"
RUN ./configure && make && make install
WORKDIR "/"

COPY infinite.sh pi.c ./home/nico/

RUN rm -rf openmpi-$ompi_version_minor && rm -f openmpi-$ompi_version_minor.tar.bz2 && ldconfig && mpicc -o /home/nico/pi /home/nico/pi.c && chown nico:nico /home/nico/*

CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"
