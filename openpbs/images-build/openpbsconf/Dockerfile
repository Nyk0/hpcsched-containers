FROM python:latest

RUN apt-get update && apt-get install -y procps git vim.tiny gcc make libtool libhwloc-dev libx11-dev libxt-dev libedit-dev libical-dev ncurses-dev perl postgresql-server-dev-all postgresql-contrib python3-dev tcl-dev tk-dev swig libexpat-dev libssl-dev libxext-dev libxft-dev autoconf automake g++ && apt-get clean && mkdir /pbsconf && git clone https://github.com/openpbs/openpbs.git && pip install --upgrade pip && pip install kubernetes

WORKDIR "/openpbs"
run ./autogen.sh && ./configure --prefix=/opt/pbs && make && make install

WORKDIR "/"

COPY generate_pbs_conf.py ./
COPY add_partition.sh ./
COPY del_partition.sh ./
COPY add_node.sh ./
COPY del_node.sh ./

RUN /opt/pbs/libexec/pbs_postinstall && rm -rf /openpbs && chmod 4755 /opt/pbs/sbin/pbs_iff /opt/pbs/sbin/pbs_rcp && rm -rf /etc/pbs.conf && ln -s /pbsconf/pbs.conf /etc/pbs.conf && chmod a+x /*.sh

CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"
