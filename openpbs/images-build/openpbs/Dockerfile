FROM debian:latest

ARG ompi_version_major=4.1
ARG ompi_version_minor=4.1.2

RUN apt-get update && apt-get install -y netcat procps git vim.tiny gcc make libtool libhwloc-dev libx11-dev libxt-dev libedit-dev libical-dev ncurses-dev perl postgresql-server-dev-all postgresql-contrib python3-dev tcl-dev tk-dev swig libexpat-dev libssl-dev libxext-dev libxft-dev autoconf automake g++  bzip2 wget && apt-get clean && useradd -s /bin/bash nico && mkdir /pbsconf && git clone https://github.com/openpbs/openpbs.git && wget https://download.open-mpi.org/release/open-mpi/v$ompi_version_major/openmpi-$ompi_version_minor.tar.bz2 && tar -xjf openmpi-$ompi_version_minor.tar.bz2

WORKDIR "/openpbs"
run ./autogen.sh && ./configure --prefix=/opt/pbs && make && make install

WORKDIR "/openmpi-$ompi_version_minor"
RUN export LD_LIBRARY_PATH=/opt/pbs/lib:$LD_LIBRARY_PATH && export LDFLAGS="-L/opt/pbs/lib -lpbs -lpthread -lcrypto" && ./configure --without-slurm --with-tm=/opt/pbs && make && make install && ldconfig

WORKDIR "/"

COPY start-pbs.sh ./
COPY start-mom.sh ./

RUN /opt/pbs/libexec/pbs_postinstall && rm -rf /openpbs && rm -rf openmpi-$ompi_version_minor && rm -f openmpi-$ompi_version_minor.tar.bz2 && chmod 4755 /opt/pbs/sbin/pbs_iff /opt/pbs/sbin/pbs_rcp && rm -rf /etc/pbs.conf && ln -s /pbsconf/pbs.conf /etc/pbs.conf && touch /server.lock && echo "\$usecp *:/home  /home" >> /var/spool/pbs/mom_priv/config && ldconfig && echo "source /etc/profile.d/pbs.sh" >> /root/.bashrc

CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"
